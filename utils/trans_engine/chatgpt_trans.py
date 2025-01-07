"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 18:37:40
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-07-10 20:15:29
FilePath: \not-powerful-translator\chatgpt_trans.py
Description: 定义 ChatGPT 翻译类，其中根据翻译类型定义了两个翻译方法，分别为中文翻译为英文和英文翻译为中文；并以此定义了两个翻译提示。
同时还安排了两种翻译方式，一种是普通的请求方式，一种是流的方式，流的方式可以实现实时翻译，默认使用此方式。

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

import requests
from requests.exceptions import RequestException
import os
import json

prompt_zh2en = "You should act as an English translator, spelling corrector and improver. The user will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. You should only reply the correction, the improvements and nothing else, do not write explanations. Your goal is to ensure that the translation is as smooth and natural as possible, while not changing the meaning of the text."

prompt_en2zh = "You should act as a Chinese translator, spelling corrector and improver. The user will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in Chinese. You should only reply the correction, the improvements and nothing else, do not write explanations. Your goal is to ensure that the translation is as smooth and natural as possible, while not changing the meaning of the text. For certain electronic information and computer-related terminology, such as Transformer, LLM, and some titles, please do not translate."

prompt_sst = """
You need to translate the English I provide you into Chinese. Note that the English translation I provide you is marked with each block separated by carriage returns. Please translate it for me by block, retaining the detailed structure, that is, retaining the original carriage returns.
In addition, some texts are recognized from screenshots, and there will be some recognition errors. For example, the dots in the screenshots are recognized as e, etc. Please distinguish and translate them properly, and still maintain the same structure.
"""


class ChatGPT:
    def __init__(
        self,
        api_base: str = "https://njuapi.pezayo.com/v1",
        api_key: str = "",
        stream_flag: bool = False,
        model: str = "gpt-4o-mini",
    ):
        self.stream_flag = stream_flag
        self.error = ""
        self.retry_nums = 3
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

    def setProxy(
        self, address: str = "127.0.0.1", port: int = 7890, unset: bool = False
    ):
        if unset:
            self.proxies = None
            return
        self.proxies = {
            "https": f"http://{address}:{port}",
            "http": f"http://{address}:{port}",
        }

    def chatgpt(self, prompt: str, text: str, stream: bool = False) -> tuple:
        """翻译文本

        Args:
            prompt (str): 提示 ChatGPT 翻译类型
            text (str): 待翻译文本
            stream (bool, optional): 是否采用流的方式输出翻译结果. Defaults to False.

        Returns:
            tuple: (翻译结果, 状态)
        """
        if stream:
            return self.chatgpt_stream(prompt, text)
        if self.stream_flag:
            return self.chatgpt_stream(prompt, text)
        i = 0
        while i < self.retry_nums:
            try:
                url = f"{self.api_base}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text},
                    ],
                }
                response = requests.post(
                    url,
                    headers=headers,
                    data=json.dumps(data),
                    stream=True,
                    timeout=10,
                    proxies=self.proxies,
                )
                # Parse the JSON content of the response
                response_data = response.json()
                result = response_data["choices"][0]["message"]["content"]
                return result, "成功"
            except Exception as e:
                self.error = str(e)
                print("连接失败，错误信息为 ", e)
                i += 1
        return self.error, "失败"

    def chatgpt_stream(self, prompt: str, text: str) -> tuple:
        """用流的方式进行翻译

        Args:
            prompt (str): 提示 ChatGPT 翻译类型
            text (str): 待翻译文本

        Returns:
            tuple:  (生成器, 状态)
        """
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        print(self.model)
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            "stream": True,
            "temperature": 0.5,
        }

        i = 0
        while i < self.retry_nums:
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(data), stream=True, timeout=10
                )

                # Return a generator that yields each piece of content
                def generator():
                    for line in response.iter_lines():
                        if line:
                            try:
                                line_content_str = line.decode("utf-8").lstrip("data: ")
                                if line_content_str.strip() == "[DONE]":
                                    continue
                                line_content = json.loads(line_content_str)
                                if "choices" in line_content:
                                    content = line_content["choices"][0]["delta"].get(
                                        "content", ""
                                    )
                                    for char in content:
                                        yield char
                            except json.JSONDecodeError:
                                print(
                                    "Received non-JSON response:", line.decode("utf-8")
                                )

                return generator(), "成功"
            except Exception as e:
                self.error = str(e)
                print("连接失败，错误信息为 ", e)
                i += 1
        return self.error, "失败"

    def chatgpt_zh2en(
        self, text: str, stream: bool = False, sst: bool = False
    ) -> tuple:
        return self.chatgpt(prompt_zh2en, text, stream=stream)

    def chatgpt_en2zh(
        self, text: str, stream: bool = False, sst: bool = False
    ) -> tuple:
        return (
            self.chatgpt(prompt_sst, text)
            if sst
            else self.chatgpt(prompt_en2zh, text, stream=stream)
        )

    def en2zh(self, text: str) -> tuple:
        return self.chatgpt_en2zh(text)

    def zh2en(self, text: str) -> tuple:
        return self.chatgpt_zh2en(text)
