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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QTextBrowser,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(971, 717)
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
        self.actionProxy = QAction(MainWindow)
        self.actionProxy.setObjectName(u"actionProxy")
        self.actionFont = QAction(MainWindow)
        self.actionFont.setObjectName(u"actionFont")
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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.outputZH = QTextBrowser(self.centralwidget)
        self.outputZH.setObjectName(u"outputZH")
        font = QFont()
        font.setFamilies([u"\u9ed1\u4f53"])
        font.setPointSize(13)
        self.outputZH.setFont(font)

        self.gridLayout.addWidget(self.outputZH, 0, 0, 1, 1)

        self.outputEN = QTextBrowser(self.centralwidget)
        self.outputEN.setObjectName(u"outputEN")
        font1 = QFont()
        font1.setFamilies([u"\u5b8b\u4f53"])
        font1.setPointSize(13)
        self.outputEN.setFont(font1)

        self.gridLayout.addWidget(self.outputEN, 0, 1, 1, 1)

        self.inputEN = QPlainTextEdit(self.centralwidget)
        self.inputEN.setObjectName(u"inputEN")
        self.inputEN.setFont(font1)

        self.gridLayout.addWidget(self.inputEN, 1, 0, 1, 1)

        self.inputZH = QPlainTextEdit(self.centralwidget)
        self.inputZH.setObjectName(u"inputZH")
        self.inputZH.setFont(font)

        self.gridLayout.addWidget(self.inputZH, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 40))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.statusEN = QLineEdit(self.widget)
        self.statusEN.setObjectName(u"statusEN")
        font2 = QFont()
        font2.setFamilies([u"\u5b8b\u4f53"])
        font2.setPointSize(12)
        self.statusEN.setFont(font2)

        self.horizontalLayout.addWidget(self.statusEN)

        self.statusZH = QLineEdit(self.widget)
        self.statusZH.setObjectName(u"statusZH")
        self.statusZH.setFont(font2)

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

        self.allBtn = QPushButton(self.widget)
        self.allBtn.setObjectName(u"allBtn")

        self.horizontalLayout.addWidget(self.allBtn)

        self.exitBtn = QPushButton(self.widget)
        self.exitBtn.setObjectName(u"exitBtn")

        self.horizontalLayout.addWidget(self.exitBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 971, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menusettings = QMenu(self.menubar)
        self.menusettings.setObjectName(u"menusettings")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.RightToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menusettings.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menu.addAction(self.actionCopyZH)
        self.menu.addAction(self.actionAuto_Copy_EN)
        self.menu.addAction(self.actionClose_Mouse_Selection)
        self.menu.addAction(self.actionChatGPT_Stream)
        self.menu.addAction(self.actionCancel_Mouse_Backstage)
        self.menusettings.addAction(self.actionProxy)
        self.menusettings.addAction(self.actionCheck_Proxy)
        self.menuView.addAction(self.actionFont)
        self.menuView.addAction(self.actionJust_ZH)
        self.menuView.addAction(self.actionJust_EN)
        self.menuView.addAction(self.actionRestore)
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
        self.actionProxy.setText(QCoreApplication.translate("MainWindow", u"Proxy", None))
        self.actionFont.setText(QCoreApplication.translate("MainWindow", u"Font", None))
        self.actionJust_ZH.setText(QCoreApplication.translate("MainWindow", u"Just ZH", None))
        self.actionJust_EN.setText(QCoreApplication.translate("MainWindow", u"Just EN", None))
        self.actionRestore.setText(QCoreApplication.translate("MainWindow", u"Restore", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionManual.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.actionCheck_Proxy.setText(QCoreApplication.translate("MainWindow", u"Check Proxy", None))
        self.statusEN.setText("")
        self.googleBtn.setText(QCoreApplication.translate("MainWindow", u"Google", None))
        self.deeplBtn.setText(QCoreApplication.translate("MainWindow", u"DeepL", None))
        self.chatgptBtn.setText(QCoreApplication.translate("MainWindow", u"ChatGPT", None))
        self.enBtn.setText(QCoreApplication.translate("MainWindow", u"\u82f1\u8bd1\u6c49", None))
        self.zhBtn.setText(QCoreApplication.translate("MainWindow", u"\u6c49\u8bd1\u82f1", None))
        self.allBtn.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.exitBtn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Operation", None))
        self.menusettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

