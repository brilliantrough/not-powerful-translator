'''
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-28 23:04:57
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-07-10 20:14:30
FilePath: \googletranslate\translate_ui\google_trans.py
Description: 定义了 Google 翻译类，其中定义了翻译方法 google，以及设置代理方法 setProxy。

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
'''

import requests
from requests.exceptions import RequestException
import time

def Timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        Google.time = time.time() - start
        print(f"耗时: {Google.time:.3f} 秒")
        return result
    return wrapper

# TODO: 代理设置，是否使用代理，手动设置代理，自动设置代理
class Google():
    time:float = 0.0
    def __init__(self) -> None:
        self.port = 7890
        self.address = "127.0.0.1"
        self.params = {
            "client": "gtx",
            "sl": "en",
            "tl": "zh-CN",
            "dt": "t",
            "q": "",
        }
        self.url = "https://translate.googleapis.com/translate_a/single"
        self.retry_nums = 3
        
    def setProxy(self, address:str = "127.0.0.1", port:int = 7890) -> None:
        self.address = address
        self.port = port
        
        
    @Timer
    def google(self, text:str, src:str = 'en', dst:str = 'zh-CN') -> tuple:
        """调用 google 翻译接口翻译文本，返回翻译后的文本。

        Args:
            text (str): 待翻译的文本
            src (str, optional): 待翻译文本的语言，默认为 'en'.
            dst (str, optional): 目标语言，默认为 'zh-CN'.

        Returns:
            tuple: 翻译后的文本以及状态信息
        """
        self.params['sl'] = src
        self.params['tl'] = dst
        self.params['q'] = text
        proxies = {
            "https": f"http://{self.address}:{self.port}", 
            "http": f"http://{self.address}:{self.port}"
        }
        i = 0
        while i < self.retry_nums:
            try:
                response = requests.get(self.url, params=self.params)
                if response.status_code == 200:
                    result = response.json()[0]
                    translated_text = ''.join([i[0] for i in result])
                    return translated_text, "成功"
                else:
                    print("连接失败，状态码为 ", response.status_code)
                    i += 1
            except RequestException as e:
                print("连接失败，错误信息为 ", e)
                i += 1
        return None, "失败"
    
    
    def google_zh2en(self, text:str) -> tuple:
        return self.google(text, src='zh-CN', dst='en')
    
    def google_en2zh(self, text:str) -> tuple:
        return self.google(text, src='en', dst='zh-CN')