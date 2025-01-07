"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 00:09:28
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-06-30 22:05:09
FilePath: \googletranslate\translate_ui\mainwindow.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved.  """

import re
import sys
import warnings
from collections.abc import Iterable
from types import MethodType

sys.path.append(".")

import json
import os
import time

# to import Union
from time import sleep

from PyQt5.QtCore import (
    QObject,
    QPoint,
    QSize,
    Qt,
    QThread,
    QUrl,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import (
    QCursor,
    QDesktopServices,
    QFocusEvent,
    QFont,
    QHideEvent,
    QIcon,
    QKeyEvent,
    QShowEvent,
    QTextBlockFormat,
    QTextCursor,
    QTextFormat,
)
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFontDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
)

import icon_rc
from getinfo import InfoPopup
from mainwindow_ui import Ui_MainWindow
from menu.settings_manager import SettingsManager
from menu.settings_window import SettingsWindow
from mouse_listen import MouseListener
from utils.func import clickFunc
from utils.settings import (
    ARGS_TUPLE,
    ENGINE_NAME_DICT,
    ENGINE_TUPLE,
    Engine,
    GlobalConditionVariables,
    RuntimeSettings,
    Settings,
    WindowSettings,
    get_MOUSE_LISTEN_KEEP_GOING,
    set_MOUSE_LISTEN_KEEP_GOING,
    setProxy,
)
from utils.sst import ScreenCaptureTool
from utils.trans_engine import Baidu, ChatGPT, DeepL, Google
from widget.customButton import CustomButton


def check_ip(string: str = None) -> bool:
    """判断是否为 ip 地址加端口号的形式

    Args:
        string (str): 待测代理地址

    Returns:
        bool: 返回真或假
    """
    pattern = r"(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|localhost):([0-9]+)"
    return re.match(pattern, str(string)) is not None


# import markdown

warnings.filterwarnings("ignore")

version = "3.0.0"
proxies = None
google = Google()
deepl = DeepL()
stream: bool = True
BAIDU = 0
OPENAI = 1
SUCCESS = "成功"
FAILED = "失败"

ABOUT = f"""
<p style='font-family: Arial, Simsun; font-size: 16px'>不太全能的翻译(not powerful translator){version}</p>
<p style='font-family: Arial, Simsun; font-size: 16px'>暂无任何许可证</p>
<p style='font-family: Arial, Simsun; font-size: 16px'>作者：brilliantrough/pezayo</p>
<p style='font-family: Arial, Simsun; font-size: 16px'>速速去github给我点个star吧</p>
"""


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.screenshot = ScreenCaptureTool(self)
        self.clipboard = None
        self.engine = None
        self.zh2en: ZH2EN = None
        self.en2zh: EN2ZH = None
        self.reserve_flag: bool = False
        self.settings_manager = SettingsManager()
        self.initSettings()
        self.initMenu()
        self.initVariables()
        self.initSelectTextThread()
        self.initButtons()
        self.initActions()
        self.initWindows()

        # self.setEN2ZHOnly()

    def initSettings(self):
        self.settings = self.settings_manager.settings
        proxy = self.settings_manager.get_setting("service_settings", "proxy")
        Settings.PROXY = proxy
        if check_ip(proxy):
            self.address = proxy.split(":")[0]
            self.port = int(proxy.split(":")[1])
            Settings.PROXY_ADDRESS, Settings.PROXY_PORT = self.address, self.port
        self.baiduid = self.settings_manager.get_setting(
            "service_settings", "BAIDU_APP_ID", "xxxxxxxx"
        )
        self.baidukey = self.settings_manager.get_setting(
            "service_settings", "BAIDU_KEY", "xxxxxxxx"
        )
        self.openaibase = self.settings_manager.get_setting(
            "service_settings", "OPENAI_API_BASE", "https://api.openai.com/v1"
        )
        self.openaikey = self.settings_manager.get_setting(
            "service_settings", "OPENAI_API_KEY", "sk-xxxxxxx"
        )
        self.proxy = self.settings_manager.get_setting(
            "service_settings", "proxy", "http://localhost:7890"
        )
        self.translation_engine = self.settings_manager.get_setting(
            "service_settings", "translation_engine", "Google"
        )
        self.updateServiceSettings()
        self.setFocusPolicy(Qt.ClickFocus)

        self.setWindowTitle("not-powerful-translator")

    def saveSettings(self):
        self.settings_manager.save_settings()

    def initVariables(self):
        self.settings: dict = {}
        self.baiduid: str = ""
        self.baidukey: str = ""
        self.stream_flag = True
        self.en2zh = EN2ZH(self)
        self.zh2en = ZH2EN(self)
        self.engine: int = Engine.GOOGLE
        self.clipboard = QApplication.clipboard()
        self.address: str = ""
        self.port: int = 7890
        self.cursorEN = self.outputEN.textCursor()
        self.cursorZH = self.outputZH.textCursor()
        self.focused_flag: bool = False

    def initActions(self):
        self.copyZHBtn.clicked.connect(self.copyZH)
        self.actionChatGPT_Stream.triggered.connect(self.setChatGPTStream)
        self.actionProxy.triggered.connect(self.setProxy)
        self.actionCheck_Proxy.triggered.connect(self.checkProxy)
        self.actionAbout.triggered.connect(self.aboutPopup)
        self.actionManual.triggered.connect(self.openManual)
        self.actionFontZH.triggered.connect(self.setFontZH)
        self.actionFontEN.triggered.connect(self.setFontEN)
        self.actionModify_Baidu_API.triggered.connect(self.modifyBaiduAPI)
        self.actionModify_OpenAI_API.triggered.connect(self.modifyOpenAIAPI)
        self.actionMinimalist_Mode.toggled.connect(self.minimalistMode)
        self.actionCancel_Mouse_Backstage.triggered.connect(self.cancelMouseBackstage)

    def initButtons(self):
        self.inputEN.installEventFilter(self)
        self.inputZH.installEventFilter(self)
        self.exitBtn.clicked.connect(self.close)
        self.onTopCheckBox.stateChanged.connect(self.onTopCheckBoxChanged)
        self.engineBox.currentIndexChanged.connect(self.selectEngine)
        self.modeBox.currentIndexChanged.connect(self.updateWindow)
        self.selectionCheckBox.stateChanged.connect(self.selectionCheckBoxChanged)
        self.screenshotBtn.clicked.connect(self.screenshotTranslate)
        self.hideInputCheckBox.stateChanged.connect(self.updateWindow)
        self.customButton = CustomButton(self, self.selectTextThread.mouseListener)
        self.customButton.onClick = MethodType(clickFunc, self.customButton)
        self.customButton.clicked.connect(self.customButton.onClick)

    def initWindows(self):
        self.setWindowTitle("not-powerful-translator")
        self.setIcon(":/candy.ico")
        self.updateWindowSettings()
        self.updateRuntimeSettings()

    # record the window size when the window is resized
    def resizeEvent(self, event):
        self.width = self.size().width()
        self.height = self.size().height()
        self.settings_manager.set_setting("window_settings", "width", self.width)
        self.settings_manager.set_setting("window_settings", "height", self.height)
        super().resizeEvent(event)

    def selectEngine(self):
        if self.engineBox.currentIndex() == 0:
            self.setGoogleEngine()
            self.settings_manager.set_setting(
                "service_settings", "translation_engine", "Google"
            )
        elif self.engineBox.currentIndex() == 1:
            self.setDeepLEngine()
            self.settings_manager.set_setting(
                "service_settings", "translation_engine", "DeepL"
            )
        elif self.engineBox.currentIndex() == 2:
            self.setBaiduEngine()
            self.settings_manager.set_setting(
                "service_settings", "translation_engine", "Baidu"
            )
        else:
            self.setChatGPTEngine()
            self.settings_manager.set_setting(
                "service_settings", "translation_engine", "ChatGPT"
            )

    def updateWindow(self):
        if self.modeBox.currentIndex() == 0:
            self.statusEN.show()
            self.statusZH.hide()
            self.outputZH.show()
            self.outputEN.hide()
            self.inputZH.hide()
            (
                self.inputEN.show()
                if not self.hideInputCheckBox.isChecked()
                else self.inputEN.hide()
            )

        elif self.modeBox.currentIndex() == 1:
            self.statusEN.hide()
            self.statusZH.show()
            self.outputZH.hide()
            self.outputEN.show()
            self.inputEN.hide()
            (
                self.inputZH.show()
                if not self.hideInputCheckBox.isChecked()
                else self.inputZH.hide()
            )
        else:
            self.statusEN.show()
            self.outputZH.show()
            self.outputEN.show()
            if not self.hideInputCheckBox.isChecked():
                self.inputZH.show()
                self.inputEN.show()
            else:
                self.inputZH.hide()
                self.inputEN.hide()

    def initSelectTextThread(self):
        self.selectTextThread = SelectTextThread(self)
        self.selectTextThread.select_finished.connect(self.translateSelectedText)
        self.selectTextThread.start()

    def endSelectTextThread(self):
        print("endSelectTextThread")
        self.selectTextThread.quit()
        self.selectTextThread.wait()

    def setIcon(self, icon_path: str) -> None:
        """用来设置窗口图标的函数

        Args:
            icon_path (str): 图标的 qrc 路径
        """
        icon = QIcon()
        icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

    def zh2enTranslate(self):
        self.statusZH.setText("正在翻译...")
        self.outputEN.setText("")
        self.setCursorFormat(self.cursorEN)
        self.zh2en.translate(self.engine, self.inputZH.toPlainText())

    def en2zhTranslate(self):
        self.statusEN.setText("正在翻译...")
        self.outputZH.setText("")
        self.setCursorFormat(self.cursorZH)
        self.en2zh.translate(self.engine, self.inputEN.toPlainText())

    def translateAll(self):
        self.zh2enTranslate()
        self.en2zhTranslate()

    def translateSelectedText(self, text):
        self.inputEN.setPlainText(text)
        self.en2zhTranslate()

    def setGoogleEngine(self):
        self.engine = Engine.GOOGLE
        self.screenshot.engine = Engine.GOOGLE

    def setDeepLEngine(self):
        self.engine = Engine.DEEPL
        self.screenshot.engine = Engine.DEEPL

    def setBaiduEngine(self):
        self.engine = Engine.BAIDU
        self.screenshot.engine = Engine.BAIDU
        if not (self.baidukey and self.baiduid):
            self.modifyBaiduAPI()

    def setChatGPTEngine(self):
        self.engine = Engine.OPENAI
        self.screenshot.engine = Engine.OPENAI
        if not self.openaikey:
            self.modifyOpenAIAPI()

    @pyqtSlot(str, str, int)
    def getIdKey(self, base_or_id: str, api_key: str, api_class: int):
        if api_class == BAIDU:
            self.getBaiduIdKey(baidu_id=base_or_id, baidu_key=api_key)
        elif api_class == OPENAI:
            self.getOpenAIAPI(api_base=base_or_id, api_key=api_key)

    def getOpenAIAPI(self, api_base, api_key):
        if not api_key:
            self.engineBox.setCurrentIndex(0)
            self.engine = Engine.GOOGLE
            self.screenshot.engine = Engine.GOOGLE
            del self.popup
            return
        self.openaibase, self.openaikey = api_base, api_key
        Settings.OPENAI_API_BASE, Settings.OPENAI_API_KEY = api_base, api_key
        self.settings["OPENAI_API_BASE"] = api_base
        self.settings["OPENAI_API_KEY"] = api_key
        # self.saveSettings()
        del self.popup
        self.selectTextThread.resume()

    def getBaiduIdKey(self, baidu_id: str, baidu_key: str):
        if not (baidu_id and baidu_key):
            self.engineBox.setCurrentIndex(0)
            self.engine = Engine.GOOGLE
            self.screenshot.engine = Engine.GOOGLE
            del self.popup
            return
        self.baiduid, self.baidukey = baidu_id, baidu_key
        Settings.BAIDU_APP_ID, Settings.BAIDU_API_KEY = baidu_id, baidu_key
        self.settings["BAIDU_APP_ID"] = baidu_id
        self.settings["BAIDU_KEY"] = baidu_key
        # self.saveSettings()
        del self.popup
        self.selectTextThread.resume()

    @pyqtSlot()
    def modifyBaiduAPI(self):
        self.modifyAPIGeneral(BAIDU)

    @pyqtSlot()
    def modifyOpenAIAPI(self):
        self.modifyAPIGeneral(OPENAI)

    def modifyAPIGeneral(self, api_class: int):
        self.selectTextThread.pause()
        self.popup = InfoPopup(api_class=api_class)
        self.popup.submitted.connect(self.getIdKey)
        self.popup.show()

    @pyqtSlot(str, str)
    def getOutputZH(self, result: str, status: str):
        self.cursorZH.insertText(result)
        self.statusEN.setText(status)

    @pyqtSlot(str, str)
    def getOutputEN(self, result: str, status: str):
        self.cursorEN.insertText(result)
        self.statusZH.setText(status)
        self.autoCopyEN()

    def onTopCheckBoxChanged(self):
        if self.onTopCheckBox.isChecked():
            WindowSettings.ALWAYS_ON_TOP = True
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.settings_manager.set_setting("window_settings", "always_on_top", True)
            time.sleep(0.2)  # NOTE: must set in Linux or the window will not be on top
            self.show()
        else:
            WindowSettings.ALWAYS_ON_TOP = False
            self.setWindowFlags(Qt.Widget)
            self.show()
            self.settings_manager.set_setting("window_settings", "always_on_top", False)
        # self.settings_manager.save_settings()

    def hideInputCheckBoxChanged(self):
        if self.hideInputCheckBox.isChecked():
            self.inputEN.hide()
            self.inputZH.hide()
            self.settings_manager.set_setting("window_settings", "hide_input", True)
        else:
            self.inputZH.show()
            self.inputEN.show()
            self.settings_manager.set_setting("window_settings", "hide_input", False)
        # self.settings_manager.save_settings()

    def selectionCheckBoxChanged(self):
        RuntimeSettings.USE_SELECT_TEXT = self.selectionCheckBox.isChecked()
        self.settings_manager.set_setting(
            "runtime_settings", "use_select_text", RuntimeSettings.USE_SELECT_TEXT
        )
        if RuntimeSettings.USE_SELECT_TEXT:
            self.selectTextThread.resume()
        else:
            self.selectTextThread.pause()

    def autoCopyEN(self):
        if self.actionAuto_Copy_EN.isChecked():
            self.copyEN()

    def copyZH(self):
        self.clipboard.setText(self.outputZH.toPlainText())

    def copyEN(self):
        self.clipboard.setText(self.outputEN.toPlainText())

    def setCursorFormat(self, cursor):
        cursor.movePosition(QTextCursor.Start)
        block_format = QTextBlockFormat()
        block_format.setLineHeight(
            150, QTextBlockFormat.ProportionalHeight
        )  # Set line height
        cursor.setBlockFormat(block_format)

    def setChatGPTStream(self):
        global stream
        stream = self.actionChatGPT_Stream.isChecked()
        self.stream_flag = stream

    def setProxy(self):
        proxy, ok = QInputDialog.getText(
            self,
            "设置代理",
            "<font><span style='font-family: Simsun; font-size: 16px'>请输入代理地址，例如：127.0.0.1:7890</span>",
        )
        proxy = str(proxy)
        if ok and check_ip(proxy):
            self.settings_manager.set_setting("service_settings", "proxy", proxy)
            self.address = proxy.split(":")[0]
            self.port = int(proxy.split(":")[1])
            Settings.PROXY, Settings.PROXY_ADDRESS, Settings.PROXY_PORT = (
                proxy,
                self.address,
                self.port,
            )
            # self.saveSettings()
            self.msgBox(
                "设置代理", "代理成功设置为：http://" + proxy, QMessageBox.Information
            )
        elif ok:
            self.msgBox(
                "设置代理",
                "代理不合法，设置失败：http://" + proxy,
                QMessageBox.Information,
            )

    def msgBox(self, title, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setFont(QFont("Simsun", 13))
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setIcon(icon)
        msg_box.exec()

    def checkProxy(self):
        proxy = self.settings_manager.get_setting(
            "service_settings", "proxy", "http://localhost:7890"
        )
        self.msgBox(
            "检查代理",
            "当前代理为：" + (proxy if check_ip(proxy) else "使用系统代理"),
            QMessageBox.Information,
        )

    def aboutPopup(self):
        QMessageBox.about(self, "关于", ABOUT)

    def openManual(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/brilliantrough/not-powerful-translator")
        )

    def minimalistMode(self):
        WindowSettings.SIMPLE_MODE = self.actionMinimalist_Mode.isChecked()
        self.settings_manager.set_setting(
            "window_settings", "simple_mode", WindowSettings.SIMPLE_MODE
        )
        if WindowSettings.SIMPLE_MODE:
            self.display_widget.hide()
            self.func_widget.hide()
        else:
            self.display_widget.show()
            self.func_widget.show()

    def setFontZH(self):
        """set font of each text edit"""
        font, ok = QFontDialog.getFont(self)
        if ok:
            self.inputZH.setFont(font)
            self.outputZH.setFont(font)

    def setFontEN(self):
        """set font of each text edit"""
        ok, font = QFontDialog.getFont(self)
        if ok:
            self.inputEN.setFont(font)
            self.outputEN.setFont(font)

    def setEN2ZHOnly(self):
        self.outputZH.show()
        self.inputEN.show()
        self.outputEN.hide()
        self.inputZH.hide()

    def screenshotTranslate(self):
        """截图翻译"""
        if RuntimeSettings.AUTO_HIDE:
            self.auto_hide_flag = True
            RuntimeSettings.AUTO_HIDE = False
        self.showMinimized()
        time.sleep(0.5)
        print("screenshotTranslate")
        self.screenshot.show()
        # self.show()

    @pyqtSlot()
    def sst_finished_slot(self):
        self.inputEN.setPlainText(self.screenshot.text_todo)
        self.outputZH.setPlainText(self.screenshot.text_trans)
        self.statusEN.setText("截图翻译完成")
        RuntimeSettings.AUTO_HIDE = self.auto_hide_flag

    @pyqtSlot()
    def sst_begin_slot(self):
        self.statusEN.setText("正在截图翻译...")
        if self.isMinimized() or self.isHidden():
            self.showNormal()

    def eventFilter(self, obj, event):
        """重写事件过滤器，用来实现 shift+enter 换行，enter 翻译

        Args:
            obj (QWidget):  事件发生的对象
            event (QEvent): 发生的事件

        Returns:
            bool:  是否拦截事件
        """
        if event.type() == 17 or event.type() == 18:
            return False
        if (
            event.type() == QKeyEvent.KeyPress
            and event.key() == Qt.Key_Space
            and event.modifiers() == (Qt.ShiftModifier)
        ):
            RuntimeSettings.USE_SELECT_TEXT = not RuntimeSettings.USE_SELECT_TEXT
            self.selectionCheckBox.setChecked(RuntimeSettings.USE_SELECT_TEXT)
            return True
        if obj == self.inputZH or obj == self.inputEN:
            if (
                event.type() == QKeyEvent.KeyPress
                and event.key() == Qt.Key_Return
                and event.modifiers() == Qt.ShiftModifier
            ):
                obj.insertPlainText("\n")
                return True
            elif event.type() == QKeyEvent.KeyPress and event.key() == Qt.Key_Return:
                if obj == self.inputZH:
                    self.zh2enTranslate()
                    self.clearFocus()
                else:
                    self.en2zhTranslate()
                    self.clearFocus()
                return True
        return False

    def focusInEvent(self, event: QFocusEvent):
        self.focused_flag = True

    def focusOutEvent(self, event: QFocusEvent):
        self.focused_flag = False

    def autoHideEvent(self, x, y):
        if RuntimeSettings.AUTO_HIDE:
            if not self.frameGeometry().contains(QPoint(x, y)):
                self.showMinimized()

    def hideEvent(self, event: QHideEvent) -> None:
        if RuntimeSettings.CANCEL_MOUSE_BACKSTAGE:
            self.selectTextThread.pause()
        super().hideEvent(event)

    def showEvent(self, event: QShowEvent) -> None:
        if RuntimeSettings.CANCEL_MOUSE_BACKSTAGE:
            self.selectTextThread.resume()
        super().showEvent(event)

    def closeEvent(self, event) -> None:
        self.statusEN.setText("正在关闭...")
        self.statusZH.setText("正在关闭...")
        # 强制更新 UI
        QApplication.processEvents()

        self.settings_manager.save_settings()
        print("closeEvent")
        self.endSelectTextThread()
        self.zh2en.thread.quit()
        self.en2zh.thread.quit()
        self.screenshot.close()
        super().closeEvent(event)

    def initMenu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Menu")
        font = QFont()
        font.setFamily("SimSun")
        font.setPointSize(11)

        open_settings_action = QAction("打开统一设置菜单", self)
        open_settings_action.setFont(font)
        open_settings_action.triggered.connect(self.openSettingsWindow)
        settings_menu.addAction(open_settings_action)

    def cancelMouseBackstage(self):
        RuntimeSettings.CANCEL_MOUSE_BACKSTAGE = (
            self.actionCancel_Mouse_Backstage.isChecked()
        )

    def openSettingsWindow(self):
        self.settings_window = SettingsWindow(self.settings_manager)
        self.settings_window.settings_applied.connect(self.onSettingsChanged)
        self.settings_window.show()

    @pyqtSlot()
    def onSettingsChanged(self):
        """Handle settings changes."""
        self.updateWindowSettings()
        self.updateRuntimeSettings()
        self.updateServiceSettings()
        self.releaseConditionVariables()
        # 焦点回到主窗口
        self.setFocus()
        if self.isMinimized() or self.isHidden():
            self.showNormal()

    def releaseConditionVariables(self):
        set_MOUSE_LISTEN_KEEP_GOING(False)
        with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
            GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.notify_all()
        with GlobalConditionVariables.CV_MOUSE_LISTEN:
            GlobalConditionVariables.CV_MOUSE_LISTEN.notify_all()

    def updateWindowSettings(self):
        """Update window settings from the settings manager."""
        WindowSettings.WIDTH = self.settings_manager.get_setting(
            "window_settings", "width", WindowSettings.WIDTH
        )
        WindowSettings.HEIGHT = self.settings_manager.get_setting(
            "window_settings", "height", WindowSettings.HEIGHT
        )
        WindowSettings.ALWAYS_ON_TOP = self.settings_manager.get_setting(
            "window_settings", "always_on_top", WindowSettings.ALWAYS_ON_TOP
        )
        WindowSettings.HIDE_INPUT = self.settings_manager.get_setting(
            "window_settings", "hide_input", WindowSettings.HIDE_INPUT
        )
        WindowSettings.HIDE_OUTPUT = self.settings_manager.get_setting(
            "window_settings", "hide_output", WindowSettings.HIDE_OUTPUT
        )
        WindowSettings.SIMPLE_MODE = self.settings_manager.get_setting(
            "window_settings", "simple_mode", WindowSettings.SIMPLE_MODE
        )
        self.resize(WindowSettings.WIDTH, WindowSettings.HEIGHT)
        self.actionMinimalist_Mode.setChecked(WindowSettings.SIMPLE_MODE)
        self.onTopCheckBox.setChecked(WindowSettings.ALWAYS_ON_TOP)
        self.hideInputCheckBox.setChecked(WindowSettings.HIDE_INPUT)
        self.copyZHBtn.hide()
        self.exitBtn.hide()
        self.engineBox.setCurrentIndex(
            ENGINE_NAME_DICT[
                self.settings_manager.get_setting(
                    "service_settings", "translation_engine"
                )
            ]
        )
        self.selectEngine()
        self.show()

    def updateRuntimeSettings(self):
        RuntimeSettings.USE_SELECT_TEXT = self.settings_manager.get_setting(
            "runtime_settings", "use_select_text"
        )
        RuntimeSettings.USE_MOUSE_LISTEN = self.settings_manager.get_setting(
            "runtime_settings", "use_mouse_listen"
        )
        RuntimeSettings.USE_BUTTON = self.settings_manager.get_setting(
            "runtime_settings", "use_button"
        )
        RuntimeSettings.USE_HOTKEY = self.settings_manager.get_setting(
            "runtime_settings", "use_hotkey"
        )
        RuntimeSettings.AUTO_HIDE = self.settings_manager.get_setting(
            "runtime_settings", "auto_hide"
        )
        RuntimeSettings.CANCEL_MOUSE_BACKSTAGE = self.settings_manager.get_setting(
            "runtime_settings", "cancel_mouse_backstage"
        )
        self.auto_hide_flag = RuntimeSettings.AUTO_HIDE
        self.selectionCheckBox.setChecked(RuntimeSettings.USE_SELECT_TEXT)
        self.actionCancel_Mouse_Backstage.setChecked(
            RuntimeSettings.CANCEL_MOUSE_BACKSTAGE
        )

    def updateServiceSettings(self):
        Settings.OPENAI_MODEL = self.settings_manager.get_setting(
            "service_settings", "OPENAI_MODEL"
        )
        Settings.OPENAI_API_KEY = self.settings_manager.get_setting(
            "service_settings", "OPENAI_API_KEY"
        )
        Settings.OPENAI_API_BASE = self.settings_manager.get_setting(
            "service_settings", "OPENAI_API_BASE"
        )
        Settings.BAIDU_APP_ID = self.settings_manager.get_setting(
            "service_settings", "BAIDU_APP_ID"
        )
        Settings.BAIDU_KEY = self.settings_manager.get_setting(
            "service_settings", "BAIDU_KEY"
        )
        Settings.PROXY = self.settings_manager.get_setting("service_settings", "proxy")

    def moveToMousePosition(self):
        """Move the window to the current mouse position and show it."""
        pos = QCursor.pos()
        self.move(pos.x(), pos.y())
        self.showNormal()  # Restore the window if it is minimized


window: MainWindow = None


class ZH2ENThread(QObject):
    # Define a new pyqtSignal called 'task' that takes no parameters.
    task = pyqtSignal(int, str)
    translate_finished = pyqtSignal(str, str)

    @pyqtSlot(int, str)
    def do_work(self, engine: int, text: str):
        global window, stream
        temp_engine = ENGINE_TUPLE[engine](*ARGS_TUPLE[engine](0))
        setProxy(temp_engine)
        result, status = temp_engine.zh2en(text)
        if not isinstance(result, Iterable):
            self.translate_finished.emit("", status)
            return
        if isinstance(result, str):
            self.translate_finished.emit(result, status)
            return
        if engine == Engine.OPENAI and stream:
            for content in result:
                self.translate_finished.emit(content, status)


class ZH2EN(QObject):
    def __init__(self, parent):
        # Create a QThread object.
        self.thread = QThread()
        self.worker = ZH2ENThread()
        self.worker.moveToThread(self.thread)

        self.worker.task.connect(self.worker.do_work)
        self.worker.translate_finished.connect(parent.getOutputEN)

        # Start the thread.
        self.thread.start()

    def translate(self, engine: int, text: str):
        self.worker.task.emit(engine, text)


class EN2ZHThread(QObject):
    # Define a new pyqtSignal called 'task' that takes no parameters.
    task = pyqtSignal(int, str)
    translate_finished = pyqtSignal(str, str)

    @pyqtSlot(int, str)
    def do_work(self, engine: int, text: str):
        global window, stream
        temp_engine = ENGINE_TUPLE[engine](*ARGS_TUPLE[engine](0))
        print(Settings.OPENAI_MODEL)
        setProxy(temp_engine)
        result, status = temp_engine.en2zh(text)
        if not isinstance(result, Iterable):
            self.translate_finished.emit("", status)
            return
        if isinstance(result, str):
            self.translate_finished.emit(result, status)
            return
        if engine == Engine.OPENAI and stream:
            for content in result:
                self.translate_finished.emit(content, status)


class EN2ZH(QObject):
    def __init__(self, parent):
        # Create a QThread object.
        self.thread = QThread()
        self.worker = EN2ZHThread()
        self.worker.moveToThread(self.thread)

        self.worker.task.connect(self.worker.do_work)
        self.worker.translate_finished.connect(parent.getOutputZH)

        # Start the thread.
        self.thread.start()

    def translate(self, engine: int, text: str):
        self.worker.task.emit(engine, text)


class SelectTextThread(QThread):
    select_finished = pyqtSignal(str)
    triggerHotkey = pyqtSignal()

    def __init__(self, parent=None):
        super(SelectTextThread, self).__init__(parent)
        self.parent = parent
        self.mouseListener = MouseListener()
        self.mouseListener.selectText.connect(self.selectTextFinished)
        self.mouseListener.triggerHotkey.connect(self.moveToMousePosition)
        self.mouseListener.popButton.connect(self.moveToMousePositionByMouse)
        self.mouseListener.clickAutoHide.connect(self.parent.autoHideEvent)

    def selectTextFinished(self, text):
        if RuntimeSettings.USE_SELECT_TEXT:
            self.select_finished.emit(text)

    def moveToMousePosition(self):
        # self.parent.customButton.moveToMousePosition()
        with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
            GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.notify_all()
        if RuntimeSettings.USE_MOUSE_LISTEN and RuntimeSettings.USE_SELECT_TEXT:
            if self.parent.isMinimized() or self.parent.isHidden():
                time.sleep(0.2)
                self.parent.moveToMousePosition()

    def moveToMousePositionByMouse(self):
        self.parent.customButton.moveToMousePosition()

    def run(self):
        self.mouseListener.start()

    def pause(self):
        RuntimeSettings.USE_MOUSE_LISTEN = False

    def resume(self):
        RuntimeSettings.USE_MOUSE_LISTEN = True

    def quit(self):
        print("selectTextThread quit")
        self.mouseListener.quit()
        super().quit()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
