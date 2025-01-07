from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QTextBrowser


class CustomTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super(CustomTextBrowser, self).__init__(parent)
        self.copyButton = QPushButton(self)
        self.copyButton.setStyleSheet(
            """
            QPushButton {
                image: url(:/copy.svg);
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(115, 210, 22, 0.5);
                border: 1px solid rgb(115, 210, 22);
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgba(80, 160, 17, 0.7);
                border: 1px solid rgb(80, 160, 17);
                border-radius: 5px;
            }
        """
        )
        self.copyButton.setCursor(Qt.PointingHandCursor)
        self.copyButton.clicked.connect(self.copyText)
        self.copyButton.hide()  # Initially hide the button
        # Set scrollbar width
        self.setStyleSheet(
            """
            QScrollBar:vertical {
                width: 10px;
            }
        """
        )

    def enterEvent(self, event):
        self.adjustButtonPosition()
        self.copyButton.show()
        super(CustomTextBrowser, self).enterEvent(event)

    def leaveEvent(self, event):
        self.copyButton.hide()
        super(CustomTextBrowser, self).leaveEvent(event)

    def resizeEvent(self, event):
        self.adjustButtonPosition()
        super(CustomTextBrowser, self).resizeEvent(event)

    def adjustButtonPosition(self):
        scrollbar_width = 10 if self.verticalScrollBar().isVisible() else 0
        self.copyButton.move(
            self.width() - self.copyButton.width() - scrollbar_width, 0
        )

    def copyText(self):
        self.selectAll()
        self.copy()
        self.moveCursor(self.textCursor().End)
