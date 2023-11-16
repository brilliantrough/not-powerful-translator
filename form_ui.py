# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QTextBrowser, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 400)
        MainWindow.setStyleSheet(u"")
        self.actionCopyZH = QAction(MainWindow)
        self.actionCopyZH.setObjectName(u"actionCopyZH")
        self.actionAuto_Copy_EN = QAction(MainWindow)
        self.actionAuto_Copy_EN.setObjectName(u"actionAuto_Copy_EN")
        self.actionAuto_Copy_EN.setCheckable(True)
        self.actionAuto_Copy_EN.setChecked(True)
        self.actionClose_Mouse_Selection = QAction(MainWindow)
        self.actionClose_Mouse_Selection.setObjectName(u"actionClose_Mouse_Selection")
        self.actionClose_Mouse_Selection.setCheckable(True)
        self.actionChatGPT_Stream = QAction(MainWindow)
        self.actionChatGPT_Stream.setObjectName(u"actionChatGPT_Stream")
        self.actionChatGPT_Stream.setCheckable(True)
        self.actionChatGPT_Stream.setChecked(True)
        self.actionCancel_Mouse_Backstage = QAction(MainWindow)
        self.actionCancel_Mouse_Backstage.setObjectName(u"actionCancel_Mouse_Backstage")
        self.actionCancel_Mouse_Backstage.setCheckable(True)
        self.actionCancel_Mouse_Backstage.setChecked(True)
        self.actionZH2EN_only = QAction(MainWindow)
        self.actionZH2EN_only.setObjectName(u"actionZH2EN_only")
        self.actionZH2EN_only.setCheckable(True)
        self.actionEN2ZH_only = QAction(MainWindow)
        self.actionEN2ZH_only.setObjectName(u"actionEN2ZH_only")
        self.actionEN2ZH_only.setCheckable(True)
        self.actionEN2ZH_only.setChecked(True)
        self.actionBoth = QAction(MainWindow)
        self.actionBoth.setObjectName(u"actionBoth")
        self.actionBoth.setCheckable(True)
        self.actionProxy = QAction(MainWindow)
        self.actionProxy.setObjectName(u"actionProxy")
        self.actionJust_ZH = QAction(MainWindow)
        self.actionJust_ZH.setObjectName(u"actionJust_ZH")
        self.actionJust_EN = QAction(MainWindow)
        self.actionJust_EN.setObjectName(u"actionJust_EN")
        self.actionRestore = QAction(MainWindow)
        self.actionRestore.setObjectName(u"actionRestore")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionManual = QAction(MainWindow)
        self.actionManual.setObjectName(u"actionManual")
        self.actionCheck_Proxy = QAction(MainWindow)
        self.actionCheck_Proxy.setObjectName(u"actionCheck_Proxy")
        self.actionFontZH = QAction(MainWindow)
        self.actionFontZH.setObjectName(u"actionFontZH")
        self.actionFontEN = QAction(MainWindow)
        self.actionFontEN.setObjectName(u"actionFontEN")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 40))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.onTopCheckBox = QCheckBox(self.widget)
        self.onTopCheckBox.setObjectName(u"onTopCheckBox")
        font = QFont()
        font.setFamilies([u"\u9ed1\u4f53"])
        font.setPointSize(10)
        self.onTopCheckBox.setFont(font)

        self.horizontalLayout.addWidget(self.onTopCheckBox)

        self.statusEN = QLineEdit(self.widget)
        self.statusEN.setObjectName(u"statusEN")
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(12)
        self.statusEN.setFont(font1)

        self.horizontalLayout.addWidget(self.statusEN)

        self.statusZH = QLineEdit(self.widget)
        self.statusZH.setObjectName(u"statusZH")
        self.statusZH.setFont(font1)

        self.horizontalLayout.addWidget(self.statusZH)

        self.googleBtn = QPushButton(self.widget)
        self.googleBtn.setObjectName(u"googleBtn")

        self.horizontalLayout.addWidget(self.googleBtn)

        self.deeplBtn = QPushButton(self.widget)
        self.deeplBtn.setObjectName(u"deeplBtn")

        self.horizontalLayout.addWidget(self.deeplBtn)

        self.chatgptBtn = QPushButton(self.widget)
        self.chatgptBtn.setObjectName(u"chatgptBtn")

        self.horizontalLayout.addWidget(self.chatgptBtn)

        self.enBtn = QPushButton(self.widget)
        self.enBtn.setObjectName(u"enBtn")

        self.horizontalLayout.addWidget(self.enBtn)

        self.zhBtn = QPushButton(self.widget)
        self.zhBtn.setObjectName(u"zhBtn")

        self.horizontalLayout.addWidget(self.zhBtn)

        self.exitBtn = QPushButton(self.widget)
        self.exitBtn.setObjectName(u"exitBtn")

        self.horizontalLayout.addWidget(self.exitBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.inputEN = QPlainTextEdit(self.centralwidget)
        self.inputEN.setObjectName(u"inputEN")
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei"])
        font2.setPointSize(11)
        self.inputEN.setFont(font2)
        self.inputEN.setStyleSheet(u"background-color: rgb(203, 203, 203);\n"
"border-color: rgb(170, 0, 0);\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.inputEN, 1, 0, 1, 1)

        self.outputEN = QTextBrowser(self.centralwidget)
        self.outputEN.setObjectName(u"outputEN")
        self.outputEN.setFont(font2)
        self.outputEN.setStyleSheet(u"background-color: rgb(203, 203, 203);\n"
"border-color: rgb(170, 0, 0);\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.outputEN, 0, 1, 1, 1)

        self.inputZH = QPlainTextEdit(self.centralwidget)
        self.inputZH.setObjectName(u"inputZH")
        font3 = QFont()
        font3.setFamilies([u"\u9ed1\u4f53"])
        font3.setPointSize(13)
        self.inputZH.setFont(font3)
        self.inputZH.setStyleSheet(u"background-color: rgb(203, 203, 203);\n"
"border-color: rgb(170, 0, 0);\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.inputZH, 0, 0, 1, 1)

        self.outputZH = QTextBrowser(self.centralwidget)
        self.outputZH.setObjectName(u"outputZH")
        font4 = QFont()
        font4.setFamilies([u"\u9ed1\u4f53"])
        font4.setPointSize(13)
        font4.setBold(False)
        font4.setItalic(False)
        self.outputZH.setFont(font4)
        self.outputZH.setStyleSheet(u"background-color: rgb(203, 203, 203);\n"
"border-color: rgb(170, 0, 0);\n"
"border-radius: 10px;")

        self.gridLayout.addWidget(self.outputZH, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menumode = QMenu(self.menubar)
        self.menumode.setObjectName(u"menumode")
        self.menusettings = QMenu(self.menubar)
        self.menusettings.setObjectName(u"menusettings")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuFont = QMenu(self.menuView)
        self.menuFont.setObjectName(u"menuFont")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menusettings.menuAction())
        self.menubar.addAction(self.menumode.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menu.addAction(self.actionCopyZH)
        self.menu.addAction(self.actionAuto_Copy_EN)
        self.menu.addAction(self.actionClose_Mouse_Selection)
        self.menu.addAction(self.actionChatGPT_Stream)
        self.menu.addAction(self.actionCancel_Mouse_Backstage)
        self.menumode.addAction(self.actionZH2EN_only)
        self.menumode.addAction(self.actionEN2ZH_only)
        self.menusettings.addAction(self.actionProxy)
        self.menusettings.addAction(self.actionCheck_Proxy)
        self.menuView.addAction(self.menuFont.menuAction())
        self.menuView.addAction(self.actionJust_ZH)
        self.menuView.addAction(self.actionJust_EN)
        self.menuView.addAction(self.actionRestore)
        self.menuFont.addAction(self.actionFontZH)
        self.menuFont.addAction(self.actionFontEN)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionManual)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionCopyZH.setText(QCoreApplication.translate("MainWindow", u"Copy zhCN", None))
        self.actionAuto_Copy_EN.setText(QCoreApplication.translate("MainWindow", u"Auto Copy EN", None))
        self.actionClose_Mouse_Selection.setText(QCoreApplication.translate("MainWindow", u"Close Mouse Selection", None))
        self.actionChatGPT_Stream.setText(QCoreApplication.translate("MainWindow", u"ChatGPT Stream", None))
        self.actionCancel_Mouse_Backstage.setText(QCoreApplication.translate("MainWindow", u"Cancel Mouse Backstage", None))
        self.actionZH2EN_only.setText(QCoreApplication.translate("MainWindow", u"zh2en only", None))
        self.actionEN2ZH_only.setText(QCoreApplication.translate("MainWindow", u"en2zh only", None))
        self.actionBoth.setText(QCoreApplication.translate("MainWindow", u"both", None))
        self.actionProxy.setText(QCoreApplication.translate("MainWindow", u"Proxy", None))
        self.actionJust_ZH.setText(QCoreApplication.translate("MainWindow", u"Just ZH", None))
        self.actionJust_EN.setText(QCoreApplication.translate("MainWindow", u"Just EN", None))
        self.actionRestore.setText(QCoreApplication.translate("MainWindow", u"Restore", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.actionCheck_Proxy.setText(QCoreApplication.translate("MainWindow", u"Check Proxy", None))
        self.actionFontZH.setText(QCoreApplication.translate("MainWindow", u"Chinese font", None))
        self.actionFontEN.setText(QCoreApplication.translate("MainWindow", u"English font", None))
        self.onTopCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u754c\u9762\u7f6e\u9876", None))
        self.statusEN.setText("")
        self.googleBtn.setText(QCoreApplication.translate("MainWindow", u"Google", None))
        self.deeplBtn.setText(QCoreApplication.translate("MainWindow", u"DeepL", None))
        self.chatgptBtn.setText(QCoreApplication.translate("MainWindow", u"ChatGPT", None))
        self.enBtn.setText(QCoreApplication.translate("MainWindow", u"\u82f1\u8bd1\u6c49", None))
        self.zhBtn.setText(QCoreApplication.translate("MainWindow", u"\u6c49\u8bd1\u82f1", None))
        self.exitBtn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Operation", None))
        self.menumode.setTitle(QCoreApplication.translate("MainWindow", u"mode", None))
        self.menusettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuFont.setTitle(QCoreApplication.translate("MainWindow", u"Font", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

