"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 03:20:09
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-06-29 04:12:17
FilePath: \googletranslate\translate_ui\mouse_listen.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

from pyperclip import copy, paste
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController
from pynput import mouse
import time
from threading import Condition
import os
from utils import Log

from PySide6.QtCore import Signal, QThread

# create a condition variable for the main thread to wait for the mouse release event
cv = Condition()

keyboard = Controller()  # create a keyboard controller
mouse1 = MouseController()  # create a mouse controller
TIME_TO_WAIT = 0.4  # the time to wait for the mouse release event
t = time.time()  # the time when the mouse is pressed
last_selected_text = ""  # the last selected text, initialized to empty
original_text = ""  # the original text, initialized to empty
translate_num = 1  # the number of the translation, initialized to 1


def on_click(x, y, button, pressed):
    """the click event handler, with the press and release event

    Args:
        x (int): the position of the mouse on the x axis, do not use
        y (int): the position of the mouse on the y axis, do not use
        button (Button): which button is pressed
        pressed (bool): whether the button is pressed or released
    """
    global t
    if pressed and button == mouse.Button.left:
        t = time.time()
        # print('press on {0} at {1}'.format(x, y))
    elif not pressed and button == mouse.Button.left:
        # print('release on {0} at {1}'.format(x, y))
        time_margin = time.time() - t
        # print("the time margin is", time_margin)
        if time_margin > TIME_TO_WAIT:
            with cv:
                cv.notify_all()


class MouseListener(QThread):
    selectText = Signal(str)

    def __init__(self):
        super(MouseListener, self).__init__()
        self.listener = mouse.Listener(on_click=on_click)
        self.running: bool = True
        self.stop: bool = False
        self.log = Log("log.txt")

    def run(self):
        """the main thread, to translate the selected text

        * the original text will be restored
        * the selected text will be copied to the clipboard
        * the translated text will be printed to the console
        * the original text will be copied to the clipboard
        * if the selected text is the same as the last selected text, the translation will be skipped
        * if the selected text is empty, the translation will be skipped
        * if the selected text is the same as the original text, the translation will be skipped
        * if the translation failed up to 3 times, the translation will be skipped
        """
        global original_text, translate_num, last_selected_text
        self.listener.start()  # start the mouse listener
        while True:
            if not self.running:
                time.sleep(1)
                continue
            with cv:
                cv.wait()
            if self.stop:
                break
            original_text = paste()
            keyboard.press(Key.ctrl)
            keyboard.press(Key.insert)
            keyboard.release(Key.insert)
            keyboard.release(Key.ctrl)  # copy the selected text
            time.sleep(0.2)  # wait for the text to be copied
            selected_text = paste()
            # restore the original text
            copy(original_text)

            if (
                selected_text == last_selected_text
                or selected_text == ""
                or selected_text == original_text
            ):
                continue
            # print("the selected text is", selected_text)
            self.selectText.emit(selected_text)
            last_selected_text = selected_text  # update the last selected text
            translate_num += 1  # update the number of the translation

    def pause(self):
        """pause the mouse listener"""
        mouse.Listener.stop(self.listener)
        mouse.Listener.join(self.listener)
        self.listener = None

    def resume(self):
        """resume the mouse listener"""
        self.listener = mouse.Listener(on_click=on_click)
        self.listener.start()

    def quit(self):
        """exit the mouse listener"""
        if self.listener is not None:
            mouse.Listener.stop(self.listener)
            mouse.Listener.join(self.listener)
        self.stop = True
        del self.log
        with cv:
            cv.notify_all()
        # time.sleep(0.1)
        super().quit()
