"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 00:09:28
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-06-30 22:05:09
FilePath: \googletranslate\translate_ui\mainwindow.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

import re
import warnings

from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize, QUrl
from PyQt5.QtGui import (
    QKeyEvent,
    QIcon,
    QHideEvent,
    QShowEvent,
    QDesktopServices,
    QFont,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QMessageBox,
    QFontDialog,
)
from form_ui import Ui_MainWindow
from mouse_listen import MouseListener
from utils import ScreenCaptureTool, Google, DeepL, ChatGPT
import icon_rc

# to import Union
from typing import Union
from time import sleep


def check_ip(string: str) -> bool:
    """判断是否为 ip 地址加端口号的形式

    Args:
        string (str): 待测代理地址

    Returns:
        bool: 返回真或假
    """
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$"
    return re.match(pattern, string) is not None


# import markdown

warnings.filterwarnings("ignore")

version = "1.2.1"
proxies = None
google = Google()
deepl = DeepL()
stream: bool = True

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
        self.reserve_flag = False
        self.initVariables()
        self.initButtons()
        self.initActions()
        self.initWindows()
        self.initSelectTextThread()
        self.setEN2ZHOnly()

    def initVariables(self):
        self.en2zh = EN2ZH(self)
        self.zh2en = ZH2EN(self)
        self.engine: str = "google"
        self.clipboard = QApplication.clipboard()
        self.address: str = ""
        self.port: int = 7890
        self.cursorEN = self.outputEN.textCursor()
        self.cursorZH = self.outputZH.textCursor()

    def initActions(self):
        self.actionCopyZH.triggered.connect(self.copyZH)
        self.actionChatGPT_Stream.triggered.connect(self.setChatGPTStream)
        self.actionClose_Mouse_Selection.triggered.connect(self.closeMouseSelection)
        self.actionProxy.triggered.connect(self.setProxy)
        self.actionCheck_Proxy.triggered.connect(self.checkProxy)
        self.actionAbout.triggered.connect(self.aboutPopup)
        self.actionManual.triggered.connect(self.openManual)
        self.actionClose_Mouse_Selection.toggled.connect(self.closeMouseSelection)
        self.actionEN2ZH_only.triggered.connect(self.setEN2ZHOnly)
        self.actionZH2EN_only.triggered.connect(self.setZH2ENOnly)
        self.actionFontZH.triggered.connect(self.setFontZH)
        self.actionFontEN.triggered.connect(self.setFontEN)

    def initButtons(self):
        self.inputEN.installEventFilter(self)
        self.inputZH.installEventFilter(self)
        self.googleBtn.setEnabled(False)
        self.googleBtn.clicked.connect(self.setGoogleEngine)
        self.deeplBtn.clicked.connect(self.setDeepLEngine)
        self.chatgptBtn.clicked.connect(self.setChatGPTEngine)
        self.exitBtn.clicked.connect(self.close)
        self.zhBtn.clicked.connect(self.zh2enTranslate)
        self.enBtn.clicked.connect(self.en2zhTranslate)
        self.onTopCheckBox.stateChanged.connect(self.onTopCheckBoxChanged)
        self.engineBox.currentIndexChanged.connect(self.selectEngine)
        self.screenshotBtn.clicked.connect(self.screenshotTranslate)
        self.hideButtons()
        # self.allBtn.clicked.connect(self.translateAll)
        

    def initWindows(self):
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)  # make the window on the top
        self.setWindowTitle("不太全能的翻译-pezayo")
        self.setIcon(":/candy.ico")
        self.resize(900, 400)
        
        
    def selectEngine(self):
        if self.engineBox.currentIndex() == 0:
            self.setGoogleEngine()
        elif self.engineBox.currentIndex() == 1:
            self.setDeepLEngine()
        else:
            self.setChatGPTEngine()

    def initSelectTextThread(self):
        self.selectTextThread = SelectTextThread()
        self.selectTextThread.select_finished.connect(self.translateSelectedText)
        self.selectTextThread.start()

    def endSelectTextThread(self):
        self.selectTextThread.quit()
        self.selectTextThread.wait()
        
    def hideButtons(self):
        self.googleBtn.hide()
        self.deeplBtn.hide()
        self.chatgptBtn.hide()
        self.zhBtn.hide()
        self.enBtn.hide()

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
        self.googleBtn.setEnabled(False)
        self.deeplBtn.setEnabled(True)
        self.chatgptBtn.setEnabled(True)
        self.engine = "google"
        screenshot.engine = "google"

    def setDeepLEngine(self):
        self.deeplBtn.setEnabled(False)
        self.googleBtn.setEnabled(True)
        self.chatgptBtn.setEnabled(True)
        self.engine = "deepl"
        screenshot.engine = "deepl"

    def setChatGPTEngine(self):
        self.chatgptBtn.setEnabled(False)
        self.deeplBtn.setEnabled(True)
        self.googleBtn.setEnabled(True)
        self.engine = "chatgpt"
        screenshot.engine = "chatgpt"

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
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.Widget)
            self.show()

    def autoCopyEN(self):
        if self.actionAuto_Copy_EN.isChecked():
            self.copyEN()

    def copyZH(self):
        self.clipboard.setText(self.outputZH.toPlainText())

    def copyEN(self):
        self.clipboard.setText(self.outputEN.toPlainText())

    def closeMouseSelection(self):
        self.selectTextThread.setFlag(not self.actionClose_Mouse_Selection.isChecked())
        if self.selectTextThread.flag:
            self.selectTextThread.resume()
        else:
            self.selectTextThread.pause()
            
    def setCursorFormat(self, cursor):
        cursor.movePosition(QTextCursor.Start)
        block_format = QTextBlockFormat()
        block_format.setLineHeight(150, QTextBlockFormat.ProportionalHeight)  # Set line height
        cursor.setBlockFormat(block_format)


    def setChatGPTStream(self):
        global stream
        stream = self.actionChatGPT_Stream.isChecked()

    def setProxy(self):
        proxy, ok = QInputDialog.getText(
            self,
            "设置代理",
            "<font><span style='font-family: Simsun; font-size: 16px'>请输入代理地址，例如：127.0.0.1:7890</span>",
        )
        proxy = str(proxy)
        global proxies
        if ok and check_ip(proxy):
            proxies = {"http": "http://" + proxy, "https": "https://" + proxy}
            # QMessageBox.information(self, "设置代理", "代理成功设置为：http://" + proxy)
            self.address = proxy.split(":")[0]
            self.port = int(proxy.split(":")[1])
            self.msgBox("设置代理", "代理成功设置为：http://" + proxy, QMessageBox.Information)
        else:
            pass

    def msgBox(self, title, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setFont(QFont("Simsun", 13))
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setIcon(icon)
        msg_box.exec()

    def checkProxy(self):
        self.msgBox(
            "检查代理",
            "当前代理为：" + (proxies["http"] if proxies else "使用系统代理"),
            QMessageBox.Information,
        )

    def aboutPopup(self):
        # self.msgBox("关于", ABOUT, QIcon(":/icon/candy.ico"))
        QMessageBox.about(self, "关于", ABOUT)

    def openManual(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/brilliantrough/not-powerful-translator")
        )

    def setFontZH(self):
        """set font of each text edit"""
        ok, font = QFontDialog.getFont(self)
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
        print("emit en2zh")
        if self.actionEN2ZH_only.isChecked():
            self.outputZH.show()
            self.inputEN.show()
            self.outputEN.hide()
            self.inputZH.hide()
            if self.actionZH2EN_only.isChecked():
                self.actionZH2EN_only.setChecked(False)
        else:
            self.outputZH.show()
            self.inputEN.show()
            self.outputEN.show()
            self.inputZH.show()

    def setZH2ENOnly(self):
        print("emit zh2en")
        if self.actionZH2EN_only.isChecked():
            self.outputZH.hide()
            self.inputEN.hide()
            self.outputEN.show()
            self.inputZH.show()
            if self.actionEN2ZH_only.isChecked():
                self.actionEN2ZH_only.setChecked(False)
        else:
            self.outputZH.show()
            self.inputEN.show()
            self.outputEN.show()
            self.inputZH.show()
            
    def screenshotTranslate(self):
        """截图翻译
        """
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
        if (
            event.type() == QKeyEvent.KeyPress
            and event.key() == Qt.Key_Space
            and event.modifiers() == (Qt.ShiftModifier)
        ):
            self.actionClose_Mouse_Selection.trigger()
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
            not self.actionClose_Mouse_Selection.isChecked()
            and self.actionCancel_Mouse_Backstage.isChecked()
        ):
            self.actionClose_Mouse_Selection.trigger()
            self.reserve_flag = True
        super().hideEvent(event)

    def showEvent(self, event: QShowEvent) -> None:
        if self.reserve_flag and self.actionCancel_Mouse_Backstage.isChecked():
            self.actionClose_Mouse_Selection.trigger()
            self.reserve_flag = False
        super().showEvent(event)

    def closeEvent(self, event) -> None:
        self.endSelectTextThread()
        self.zh2en.thread.quit()
        self.en2zh.thread.quit()
        screenshot.close()
        super().closeEvent(event)


