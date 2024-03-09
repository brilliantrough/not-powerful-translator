"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 00:09:28
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-06-30 22:05:09
FilePath: \googletranslate\translate_ui\mainwindow.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved.  """

import re
import warnings
from collections.abc import Iterable

from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize, QUrl
from PyQt5.QtGui import QKeyEvent, QIcon, QHideEvent, QShowEvent, QDesktopServices, QFont, QTextBlockFormat, QTextCursor, QTextFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFontDialog

from mainwindow_ui import Ui_MainWindow
from mouse_listen import MouseListener
from utils.settings import Settings, Engine, ENGINE_TUPLE, ARGS_TUPLE, setProxy
from utils.sst import ScreenCaptureTool
from utils.trans_engine import Google, DeepL, ChatGPT, Baidu
import icon_rc

# to import Union
from time import sleep
import json
import os
from getinfo import InfoPopup
import time


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
BAIDU=0
OPENAI=1
SUCCESS="成功"
FAILED="失败"

ABOUT = f"""
<font>
<p style='font-family: Arial, Simsun; font-size: 16px'>不太全能的翻译(not powerful translator){version}</p>
<p style='font-family: Arial, Simsun; font-size: 16px'>暂无任何许可证</p>
<p style='font-family: Arial, Simsun; font-size: 16px'>作者：brilliantrough/pezayo</p>
<p style='font-family: Arial, Simsun; font-size: 16px'>速速去github给我点个star吧</p>
"""


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.clipboard = None
        self.engine = None
        self.zh2en: ZH2EN = None
        self.en2zh: EN2ZH = None
        self.reserve_flag: bool = False
        self.top_flag: bool = False
        self.initVariables()
        self.initButtons()
        self.initActions()
        self.initWindows()
        self.initSelectTextThread()
        self.setEN2ZHOnly()
        self.initSettings()

    def initSettings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", 'r') as file:
                try:
                    self.settings = json.load(file)
                except json.decoder.JSONDecodeError:
                    self.settings = {}                    
                    self.msgBox("设置错误", "配置文件 settings.json 格式错误，所有配置清空\n已将当前文件备份至 settings.json.backup", QMessageBox.Information)
                    os.system("copy settings.json settings.json.backup")
                    self.saveSettings()
        proxy = self.settings.get("proxy", None)
        Settings.PROXY = proxy
        if check_ip(proxy):
            self.address = proxy.split(":")[0]
            self.port = int(proxy.split(":")[1])
            Settings.PROXY_ADDRESS, Settings.PROXY_PORT = self.address, self.port
        self.baiduid = self.settings.get("BAIDU_APP_ID", None) 
        self.baidukey = self.settings.get("BAIDU_KEY", None)
        self.openaibase = self.settings.get("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.openaikey = self.settings.get("OPENAI_API_KEY", "")
        Settings.BAIDU_APP_ID, Settings.BAIDU_API_KEY, Settings.OPENAI_API_BASE, Settings.OPENAI_API_KEY = self.baiduid, self.baidukey, self.openaibase, self.openaikey


    def saveSettings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

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

    def initButtons(self):
        self.inputEN.installEventFilter(self)
        self.inputZH.installEventFilter(self)
        self.exitBtn.clicked.connect(self.close)
        self.onTopCheckBox.stateChanged.connect(self.onTopCheckBoxChanged)
        self.engineBox.currentIndexChanged.connect(self.selectEngine)
        self.modeBox.currentIndexChanged.connect(self.selectMode)
        self.selectionCheckBox.stateChanged.connect(self.selectionCheckBoxChanged)
        self.screenshotBtn.clicked.connect(self.screenshotTranslate)

    def initWindows(self):
        self.setWindowTitle("not-powerful-translator")
        self.setIcon(":/candy.ico")
        self.resize(900, 400)

    def selectEngine(self):
        if self.engineBox.currentIndex() == 0:
            self.setGoogleEngine()
        elif self.engineBox.currentIndex() == 1:
            self.setDeepLEngine()
        elif self.engineBox.currentIndex() == 2:
            self.setBaiduEngine()
        else:
            self.setChatGPTEngine()

    def selectMode(self):
        if self.modeBox.currentIndex() == 0:
            self.outputZH.show()
            self.inputEN.show()
            self.outputEN.hide()
            self.inputZH.hide()

        elif self.modeBox.currentIndex() == 1:
            self.outputZH.hide()
            self.inputEN.hide()
            self.outputEN.show()
            self.inputZH.show()
        else:
            self.outputZH.show()
            self.inputEN.show()
            self.outputEN.show()
            self.inputZH.show()

    def initSelectTextThread(self):
        self.selectTextThread = SelectTextThread()
        self.selectTextThread.select_finished.connect(self.translateSelectedText)
        self.selectTextThread.start()

    def endSelectTextThread(self):
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
        self.statusZH.setText("等待...")
        self.outputEN.setText("")
        self.setCursorFormat(self.cursorEN)
        self.zh2en.translate(self.engine, self.inputZH.toPlainText())

    def en2zhTranslate(self):
        self.statusEN.setText("等待...")
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
        screenshot.engine = Engine.GOOGLE

    def setDeepLEngine(self):
        self.engine = Engine.DEEPL
        screenshot.engine = Engine.DEEPL

    def setBaiduEngine(self):
        self.engine = Engine.BAIDU
        screenshot.engine = Engine.BAIDU
        if not (self.baidukey and self.baiduid):
            self.modifyBaiduAPI()
            
    def setChatGPTEngine(self):
        self.engine = Engine.OPENAI
        screenshot.engine = Engine.OPENAI
        if not self.openaikey:
            self.modifyOpenAIAPI()
            
    @pyqtSlot(str, str, int)
    def getIdKey(self, base_or_id: str, api_key: str, api_class:int):
        if api_class == BAIDU:
            self.getBaiduIdKey(baidu_id=base_or_id, baidu_key=api_key)
        elif api_class == OPENAI:
            self.getOpenAIAPI(api_base=base_or_id, api_key=api_key)
            
    def getOpenAIAPI(self, api_base, api_key):
        if not api_key:
            self.engineBox.setCurrentIndex(0)
            self.engine = Engine.GOOGLE
            screenshot.engine = Engine.GOOGLE
            del self.popup
            return
        self.openaibase, self.openaikey = api_base, api_key
        Settings.OPENAI_API_BASE, Settings.OPENAI_API_KEY = api_base, api_key
        self.settings["OPENAI_API_BASE"] = api_base
        self.settings["OPENAI_API_KEY"] = api_key
        self.saveSettings()
        del self.popup
        self.selectTextThread.resume()
    
    def getBaiduIdKey(self, baidu_id:str, baidu_key: str):
        if not (baidu_id and baidu_key):
            self.engineBox.setCurrentIndex(0)
            self.engine = Engine.GOOGLE
            screenshot.engine = Engine.GOOGLE
            del self.popup
            return
        self.baiduid, self.baidukey = baidu_id, baidu_key
        Settings.BAIDU_APP_ID, Settings.BAIDU_API_KEY = baidu_id, baidu_key
        self.settings["BAIDU_APP_ID"] = baidu_id
        self.settings["BAIDU_KEY"] = baidu_key
        self.saveSettings()
        del self.popup
        self.selectTextThread.resume()

    @pyqtSlot()
    def modifyBaiduAPI(self):
        self.modifyAPIGeneral(BAIDU)
        
    @pyqtSlot()
    def modifyOpenAIAPI(self):
        self.modifyAPIGeneral(OPENAI)
        
    def modifyAPIGeneral(self, api_class:int):
        self.selectTextThread.pause()
        self.popup = InfoPopup(api_class=api_class)
        self.popup.submitted.connect(self.getIdKey)
        self.popup.show()

    @pyqtSlot(str, str)
    def getOutputZH(self, result: str, status: str):
        # self.outputZH.insertPlainText(result)
        self.cursorZH.insertText(result)
        self.statusEN.setText(status)

    @pyqtSlot(str, str)
    def getOutputEN(self, result: str, status: str):
        # self.outputEN.insertPlainText(result)
        self.cursorEN.insertText(result)
        # self.outputEN.insertHtml(markdown.markdown(result))
        self.statusZH.setText(status)
        self.autoCopyEN()

    def onTopCheckBoxChanged(self):
        if self.onTopCheckBox.isChecked():
            self.top_flag = True
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            time.sleep(0.2)  # NOTE: must set in Linux or the window will not be on top
            self.show()
        else:
            self.top_flag = True
            self.setWindowFlags(Qt.Widget)
            self.show()
    
    def selectionCheckBoxChanged(self):
        self.selectTextThread.setFlag(self.selectionCheckBox.isChecked())
        if self.selectionCheckBox.isChecked():
            self.selectTextThread.resume()
        else:
            self.selectTextThread.pause()

    def selectionCheckBoxChanged(self):
        self.selectTextThread.setFlag(self.selectionCheckBox.isChecked())
        if self.selectionCheckBox.isChecked():
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
            self.settings["proxy"] = proxy
            # QMessageBox.information(self, "设置代理", "代理成功设置为：http://" + proxy)
            self.address = proxy.split(":")[0]
            self.port = int(proxy.split(":")[1])
            Settings.PROXY, Settings.PROXY_ADDRESS, Settings.PROXY_PORT = proxy, self.address, self.port
            self.saveSettings()
            self.msgBox("设置代理", "代理成功设置为：http://" + proxy, QMessageBox.Information)
        elif ok:
            self.msgBox("设置代理", "代理不合法，设置失败：http://" + proxy, QMessageBox.Information)
        
    def msgBox(self, title, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setFont(QFont("Simsun", 13))
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setIcon(icon)
        msg_box.exec()

    def checkProxy(self):
        proxy = self.settings.get("proxy", "")
        self.msgBox("检查代理", "当前代理为：" + (proxy if check_ip(proxy) else "使用系统代理"), QMessageBox.Information)

    def aboutPopup(self):
        # self.msgBox("关于", ABOUT, QIcon(":/icon/candy.ico"))
        QMessageBox.about(self, "关于", ABOUT)

    def openManual(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/brilliantrough/not-powerful-translator")
        )

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
        self.showMinimized()
        # print("screenshot")
        sleep(0.5)
        screenshot.show()
        # self.show()

    @pyqtSlot()
    def sst_finished_slot(self):
        self.inputEN.setPlainText(screenshot.text_todo)
        self.outputZH.setPlainText(screenshot.text_trans)

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
            self.selectionCheckBox.setChecked(not self.selectionCheckBox.isChecked())
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

    def hideEvent(self, event: QHideEvent) -> None:
        if (
            self.selectionCheckBox.isChecked()
            and self.actionCancel_Mouse_Backstage.isChecked()
            and not self.top_flag
        ):
            self.selectTextThread.pause()
            self.reserve_flag = True
        super().hideEvent(event)

    def showEvent(self, event: QShowEvent) -> None:
        if self.top_flag:
            self.top_flag = False
        elif self.reserve_flag and self.actionCancel_Mouse_Backstage.isChecked():
            self.selectTextThread.resume()
            self.reserve_flag = False
        super().showEvent(event)

    def closeEvent(self, event) -> None:
        self.endSelectTextThread()
        self.zh2en.thread.quit()
        self.en2zh.thread.quit()
        screenshot.close()
        super().closeEvent(event)


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
            for i in result:
                try:
                    self.translate_finished.emit(
                        i.choices[0]["delta"]["content"], status
                    )
                except Exception:
                    return

    
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
        setProxy(temp_engine)
        result, status = temp_engine.en2zh(text)
        if not isinstance(result, Iterable):
            self.translate_finished.emit("", status)
            return
        if isinstance(result, str):
            self.translate_finished.emit(result, status)
            return
        if engine == Engine.OPENAI and stream:
            for i in result:
                try:
                    self.translate_finished.emit(
                        i.choices[0]["delta"]["content"], status
                    )
                except Exception:
                    return

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

    def __init__(self, parent=None):
        super(SelectTextThread, self).__init__(parent)
        self.mouseListener = MouseListener()
        self.flag = True
        self.mouseListener.selectText.connect(self.selectTextFinished)

    def setFlag(self, flag):
        self.flag = flag

    def selectTextFinished(self, text):
        if self.flag:
            self.select_finished.emit(text)

    def run(self):
        self.mouseListener.start()

    def pause(self):
        self.mouseListener.pause()

    def resume(self):
        self.mouseListener.resume()

    def quit(self):
        self.mouseListener.quit()
        super().quit()


def main():
    global screenshot, window
    app = QApplication([])
    window = MainWindow()
    screenshot = ScreenCaptureTool(window)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
