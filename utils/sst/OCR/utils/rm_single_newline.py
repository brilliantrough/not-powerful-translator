import re

def remove_single_newlines(text):
    # 替换独立的换行符为一个空格，保留连续的换行符
    # 使用负向前瞻和负向后顾来匹配单独的换行符
    return re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

if __name__ == '__main__':
    # 测试字符串
    text = "这是第一行\n这是第二行\n\n这是第四行\n\n\n这是第七行"
    
    # 处理字符串
    processed_text = remove_single_newlines(text)
    
    print(processed_text)
    
