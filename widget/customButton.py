from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton

import icon_rc
from utils.settings import (
    GlobalConditionVariables,
    MutableSharedSettings,
    set_MOUSE_LISTEN_KEEP_GOING,
)


class CustomButton(QPushButton):
    def __init__(self, parent, mouse_listener):
        super().__init__()
        self.parent = parent

        # Connect the signal from MouseListener
        mouse_listener.clickOutsideButton.connect(self.handleFocusLoss)

        # 设置无边框和总是在最前
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置窗口透明属性
        self.setAttribute(Qt.WA_TranslucentBackground)  # 添加这行来设置窗口透明
        # 设置按钮样式
        self.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;  /* 透明背景 */
                border: none;  /* 无边框 */
                border-radius: 20px;  /* 圆形按钮 */
            }
            QPushButton:hover {
                background-color: rgba(224, 234, 252, 0.5);  /* 悬停时半透明背景 */
            }
            QPushButton:pressed {
                background-color: rgba(212, 252, 121, 0.5);  /* 按下时半透明背景 */
            }
            """
        )

        # 设置按钮大小
        self.setFixedSize(40, 40)  # 确保按钮是圆形
        self.setCursor(Qt.PointingHandCursor)

        # 设置按钮图标
        self.setIcon(QIcon(":/candy.ico"))
        self.setIconSize(QSize(30, 30))

    def moveToMousePosition(self):
        pos = QCursor.pos()
        self.move(pos.x(), pos.y())
        self.showNormal()  # Restore the window if it is minimized

    def onClick(self):
        self.hide()

    def handleFocusLoss(self, x, y):
        # Logic to handle focus loss
        if not self.frameGeometry().contains(QPoint(x, y)):
            # print("handleFocusLoss", self.pos(), self.size(), x, y)
            self.hide()
            set_MOUSE_LISTEN_KEEP_GOING(False)
            with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
                GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.notify_all()
            MutableSharedSettings.POP_BUTTON = False
