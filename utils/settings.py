import os
from utils.trans_engine import Google, DeepL, ChatGPT, Baidu
from typing import Union
ENGINE_TUPLE =  (Google, DeepL, Baidu, ChatGPT)
ARGS_TUPLE = (lambda x: [], lambda x: [], lambda x: [Settings.BAIDU_APP_ID, Settings.BAIDU_API_KEY], lambda x: [Settings.OPENAI_API_BASE, Settings.OPENAI_API_KEY, Settings.STREAM])

class Engine:
    GOOGLE = 0
    DEEPL = 1
    BAIDU = 2
    OPENAI = 3

class Settings:
    OPENAI_API_KEY = ""
    OPENAI_API_BASE = ""
    BAIDU_APP_ID = ""
    BAIDU_API_KEY = ""
    PROXY = ""
    STREAM = True
    PROXY_ADDRESS = ""
    PROXY_PORT = 0
    
def setProxy(engine: Union[Google, DeepL, ChatGPT]):
    """设置代理，如果 address 和 port 为空，则取消代理，可能会默认使用系统代理

    Args:
        engine (Union[Google, DeepL, ChatGPT]): 翻译引擎
        address (str): 代理地址
        port (int): 代理端口
    """
    if Settings.PROXY_ADDRESS and Settings.PROXY_PORT:
        engine.setProxy(address=Settings.PROXY_ADDRESS, port=Settings.PROXY_PORT)
    else:
        engine.setProxy(unset=True)