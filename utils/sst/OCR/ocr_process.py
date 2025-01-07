from concurrent.futures import ThreadPoolExecutor, as_completed

import pytesseract
from PIL import Image, ImageDraw, ImageFont

from utils.settings import (
    ARGS_TUPLE,
    ENGINE_TUPLE,
    FONT_SST,
    Engine,
    Settings,
    setProxy,
)


def get_font_color(bg_color):
    """Determine font color based on background color for best visibility."""
    # Normalize RGB values to [0, 1]
    r, g, b = [x / 255.0 for x in bg_color]
    # Calculate luminance
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    # Return black or white font color based on luminance
    return "black" if luminance > 0.5 else "white"


def return_wrapped_text(draw, text, font, width, num):
    print("text: ", text)
    i = num
    j = 0
    wrapped_text = ""
    if "\n" in text:
        text = text.split("\n")
    else:
        text = [text]
    for line in text:
        while True:
            if i >= len(line):
                wrapped_text += line[j:i]
                break
            # Split the text into lines and measure each line separately
            length = draw.textlength(line[j:i], font=font)
            if length > width:
                wrapped_text += line[j : i - 2] + "\n"
                j = i - 2
            i += 2
        wrapped_text += "\n"
        i = num
        j = 0
    return wrapped_text


def ocr_process(
    image_name: str, engine: int = Engine.GOOGLE, image_num: int = 0
) -> tuple:
    # Open image file
    image = Image.open(image_name)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    block_nums = set(data["block_num"])
    text_todo = []
    heights = []

    for block in block_nums:
        block_texts = []
        block_heights = []
        for i in range(len(data["text"])):
            if (
                data["block_num"][i] == block
                and data["text"][i] != " "
                and data["text"][i]
            ):
                block_texts.append(data["text"][i])
                block_heights.append(data["height"][i])

        if block_texts:
            text_todo.append(" ".join(block_texts))
            heights += block_heights
    print(text_todo)

    height = sum(heights) / len(heights)
    # Create a draw object on the image
    draw = ImageDraw.Draw(image)
    text_trans: list[str] = [""] * len(text_todo)  # Initialize with empty strings
    temp_stream = Settings.STREAM
    Settings.STREAM = False

    def translate_text(index, text):
        # Create a new translator for each thread
        translator = ENGINE_TUPLE[engine](*ARGS_TUPLE[engine](0))
        setProxy(translator)
        return index, translator.en2zh(text)[0]

    with ThreadPoolExecutor() as executor:
        # Submit all translation tasks to the executor
        futures = {
            executor.submit(translate_text, i, text): i
            for i, text in enumerate(text_todo)
        }

        for future in as_completed(futures):
            index, translation = future.result()
            text_trans[index] = translation  # Insert translation in the correct order

    Settings.STREAM = temp_stream

    print(text_trans)
    if not text_trans:
        return (None, None)
    # 指定矩形的颜色
    rectangle_color = (255, 255, 255)  # 白色
    i = 0
    for block in block_nums:
        block_data = {
            k: [
                v[j]
                for j in range(len(data["text"]))
                if data["block_num"][j] == block
                and data["text"][j] != " "
                and data["text"][j]
            ]
            for k, v in data.items()
        }
        if not block_data["text"]:
            continue
        left = min(block_data["left"])
        right = max(block_data["left"]) + max(block_data["width"])
        height = max(block_data["height"])
        top = min(block_data["top"])
        bottom = max(block_data["top"]) + max(block_data["height"])

        rectangle_color = image.getpixel((left - 2, top - 2))

        # 在图像上绘制矩形
        draw.rectangle([(left, top), (right, bottom)], fill=rectangle_color)

        # 选择要绘制的文本和文本颜色
        try:
            text = text_trans[i]
            print(text)
        except IndexError:
            image.save(f"screenshot_image/{image_num}/screenshot_text.png")
            return text_todo, text_trans
        box_height = bottom - top if bottom - top > height else height
        if len(text) == 0:
            continue
        i += 1

        pix = int((((right - left) * box_height / len(text)) ** 0.5) * 0.9)

        # 选择一个字体和字号，确保字体包含中文字符
        font = ImageFont.truetype(FONT_SST, size=pix)
        wrapped_text = return_wrapped_text(
            draw, text, font, (right - left) * 0.9, int((right - left) / pix) + 1
        )
        # text_color = (0, 0, 0)  # 黑色
        text_color = get_font_color(rectangle_color[:3])

        # 指定文本的位置
        text_position = (left, top)

        # 在图像上绘制文本
        draw.text(text_position, wrapped_text, fill=text_color, font=font)

        # 保存图像或显示图像
    image.save(f"screenshot_image/{image_num}/screenshot_text.png")
    return "\n".join(text_todo), "\n".join(text_trans)
