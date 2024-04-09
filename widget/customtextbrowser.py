from PyQt5.QtWidgets import QTextBrowser, QPushButton
from PyQt5.QtGui import QIcon

class CustomTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super(CustomTextBrowser, self).__init__(parent)
        self.copyButton = QPushButton(self)
        self.copyButton.setStyleSheet("QPushButton {\nimage: url(:/copy.svg);\n}\n\nQPushButton:hover {\nbackground-color: rgb(115,210,22);\n}")
        self.copyButton.clicked.connect(self.copyText)
        self.copyButton.hide()  # Initially hide the button

    def enterEvent(self, event):
        self.copyButton.move(self.width() - self.copyButton.width(), 0)
        self.copyButton.show()
        super(CustomTextBrowser, self).enterEvent(event)

    def leaveEvent(self, event):
        self.copyButton.hide()
        super(CustomTextBrowser, self).leaveEvent(event)

    def resizeEvent(self, event):
        self.copyButton.move(self.width() - self.copyButton.width(), 0)
        super(CustomTextBrowser, self).resizeEvent(event)

    def copyText(self):
        self.selectAll()
        self.copy()
        self.moveCursor(self.textCursor().End)

