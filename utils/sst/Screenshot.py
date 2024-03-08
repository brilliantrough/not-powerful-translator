import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QScreen, QPixmap
from PIL import Image
from .OCR import ocr_process, SwitchImage
from utils.settings import  Engine

class ScreenCaptureTool(QWidget):
    """
    A tool for capturing screenshots and performing OCR on the captured image.

    Signals:
        ocr: pyqtSignal(str) - Signal emitted when OCR is performed on the captured image.
        quit_signal: pyqtSignal() - Signal emitted when the tool is closed.

    Methods:
        __init__(self, parent=None) - Initializes the ScreenCaptureTool.
        initUI(self) - Initializes the user interface of the tool.
        show(self) - Shows the tool.
        mousePressEvent(self, event: QMouseEvent) - Handles the mouse press event.
        mouseMoveEvent(self, event: QMouseEvent) - Handles the mouse move event.
        mouseReleaseEvent(self, event: QMouseEvent) - Handles the mouse release event.
        paintEvent(self, event) - Handles the paint event.
        performOCR(self, image_path: str) - Performs OCR on the captured image.

    Attributes:
        parent - The parent widget of the tool.
        originalPixmap - The original screenshot captured by the tool.
        selecting - A flag indicating whether the user is currently selecting an area on the screen.
        origin - The starting point of the selection.
        endPoint - The end point of the selection.
        screenshot - The cropped screenshot image.
    """
    ocr: pyqtSignal = pyqtSignal(str)
    quit_signal: pyqtSignal = pyqtSignal()
    sst_finished: pyqtSignal = pyqtSignal()
    show_image: pyqtSignal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.engine: int = Engine.GOOGLE
        self.text_todo = ""
        self.text_trans = ""
        self.show_image_pool = []
        self.show_image.connect(self.show_result)
        if self.parent:
            self.sst_finished.connect(self.parent.sst_finished_slot)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        self.originalPixmap = QScreen.grabWindow(QApplication.primaryScreen(), 0)
        self.selecting = False
        self.ocr.connect(self.performOCR)
        self.quit_signal.connect(self.close)
        
    def show(self):
        self.originalPixmap = QScreen.grabWindow(QApplication.primaryScreen(), 0)
        super().show()
        

    def mousePressEvent(self, event: QMouseEvent):
        self.origin = event.pos()
        self.selecting = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.selecting:
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.selecting = False
        rect = QRect(self.origin, self.endPoint).normalized()
        self.screenshot = self.originalPixmap.copy(rect)
        self.screenshot.save("screenshot.png")
        self.hide()
        self.ocr.emit("screenshot.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        maskColor = QColor(0, 0, 0, 100)  # 半透明黑色遮罩
        painter.fillRect(self.rect(), maskColor)

        if self.selecting:
            selectedRect = QRect(self.origin, self.endPoint).normalized()
            painter.drawPixmap(selectedRect, self.originalPixmap, selectedRect)

    @pyqtSlot(str)
    def performOCR(self, image_path: str):
        # 将QPixmap转换为PIL Image
        self.text_todo, self.text_trans = ocr_process(image_path, engine=self.engine)
        self.sst_finished.emit()
        self.show_image.emit()
        # switch_image()
        self.hide()
        if self.parent:
            self.parent.showNormal()

    @pyqtSlot()
    def show_result(self):
        self.show_image_pool.append(SwitchImage())
        self.show_image_pool[-1].show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool = ScreenCaptureTool()
    tool.show()
    sys.exit(app.exec())

