"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-28 21:54:34
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-07-10 20:13:54
FilePath: \googletranslate\translate_ui\deepL_trans.py
Description: 定义了 DeepL 翻译类，其中定义了翻译方法 deepL，以及设置代理方法 setProxy。

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

import requests
from requests.exceptions import RequestException
import time
from random import randrange

def calculate_valid_timestamp(timestamp, i_count):
    try:
        return timestamp + (i_count - timestamp % i_count)
    except ZeroDivisionError:
        return timestamp
    
    
def generate_timestamp(sentences):
    now = int(time.time() * 1000)
    i_count = 1
    for sentence in sentences:
        i_count += sentence.count("i")

    return calculate_valid_timestamp(now, i_count)

def generate_id():
    return randrange(1_000_000, 100_000_000)



def Timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        DeepL.time = time.time() - start
        print(f"耗时: {DeepL.time:.3f} 秒")
        return result

    return wrapper

MAGIC_NUMBER = int("CAFEBABE", 16)


# BUG: 这里存在一些问题，通过模拟浏览器请求有时无法成功，甚至可能会导致自己当前的浏览器无法访问 deepL 网站
# NOTE: 这里会使用到 deepL 的 jsonrpc 接口，但是这个接口是通过浏览器访问的，所以需要模拟浏览器请求。同时也会消耗 DeepL 的免费额度。
class DeepL:
    time: float = 0.0

    def __init__(self) -> None:
        self.proxies: dict = None
        self.retry_nums = 3

    def setProxy(self, address: str = "127.0.0.1", port: int = 7890, unset: bool = False) -> None:
        if unset:
            self.proxies = None
            return
        self.proxies = {"http": f"http://{address}:{port}", "https": f"http://{address}:{port}"}

    @Timer
    def deepL(self, text: str, src: str = "ZH", dst: str = "EN") -> tuple:
        """使用 deepL 翻译文本

        Args:
            text (str): 待翻译的文本
            src (str, optional): 待翻译文本语言，默认为 'ZH'
            dst (str, optional): 目标语言，默认为 'EN'

        Returns:
            tuple: 翻译后的文本以及状态信息
        """
        url = "https://www2.deepl.com/jsonrpc"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
            "Referer": "https://www.deepl.com/translator",
        }

        data = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": [
                    {
                        "kind": "default",
                        "raw_en_sentence": text,
                        "raw_en_context_before": [],
                        "raw_en_context_after": [],
                        "quality": "fast",
                    }
                ],
                "lang": {
                    "user_preferred_langs": ["EN", "ZH"],
                    "source_lang_user_selected": src,
                    "target_lang": dst,
                },
                "priority": 1,
                "commonJobParams": {},
                "timestamp": generate_timestamp(text),
            },
            "id": generate_id(),
        }

        i = 0
        response: requests.Response = None
        while i < self.retry_nums:
            try:
                response = requests.post(
                    url, headers=headers, proxies=self.proxies, json=data
                )

                if response.status_code == 200:
                    translated_text = response.json()["result"]["translations"][0][
                        "beams"
                    ][0]["postprocessed_sentence"]
                    # print("Translated text:", translated_text)
                    return translated_text, "成功"
                elif response.status_code == 429:
                    return None, "请求过于频繁"
                else:
                    # print("连接失败，状态码为:", response.status_code)
                    i += 1
            except RequestException as e:
                # print(f"连接失败，错误信息为  {e}")
                i += 1
        return None, f"失败 {response.status_code if response else '未知'}"

    def deepL_zh2en(self, text: str) -> tuple:
        """调用 deepL 将中文翻译为英文

        Args:
            text (str): 待翻译的文本

        Returns:
            str: 翻译后的文本
        """
        return self.deepL(text, "ZH", "EN")

    def deepL_en2zh(self, text: str) -> tuple:
        """调用 deepL 将英文翻译为中文

        Args:
            text (str): 待翻译的文本

        Returns:
            str: 翻译后的文本
        """
        return self.deepL(text, "EN", "ZH")
