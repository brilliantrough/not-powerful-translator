import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class InfoPopup(QWidget):
    submitted = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enter Info')

        # Create layout
        layout = QVBoxLayout()

        # ID input
        self.idLabel = QLabel('输入 APPID:')
        self.idInput = QLineEdit(self)
        layout.addWidget(self.idLabel)
        layout.addWidget(self.idInput)

        # Key input
        self.keyLabel = QLabel('输入密钥:')
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

    def onSubmit(self):
        id_value = self.idInput.text()
        key_value = self.keyInput.text()
        self.submitted.emit(id_value, key_value)
        self.close()
        # Here you can add code to handle the entered info

    def onCancel(self):
        self.submitted.emit("", "")
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InfoPopup()
    ex.show()
    sys.exit(app.exec_())
