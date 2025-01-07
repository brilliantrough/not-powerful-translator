"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 03:20:09
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-06-29 04:12:17
FilePath: \googletranslate\translate_ui\mouse_listen.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

import os
import sys
import threading
import time

from pynput import mouse
from pynput.keyboard import Controller, GlobalHotKeys, Key, KeyCode
from pyperclip import copy, paste
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QCursor

from utils.mycls import Log
from utils.settings import (
    GlobalConditionVariables,
    MutableSharedSettings,
    RuntimeSettings,
    get_MOUSE_LISTEN_KEEP_GOING,
    set_MOUSE_LISTEN_KEEP_GOING,
)

TIME_TO_WAIT = 0.4  # the time to wait for the mouse release event
t = time.time()  # the time when the mouse is pressed


def on_activate():
    print("Global hotkey activated!")


class MouseListener(QThread):
    selectText = pyqtSignal(str)
    popButton = pyqtSignal()
    triggerHotkey = pyqtSignal()
    clickOutsideButton = pyqtSignal(int, int)  # New signal
    clickAutoHide = pyqtSignal(int, int)

    def __init__(self):
        super(MouseListener, self).__init__()
        self.listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = GlobalHotKeys({"<alt>+q": self.triggerHotkey.emit})
        self.running: bool = True
        self.stop: bool = False
        self.log = Log("log.txt")
        self.triggerTranslate = False
        self.read_text: list[str] = ["", ""]
        self.last_copy_text: str = ""
        self.last_selected_text = ""  # the last selected text, initialized to empty
        self.selected_text = ""  # the selected text, initialized to empty
        self.original_text = ""  # the original text, initialized to empty
        self.translate_num = 1  # the number of the translation, initialized to 1
        self.reserve_text: str = ""
        self.keyboard = Controller()  # create a keyboard controller
        if sys.platform == "win32":
            self.getSelectedText = self.getSelectedTextWin32
        else:
            self.getSelectedText = self.getSelectedTextLinux

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
        self.listener.start()  # start the mouse listener
        self.keyboard_listener.start()  # start the keyboard listener
        self.last_selected_text = (
            "" if sys.platform == "win32" else os.popen("xsel").read()
        )
        while True:
            if not self.running:
                time.sleep(1)
                continue
            with GlobalConditionVariables.CV_MOUSE_LISTEN:
                GlobalConditionVariables.CV_MOUSE_LISTEN.wait()
            if self.stop:
                break

            self.translateHotkeyCondition()
            self.getSelectedText()
            if not self.translateButtonCondition():
                continue
            self.translate()

    def translate(self):
        self.selectText.emit(self.selected_text)
        self.triggerTranslate = False

    def translateHotkeyCondition(self):
        if RuntimeSettings.USE_HOTKEY and not RuntimeSettings.USE_BUTTON:
            print("use hotkey")
            set_MOUSE_LISTEN_KEEP_GOING(True)
            with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
                GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.wait()

    def translateButtonCondition(self):
        if not self.triggerTranslate:
            return False
        if (
            RuntimeSettings.USE_BUTTON
            and not MutableSharedSettings.POP_BUTTON
            # and not get_MOUSE_LISTEN_KEEP_GOING()
        ):
            set_MOUSE_LISTEN_KEEP_GOING(True)
            MutableSharedSettings.POP_BUTTON = True
            self.popButton.emit()
            with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
                GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.wait()
        if not get_MOUSE_LISTEN_KEEP_GOING():
            set_MOUSE_LISTEN_KEEP_GOING(True)
            return False
        return True

    def getSelectedTextLinux(self):
        time.sleep(0.1)
        print("getSelectedTextLinux")
        self.selected_text = os.popen("xsel").read()
        self.read_text[1] = self.selected_text
        if (
            self.selected_text != self.last_selected_text
            and self.selected_text != ""
            and self.selected_text != self.read_text[0]
            and self.selected_text != self.reserve_text
        ):
            self.log.write("xsel: " + self.selected_text)
            self.triggerTranslate = True
            self.last_selected_text = self.selected_text
        else:
            self.original_text = paste()
            self.log.write("orignal_text:\n" + self.original_text)

            # Reset all possible held keys before simulating copy
            self._reset_all_keys()

            self.keyboard.press(Key.ctrl)
            self.keyboard.press(Key.insert)
            time.sleep(0.1)
            self.keyboard.release(Key.insert)
            self.keyboard.release(Key.ctrl)  # copy the selected text
            time.sleep(0.15)  # wait for the text to be copied
            self.selected_text = paste()
            if (
                self.selected_text != self.last_selected_text
                and self.selected_text != ""
                and self.selected_text != self.last_copy_text
                and self.selected_text != self.original_text
            ):
                self.log.write("copied:" + self.selected_text)
                self.triggerTranslate = True
                self.last_copy_text = self.selected_text
            # restore the original text
            copy(self.original_text)
        self.read_text[0] = self.read_text[1]
        self.reserve_text = os.popen("xsel").read()
        self.translate_num += 1  # update the number of the translation

    def getSelectedTextWin32(self):
        self.original_text = paste()

        # Reset all possible held keys before simulating copy
        self._reset_all_keys()

        self.keyboard.press(Key.ctrl)
        self.keyboard.press(Key.insert)
        time.sleep(0.1)
        self.keyboard.release(Key.insert)
        self.keyboard.release(Key.ctrl)  # copy the selected text
        time.sleep(0.3)  # wait for the text to be copied
        self.selected_text = paste()
        # restore the original text
        copy(self.original_text)

        if (
            self.selected_text == self.last_selected_text
            or self.selected_text == ""
            or self.selected_text == self.original_text
        ):
            self.triggerTranslate = False
            self.keyboard.press(Key.ctrl)
            self.keyboard.press("c")
            time.sleep(0.1)
            self.keyboard.release("c")
            self.keyboard.release(Key.ctrl)  # copy the selected text
            time.sleep(0.3)  # wait for the text to be copied
            self.selected_text = paste()
            copy(self.original_text)
            if (
                self.selected_text == self.last_selected_text
                or self.selected_text == ""
                or self.selected_text == self.original_text
            ):
                self.triggerTranslate = False
                return
        self.triggerTranslate = True

    def _reset_all_keys(self):
        """Reset all possible held modifier keys."""
        modifier_keys = [
            Key.alt,
            Key.alt_l,
            Key.alt_r,
            Key.ctrl,
            Key.ctrl_l,
            Key.ctrl_r,
            Key.shift,
            Key.shift_l,
            Key.shift_r,
            Key.cmd,
            Key.cmd_l,
            Key.cmd_r,
        ]

        for key in modifier_keys:
            try:
                self.keyboard.release(key)
            except:
                pass

    def pause(self):
        """pause the mouse listener"""
        RuntimeSettings.USE_SELECT_TEXT = False
        RuntimeSettings.USE_MOUSE_LISTEN = False

    def resume(self):
        """resume the mouse listener"""
        RuntimeSettings.USE_SELECT_TEXT = True
        RuntimeSettings.USE_MOUSE_LISTEN = True

    def quit(self):
        """Exit the mouse listener"""
        print("mouseListener quit")
        set_MOUSE_LISTEN_KEEP_GOING(False)
        self.stop = True

        with GlobalConditionVariables.CV_MOUSE_LISTEN:
            GlobalConditionVariables.CV_MOUSE_LISTEN.notify_all()
        with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
            GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.notify_all()

        print("mouseListener quit 1")
        # Stop the mouse listener
        if self.listener is not None and self.listener.running:
            self.listener.stop()
            try:
                # 创建一个线程来执行join，这样可以避免阻塞
                join_thread = threading.Thread(target=self.listener.join)
                join_thread.daemon = (
                    True  # 设置为守护线程，这样主程序退出时它会自动结束
                )
                join_thread.start()
                join_thread.join(timeout=0.5)  # 等待最多1秒
            except:
                pass  # 忽略任何可能的异常

        print("mouseListener quit 2")

        # Stop the keyboard listener
        if self.keyboard_listener is not None and self.keyboard_listener.running:
            self.keyboard_listener.stop()
            try:
                join_thread = threading.Thread(target=self.keyboard_listener.join)
                join_thread.daemon = True
                join_thread.start()
                join_thread.join(timeout=0.5)
            except:
                pass

        print("mouseListener quit 3")

        super().quit()

    def on_click(self, x, y, button, pressed):
        """the click event handler, with the press and release event

        Args:
            x (int): the position of the mouse on the x axis, do not use
            y (int): the position of the mouse on the y axis, do not use
            button (Button): which button is pressed
            pressed (bool): whether the button is pressed or released
        """
        global t
        if not RuntimeSettings.USE_MOUSE_LISTEN or not RuntimeSettings.USE_SELECT_TEXT:
            return
        if pressed and button == mouse.Button.left:
            t = time.time()
            if MutableSharedSettings.POP_BUTTON:
                self.clickOutsideButton.emit(QCursor.pos().x(), QCursor.pos().y())
            elif RuntimeSettings.USE_HOTKEY:
                set_MOUSE_LISTEN_KEEP_GOING(False)
                with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
                    GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.notify_all()
            if RuntimeSettings.AUTO_HIDE:
                self.clickAutoHide.emit(QCursor.pos().x(), QCursor.pos().y())
        elif not pressed and button == mouse.Button.left:
            time_margin = time.time() - t
            if time_margin > TIME_TO_WAIT:
                with GlobalConditionVariables.CV_MOUSE_LISTEN:
                    GlobalConditionVariables.CV_MOUSE_LISTEN.notify_all()
