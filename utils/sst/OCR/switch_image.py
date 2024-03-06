from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QIcon
import icon_rc


class SwitchImage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_image = 0
        self.image_paths = ["screenshot.png", "screenshot_text.png"]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setWindowIcon(QIcon(":/candy.ico"))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image_label = QLabel(self)
        self.pixmap_tuple = (QPixmap(self.image_paths[0]), QPixmap(self.image_paths[1]))
        self.image_label.setPixmap(self.pixmap_tuple[self.current_image])
        self.layout.addWidget(self.image_label)
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_layout.addItem(spacer)

        self.toggle_button = QPushButton("Toggle", self)
        self.toggle_button.clicked.connect(self.toggle_image)
        self.button_layout.addWidget(self.toggle_button)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

    def toggle_image(self):
        self.current_image = 1 - self.current_image
        self.image_label.setPixmap(self.pixmap_tuple[self.current_image])


def switch_image():
    image_view = SwitchImage()
    image_view.show()
