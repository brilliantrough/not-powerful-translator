"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-28 22:24:30
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2024-03-08 16:04:08
Description: 定义了 Google 翻译类，其中定义了翻译方法 google，以及设置代理方法 setProxy。

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

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


class Google:
    time: float = 0.0

    def __init__(self, proxies: dict = None) -> None:
        self.proxies = proxies
        self.params = {
            "client": "gtx",
            "sl": "en",
            "tl": "zh-CN",
            "dt": "t",
            "q": "",
        }
        self.url = "https://translate.googleapis.com/translate_a/single"
        self.retry_nums = 3

    def setProxy(
        self, address: str = "127.0.0.1", port: int = 7890, unset: bool = False
    ) -> None:
        if unset:
            self.proxies = None
            return
        self.proxies = {
            "https": f"http://{address}:{port}",
            "http": f"http://{address}:{port}",
        }

    @Timer
    def google(self, text: str, src: str = "en", dst: str = "zh-CN") -> tuple:
        """调用 google 翻译接口翻译文本，返回翻译后的文本。

        Args:
            text (str): 待翻译的文本
            src (str, optional): 待翻译文本的语言，默认为 'en'.
            dst (str, optional): 目标语言，默认为 'zh-CN'.

        Returns:
            tuple: 翻译后的文本以及状态信息
        """
        self.params["sl"] = src
        self.params["tl"] = dst
        self.params["q"] = text
        kw = {
            "url": self.url,
            "params": self.params,
            "proxies": self.proxies,
            "timeout": 10,
        }
        i = 0
        response: requests.Response = None
        while i < self.retry_nums:
            try:
                response = requests.get(**kw)
                if response.status_code == 200:
                    result = response.json()[0]
                    if not isinstance(result, list):
                        break
                    translated_text = "".join([i[0] for i in result])
                    return translated_text, "成功"
                else:
                    # print("连接失败，状态码为", response.status_code)
                    i += 1
            except RequestException as e:
                # print("连接失败，错误信息为 ", e)
                i += 1
        return None, f"失败 {response.status_code if response else '未知'}"

    def google_zh2en(self, text: str) -> tuple:
        return self.google(text, src="zh-CN", dst="en")

    def google_en2zh(self, text: str) -> tuple:
        return self.google(text, src="en", dst="zh-CN")
    
    def en2zh(self, text: str) -> tuple:
        return self.google_en2zh(text)

    def zh2en(self, text: str) -> tuple:
        return self.google_zh2en(text)
