import sys
from threading import Condition
from typing import Union

from utils.trans_engine import Baidu, ChatGPT, DeepL, Google

ENGINE_TUPLE = (Google, DeepL, Baidu, ChatGPT)
ARGS_TUPLE = (
    lambda x: [],
    lambda x: [],
    lambda x: [Settings.BAIDU_APP_ID, Settings.BAIDU_API_KEY],
    lambda x: [
        Settings.OPENAI_API_BASE,
        Settings.OPENAI_API_KEY,
        Settings.STREAM,
        Settings.OPENAI_MODEL,
    ],
)
FONT_SST = "simsun.ttc" if sys.platform == "win32" else "NotoSansCJK-Regular.ttc"


class Engine:
    GOOGLE = 0
    DEEPL = 1
    BAIDU = 2
    OPENAI = 3


ENGINE_NAME_DICT = {
    "Google": Engine.GOOGLE,
    "DeepL": Engine.DEEPL,
    "Baidu": Engine.BAIDU,
    "ChatGPT": Engine.OPENAI,
}


class RuntimeSettings:
    AUTO_HIDE = False
    CANCEL_MOUSE_BACKSTAGE = False
    USE_SELECT_TEXT = False
    USE_MOUSE_LISTEN = False
    USE_BUTTON = True
    USE_HOTKEY = True


class WindowSettings:
    WIDTH = 677
    HEIGHT = 408
    ALWAYS_ON_TOP = True
    HIDE_INPUT = True
    HIDE_OUTPUT = True
    SIMPLE_MODE = True


class Settings:
    OPENAI_API_KEY = ""
    OPENAI_API_BASE = ""
    BAIDU_APP_ID = ""
    BAIDU_API_KEY = ""
    PROXY = ""
    STREAM = True
    PROXY_ADDRESS = ""
    PROXY_PORT = 0
    OPENAI_MODEL = "gpt-4o-mini"


class MutableSharedSettings:
    POP_BUTTON = False
    MOUSE_LISTEN_KEEP_GOING = False


class GlobalConditionVariables:
    CV_MOUSE_LISTEN = Condition()
    CV_BUTTON_KEY_LISTEN = Condition()


def set_MOUSE_LISTEN_KEEP_GOING(value: bool):
    MutableSharedSettings.MOUSE_LISTEN_KEEP_GOING = value


def get_MOUSE_LISTEN_KEEP_GOING():
    return MutableSharedSettings.MOUSE_LISTEN_KEEP_GOING


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
