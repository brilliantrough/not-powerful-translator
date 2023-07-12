"""
Author: brilliantrough pzyinnju@163.com
Date: 2023-06-29 00:09:28
LastEditors: brilliantrough pzyinnju@163.com
LastEditTime: 2023-06-30 22:05:09
FilePath: \googletranslate\translate_ui\mainwindow.py
Description: 

Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
"""

from deepL_trans import DeepL
from google_trans import Google
from chatgpt_trans import ChatGPT
from form_ui import Ui_MainWindow

from PySide6.QtGui import QKeyEvent, QIcon, QHideEvent, QShowEvent
from PySide6.QtCore import Qt, QThread, Signal, Slot, QObject, QSize
from PySide6.QtWidgets import QApplication, QMainWindow
from mouse_listen import MouseListener
import os
import icon_rc
import warnings

warnings.filterwarnings("ignore")

google = Google()
deepl = DeepL()
stream: bool = True


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.clipboard = None
        self.engine = None
        self.zh2en = None
        self.en2zh = None
        self.reserve_flag = False
        self.initVariables()
        self.initButtons()
        self.initActions()
        self.initWindows()
        self.initSelectTextThread()

    def initVariables(self):
        self.en2zh = EN2ZH(self)
        self.zh2en = ZH2EN(self)
        self.engine: str = "google"
        self.clipboard = QApplication.clipboard()

    def initActions(self):
        self.actionCopyZH.triggered.connect(self.copyZH)
        self.actionChatGPT_Stream.triggered.connect(self.setChatGPTStream)
        self.actionClose_Mouse_Selection.triggered.connect(self.closeMouseSelection)

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
        self.allBtn.clicked.connect(self.translateAll)

    def initWindows(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("不太全能的翻译-pezayo")
        self.setIcon(":/icon/candy.ico")

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
        self.zh2en.translate(self.engine, self.inputZH.toPlainText())

    def en2zhTranslate(self):
        self.statusEN.setText("等待...")
        self.outputZH.setText("")
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

    def setDeepLEngine(self):
        self.deeplBtn.setEnabled(False)
        self.googleBtn.setEnabled(True)
        self.chatgptBtn.setEnabled(True)
        self.engine = "deepl"

    def setChatGPTEngine(self):
        self.chatgptBtn.setEnabled(False)
        self.deeplBtn.setEnabled(True)
        self.googleBtn.setEnabled(True)
        self.engine = "chatgpt"

    @Slot(str, str)
    def getOutputZH(self, result: str, status: str):
        self.outputZH.insertPlainText(result)
        self.statusEN.setText(status)

    @Slot(str, str)
    def getOutputEN(self, result: str, status: str):
        self.outputEN.insertPlainText(result)
        self.statusZH.setText(status)
        self.autoCopyEN()

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

    def setChatGPTStream(self):
        global stream
        stream = self.actionChatGPT_Stream.isChecked()

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
        super().closeEvent(event)


class ZH2ENThread(QObject):
    # Define a new signal called 'task' that takes no parameters.
    task = Signal(str, str)
    translate_finished = Signal(str, str)

    @Slot()
    def do_work(self, engine: str, text):
        if engine == "google":
            tempgoogle = Google()
            result, status = tempgoogle.google_zh2en(text)
            self.translate_finished.emit(result, status)
        elif engine == "deepl":
            tempdeepl = DeepL()
            result, status = tempdeepl.deepL_zh2en(text)
            self.translate_finished.emit(result, status)
        else:
            tempchatgpt = ChatGPT()
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
    task = Signal(str, str)
    translate_finished = Signal(str, str)

    @Slot()
    def do_work(self, engine: str, text: str):
        if engine == "google":
            tempgoogle = Google()
            result, status = tempgoogle.google_en2zh(text)
            self.translate_finished.emit(result, status)
        elif engine == "deepl":
            tempdeepl = DeepL()
            result, status = tempdeepl.deepL_en2zh(text)
            self.translate_finished.emit(result, status)
        else:
            tempchatgpt = ChatGPT()
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
    select_finished = Signal(str)

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
    window.show()
    app.exec()
