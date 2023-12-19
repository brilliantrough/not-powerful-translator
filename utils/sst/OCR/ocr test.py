from PIL import Image
import pytesseract
from utils.rm_single_newline import remove_single_newlines

# 指定tesseract命令行工具的路径
# Windows用户可能需要修改此路径
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 打开图像文件
image = Image.open('screenshot.png')

text = pytesseract.image_to_string(image)
text = remove_single_newlines(text)
# 打印结果
print(text)

print(text)
