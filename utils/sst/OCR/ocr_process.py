from PIL import Image, ImageDraw, ImageFont
import pytesseract
from ...trans_engine import Google, ChatGPT, DeepL


def get_font_color(bg_color):
    """Determine font color based on background color for best visibility."""
    # Normalize RGB values to [0, 1]
    r, g, b = [x / 255.0 for x in bg_color]
    # Calculate luminance
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    # Return black or white font color based on luminance
    return "black" if luminance > 0.5 else "white"


def return_wrapped_text(draw, text, font, width, num):
    i = num
    j = 0
    wrapped_text = ""
    while True:
        length = draw.textlength(text[j:i], font=font)
        if length > width:
            wrapped_text += text[j : i - 2] + "\n"
            j = i - 2
        if i >= len(text):
            wrapped_text += text[j:i]
            return wrapped_text
        i += 2


def ocr_process(image_name: str, engine: str = "google") -> tuple:
    # 打开图像文件
    image = Image.open(image_name)

    text_pd = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)
    text_pd = text_pd[text_pd['text'].notnull()]
    text_pd = text_pd[text_pd['text'] != ' ']
    text_todo = ''
    for i in text_pd['block_num'].unique():
        text_todo += ' '.join(list(text_pd['text'][text_pd['block_num']==i])) + '\n'
        
    # print(text_todo)

    text_trans:str = ''
    if engine == "google":
        google = Google()
        text_trans = google.google_en2zh(text_todo)[0]
    elif engine == "deepl":
        deepl = DeepL()
        text_trans = deepl.deepl_en2zh(text_todo)[0]
    else:
        print("chatGPT ")
        chatgpt = ChatGPT()
        text_trans = chatgpt.chatgpt_en2zh(text_todo, sst=True)[0]
    
    if not text_trans:
        return (None, None)

    text_trans_list = text_trans.splitlines()

    # 在图像上创建一个绘制对象
    draw = ImageDraw.Draw(image)
    height = text_pd['height'].mean()
    # 指定矩形的颜色
    rectangle_color = (255, 255, 255)  # 白色
    for i, j in enumerate(text_pd['block_num'].unique()):
        temp = text_pd[text_pd['block_num'] == j]
        left = temp['left'].min()
        right = temp['left'].max() + temp['width'].max()
        height = int(temp['height'].max())
        top = temp['top'].min()
        bottom = temp['top'].max() + temp['height'].max()
        
        rectangle_color = image.getpixel((left-2, top-2))

        # 在图像上绘制矩形
        draw.rectangle([(left, top), (right, bottom)], fill=rectangle_color)

        # 选择要绘制的文本和文本颜色
        try:
            text = text_trans_list[i]
        except IndexError:
            image.save('screenshot_text.png')
            return text_todo, text_trans
        box_height = bottom - top if bottom - top > height else height
        if len(text) == 0:
            continue

        pix = int((((right - left) * box_height / len(text)) ** 0.5) * 0.7) 

        
        # 选择一个字体和字号，确保字体包含中文字符
        font = ImageFont.truetype("msyh.ttc", size=pix)
        wrapped_text = return_wrapped_text(
            draw, text, font, (right - left) * 0.9, int((right - left) / pix * 0.8) + 1
        )
        # text_color = (0, 0, 0)  # 黑色
        text_color = get_font_color(rectangle_color)

        # 指定文本的位置
        text_position = (left, top)

        # 在图像上绘制文本
        draw.text(text_position, wrapped_text, fill=text_color, font=font)

        # 保存图像或显示图像
    image.save('screenshot_text.png')
    return text_todo, text_trans