def set_proxy(engine: Union[Google, DeepL, ChatGPT], address: str, port: int):
    """设置代理，如果 address 和 port 为空，则取消代理，可能会默认使用系统代理

    Args:
        engine (Union[Google, DeepL, ChatGPT]): 翻译引擎
        address (str): 代理地址
        port (int): 代理端口
    """
    if address and port:
        engine.setProxy(address=address, port=port)
    else:
        engine.setProxy(unset=True)


class ZH2ENThread(QObject):
    # Define a new signal called 'task' that takes no parameters.
    task = pyqtSignal(str, str)
    translate_finished = pyqtSignal(str, str)

    @pyqtSlot(str, str)
    def do_work(self, engine: str, text):
        if engine == "google":
            tempgoogle = Google()
            set_proxy(tempgoogle, window.address, window.port)
            print("the address is ", tempgoogle.proxies)
            result, status = tempgoogle.google_zh2en(text)
            self.translate_finished.emit(result, status)
        elif engine == "deepl":
            tempdeepl = DeepL()
            set_proxy(tempdeepl, window.address, window.port)
            result, status = tempdeepl.deepL_zh2en(text)
            self.translate_finished.emit(result, status)
        else:
            tempchatgpt = ChatGPT()
            set_proxy(tempchatgpt, window.address, window.port)
            global stream
            result, status = tempchatgpt.chatgpt_zh2en(text, stream=stream)
            if stream:
                for i in result:
                    try:
                        self.translate_finished.emit(
                            i.choices[0]["delta"]["content"], status
                        )
                    except Exception:
                        return
            else:
                self.translate_finished.emit(result, status)


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

    def translate(self, engine: str, text: str):
        self.worker.task.emit(engine, text)


class EN2ZHThread(QObject):
    # Define a new signal called 'task' that takes no parameters.
    task = pyqtSignal(str, str)
    translate_finished = pyqtSignal(str, str)

    @pyqtSlot(str, str)
    def do_work(self, engine: str, text: str):
        if engine == "google":
            tempgoogle = Google()
            set_proxy(tempgoogle, window.address, window.port)
            result, status = tempgoogle.google_en2zh(text)
            self.translate_finished.emit(result, status)
        elif engine == "deepl":
            tempdeepl = DeepL()
            set_proxy(tempdeepl, window.address, window.port)
            result, status = tempdeepl.deepL_en2zh(text)
            self.translate_finished.emit(result, status)
        else:
            tempchatgpt = ChatGPT()
            set_proxy(tempchatgpt, window.address, window.port)
            global stream
            result, status = tempchatgpt.chatgpt_en2zh(text, stream=stream)
            if stream:
                for i in result:
                    try:
                        self.translate_finished.emit(
                            i.choices[0]["delta"]["content"], status
                        )
                    except Exception:
                        return
            else:
                self.translate_finished.emit(result, status)


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

    def translate(self, engine: str, text: str):
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


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    screenshot = ScreenCaptureTool(window)
    window.show()
    app.exec()
