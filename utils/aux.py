"""
Author: pezayo-physical pzyinnju@163.com
Date: 2023-10-12 20:05:49
LastEditors: pezayo-physical pzyinnju@163.com
LastEditTime: 2023-10-26 16:13:37
FilePath: /not-powerful-translator-pyqt5/utils/aux.py
Description: 

Copyright (c) 2023 by pezayo-physical, All Rights Reserved. 
"""
import time
from typing import Any


class Log:
    def __init__(self, path):
        self.path = path
        self.log = open(path, "w")

    def write(self, msg):
        msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + msg + "\n"
        self.log.write(msg)
        self.log.flush()

    def close(self):
        self.log.close()

    def __del__(self):
        self.log.write("closed\n")
        self.close()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.write(*args, **kwds)
