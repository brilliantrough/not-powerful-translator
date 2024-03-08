import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import icon_rc

API_CLASS: list = [["输入 APPID:", "输入密钥:"], ["输入 OPENAI_API_BASE:","输入 OPENAI_API_KEY:"]]

class InfoPopup(QWidget):
    submitted = pyqtSignal(str, str, int)
    def __init__(self, api_class: int):
        super().__init__()
        self.api_class = api_class
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enter Info')

        # Create layout
        layout = QVBoxLayout()

        # ID input
        self.idLabel = QLabel(API_CLASS[self.api_class][0])
        self.idInput = QLineEdit(self)
        layout.addWidget(self.idLabel)
        layout.addWidget(self.idInput)

        # Key input
        self.keyLabel = QLabel(API_CLASS[self.api_class][1])
        self.keyInput = QLineEdit(self)
        layout.addWidget(self.keyLabel)
        layout.addWidget(self.keyInput)

        # Submit button
        sublayout = QHBoxLayout()
        self.submitBtn = QPushButton('Submit', self)
        self.submitBtn.clicked.connect(self.onSubmit)
        sublayout.addWidget(self.submitBtn)
        self.cancelBtn = QPushButton('Cancel', self)
        self.cancelBtn.clicked.connect(self.onCancel)
        sublayout.addWidget(self.cancelBtn)
        layout.addLayout(sublayout)
        self.setLayout(layout)
        self.setWindowIcon(QIcon(":/candy.ico"))
        self.setFixedSize(400, 300)

    def onSubmit(self):
        id_value = self.idInput.text()
        key_value = self.keyInput.text()
        self.submitted.emit(id_value, key_value, self.api_class)
        self.close()
        # Here you can add code to handle the entered info

    def onCancel(self):
        self.submitted.emit("", "", self.api_class)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InfoPopup()
    ex.show()
    sys.exit(app.exec_())
