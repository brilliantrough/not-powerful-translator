import sys

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from menu.settings_manager import SettingsManager


class SettingsPanel(QWidget):
    settings_changed = pyqtSignal()  # Signal to notify when settings are changed

    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(15)

        # 左侧列表
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(
            """
            QListWidget {
                background-color: #f0f0f0;
                border-radius: 5px;
                padding: 10px;
                color: #333333;
                font-size: 18px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #d0d0d0;
            }
        """
        )
        self.list_widget.addItem("快捷键设置")
        self.list_widget.addItem("通用设置")
        self.list_widget.addItem("服务设置")
        self.list_widget.addItem("窗口设置")
        self.list_widget.addItem("运行设置")
        self.list_widget.setFont(QFont("SimSun", 18))
        self.list_widget.currentRowChanged.connect(self.display_settings)

        # 右侧面板
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(
            """
            QWidget {
                background-color: #ffffff;
                border-radius: 5px;
                padding: 15px;
            }
            QLabel {
                color: #333333;
                font-size: 18px;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 10px;
                color: #333333;
                font-size: 18px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #aaaaaa;
            }
        """
        )
        self.create_shortcut_settings()
        self.create_general_settings()
        self.create_service_settings()
        self.create_window_settings()
        self.create_runtime_settings()

        self.layout.addWidget(self.list_widget, 1)
        self.layout.addWidget(self.stacked_widget, 3)
        self.setLayout(self.layout)

    def create_shortcut_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()

        save_layout = QHBoxLayout()
        save_label = QLabel("保存快捷键:", font=QFont("SimSun", 14))
        self.save_shortcut = QLineEdit()
        save_value = self.settings_manager.get_setting("shortcut_settings", "save")
        self.save_shortcut.setText(save_value)
        self.save_shortcut.editingFinished.connect(
            lambda: self.update_setting(
                "shortcut_settings", "save", self.save_shortcut.text()
            )
        )
        save_layout.addWidget(save_label)
        save_layout.addWidget(self.save_shortcut)

        open_layout = QHBoxLayout()
        open_label = QLabel("打开快捷键:", font=QFont("SimSun", 14))
        self.open_shortcut = QLineEdit()
        open_value = self.settings_manager.get_setting("shortcut_settings", "open")
        self.open_shortcut.setText(open_value)
        self.open_shortcut.editingFinished.connect(
            lambda: self.update_setting(
                "shortcut_settings", "open", self.open_shortcut.text()
            )
        )
        open_layout.addWidget(open_label)
        open_layout.addWidget(self.open_shortcut)

        hotkey_layout = QHBoxLayout()
        hotkey_label = QLabel("热键:", font=QFont("SimSun", 18))
        self.hotkey_shortcut = QLineEdit()
        hotkey_value = self.settings_manager.get_setting("shortcut_settings", "hotkey")
        self.hotkey_shortcut.setText(hotkey_value)
        self.hotkey_shortcut.editingFinished.connect(
            lambda: self.update_setting(
                "shortcut_settings", "hotkey", self.hotkey_shortcut.text()
            )
        )
        hotkey_layout.addWidget(hotkey_label)
        hotkey_layout.addWidget(self.hotkey_shortcut)

        layout.addLayout(save_layout)
        layout.addLayout(open_layout)
        layout.addLayout(hotkey_layout)
        layout.addStretch()
        widget.setLayout(layout)
        widget.setFont(QFont("SimSun", 18))
        self.stacked_widget.addWidget(widget)

    def create_general_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()

        language_layout = QHBoxLayout()
        language_label = QLabel("语言:", font=QFont("SimSun", 18))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "中文", "Español"])
        language_value = self.settings_manager.get_setting(
            "general_settings", "language"
        )
        index = self.language_combo.findText(language_value)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        self.language_combo.currentTextChanged.connect(
            lambda: self.update_setting(
                "general_settings", "language", self.language_combo.currentText()
            )
        )
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)

        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:", font=QFont("SimSun", 18))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        theme_value = self.settings_manager.get_setting("general_settings", "theme")
        index = self.theme_combo.findText(theme_value)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        self.theme_combo.currentTextChanged.connect(
            lambda: self.update_setting(
                "general_settings", "theme", self.theme_combo.currentText()
            )
        )
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)

        font_layout = QHBoxLayout()
        font_label = QLabel("字体大小:", font=QFont("SimSun", 18))
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 48)
        font_value = self.settings_manager.get_setting("general_settings", "font_size")
        if font_value is None:
            font_value = 12  # default value
        self.font_spin.setValue(font_value)
        self.font_spin.valueChanged.connect(
            lambda val: self.update_setting("general_settings", "font_size", val)
        )
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_spin)

        layout.addLayout(language_layout)
        layout.addLayout(theme_layout)
        layout.addLayout(font_layout)
        layout.addStretch()
        widget.setLayout(layout)
        widget.setFont(QFont("SimSun", 18))
        self.stacked_widget.addWidget(widget)

    def create_service_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()

        proxy_layout = QHBoxLayout()
        proxy_label = QLabel("代理:", font=QFont("SimSun", 18))
        self.proxy_edit = QLineEdit()
        proxy_value = self.settings_manager.get_setting("service_settings", "proxy")
        self.proxy_edit.setText(proxy_value)
        self.proxy_edit.editingFinished.connect(
            lambda: self.update_setting(
                "service_settings", "proxy", self.proxy_edit.text()
            )
        )
        proxy_layout.addWidget(proxy_label)
        proxy_layout.addWidget(self.proxy_edit)

        engine_layout = QHBoxLayout()
        engine_label = QLabel("翻译引擎:", font=QFont("SimSun", 18))
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Google", "Bing", "DeepL", "ChatGPT"])
        engine_value = self.settings_manager.get_setting(
            "service_settings", "translation_engine"
        )
        index = self.engine_combo.findText(engine_value)
        if index >= 0:
            self.engine_combo.setCurrentIndex(index)
        self.engine_combo.currentTextChanged.connect(
            lambda: self.update_setting(
                "service_settings",
                "translation_engine",
                self.engine_combo.currentText(),
            )
        )
        engine_layout.addWidget(engine_label)
        engine_layout.addWidget(self.engine_combo)

        openai_base_layout = QHBoxLayout()
        openai_base_label = QLabel("OpenAI API Base:", font=QFont("SimSun", 18))
        self.openai_base_edit = QLineEdit()
        openai_base_value = self.settings_manager.get_setting(
            "service_settings", "OPENAI_API_BASE"
        )
        self.openai_base_edit.setText(openai_base_value)
        self.openai_base_edit.editingFinished.connect(
            lambda: self.update_setting(
                "service_settings", "OPENAI_API_BASE", self.openai_base_edit.text()
            )
        )
        openai_base_layout.addWidget(openai_base_label)
        openai_base_layout.addWidget(self.openai_base_edit)

        openai_key_layout = QHBoxLayout()
        openai_key_label = QLabel("OpenAI API Key:", font=QFont("SimSun", 18))
        self.openai_key_edit = QLineEdit()
        openai_key_value = self.settings_manager.get_setting(
            "service_settings", "OPENAI_API_KEY"
        )
        self.openai_key_edit.setText(openai_key_value)
        self.openai_key_edit.editingFinished.connect(
            lambda: self.update_setting(
                "service_settings", "OPENAI_API_KEY", self.openai_key_edit.text()
            )
        )
        openai_key_layout.addWidget(openai_key_label)
        openai_key_layout.addWidget(self.openai_key_edit)

        openai_model_layout = QHBoxLayout()
        openai_model_label = QLabel("OpenAI Model:", font=QFont("SimSun", 18))
        self.openai_model_edit = QLineEdit()
        openai_model_value = self.settings_manager.get_setting(
            "service_settings", "OPENAI_MODEL"
        )
        self.openai_model_edit.setText(openai_model_value)
        self.openai_model_edit.editingFinished.connect(
            lambda: self.update_setting(
                "service_settings", "OPENAI_MODEL", self.openai_model_edit.text()
            )
        )
        openai_model_layout.addWidget(openai_model_label)
        openai_model_layout.addWidget(self.openai_model_edit)

        baidu_app_id_layout = QHBoxLayout()
        baidu_app_id_label = QLabel("Baidu App ID:", font=QFont("SimSun", 18))
        self.baidu_app_id_edit = QLineEdit()
        baidu_app_id_value = self.settings_manager.get_setting(
            "service_settings", "BAIDU_APP_ID"
        )
        self.baidu_app_id_edit.setText(baidu_app_id_value)
        self.baidu_app_id_edit.editingFinished.connect(
            lambda: self.update_setting(
                "service_settings", "BAIDU_APP_ID", self.baidu_app_id_edit.text()
            )
        )
        baidu_app_id_layout.addWidget(baidu_app_id_label)
        baidu_app_id_layout.addWidget(self.baidu_app_id_edit)

        baidu_key_layout = QHBoxLayout()
        baidu_key_label = QLabel("Baidu Key:", font=QFont("SimSun", 18))
        self.baidu_key_edit = QLineEdit()
        baidu_key_value = self.settings_manager.get_setting(
            "service_settings", "BAIDU_KEY"
        )
        self.baidu_key_edit.setText(baidu_key_value)
        self.baidu_key_edit.editingFinished.connect(
            lambda: self.update_setting(
                "service_settings", "BAIDU_KEY", self.baidu_key_edit.text()
            )
        )
        baidu_key_layout.addWidget(baidu_key_label)
        baidu_key_layout.addWidget(self.baidu_key_edit)

        layout.addLayout(proxy_layout)
        layout.addLayout(engine_layout)
        layout.addLayout(openai_base_layout)
        layout.addLayout(openai_key_layout)
        layout.addLayout(openai_model_layout)
        layout.addLayout(baidu_app_id_layout)
        layout.addLayout(baidu_key_layout)
        layout.addStretch()
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

    def create_window_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()
        widget.setLayout(layout)

        width_layout = QHBoxLayout()
        width_label = QLabel("窗口宽度:", font=QFont("SimSun", 18))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(300, 1920)
        width_value = self.settings_manager.get_setting("window_settings", "width")
        self.width_spin.setValue(width_value)
        self.width_spin.valueChanged.connect(
            lambda val: self.update_setting("window_settings", "width", val)
        )
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_spin)

        height_layout = QHBoxLayout()
        height_label = QLabel("窗口高度:", font=QFont("SimSun", 18))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(300, 1080)
        height_value = self.settings_manager.get_setting("window_settings", "height")
        self.height_spin.setValue(height_value)
        self.height_spin.valueChanged.connect(
            lambda val: self.update_setting("window_settings", "height", val)
        )
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_spin)

        always_on_top_layout = QHBoxLayout()
        always_on_top_label = QLabel("始终置顶:", font=QFont("SimSun", 18))
        self.always_on_top_check = QCheckBox()
        always_on_top_value = self.settings_manager.get_setting(
            "window_settings", "always_on_top"
        )
        self.always_on_top_check.setChecked(always_on_top_value)
        self.always_on_top_check.stateChanged.connect(
            lambda: self.update_setting(
                "window_settings", "always_on_top", self.always_on_top_check.isChecked()
            )
        )
        always_on_top_layout.addWidget(always_on_top_label)
        always_on_top_layout.addWidget(self.always_on_top_check)

        hide_input_layout = QHBoxLayout()
        hide_input_label = QLabel("隐藏输入框:", font=QFont("SimSun", 18))
        self.hide_input_check = QCheckBox()
        hide_input_value = self.settings_manager.get_setting(
            "window_settings", "hide_input"
        )
        self.hide_input_check.setChecked(hide_input_value)
        self.hide_input_check.stateChanged.connect(
            lambda: self.update_setting(
                "window_settings", "hide_input", self.hide_input_check.isChecked()
            )
        )
        hide_input_layout.addWidget(hide_input_label)
        hide_input_layout.addWidget(self.hide_input_check)

        hide_output_layout = QHBoxLayout()
        hide_output_label = QLabel("隐藏输出框:", font=QFont("SimSun", 18))
        self.hide_output_check = QCheckBox()
        hide_output_value = self.settings_manager.get_setting(
            "window_settings", "hide_output"
        )
        self.hide_output_check.setChecked(hide_output_value)
        hide_output_layout.addWidget(hide_output_label)
        hide_output_layout.addWidget(self.hide_output_check)

        simple_mode_layout = QHBoxLayout()
        simple_mode_label = QLabel("极简模式:", font=QFont("SimSun", 18))
        self.simple_mode_check = QCheckBox()
        simple_mode_value = self.settings_manager.get_setting(
            "window_settings", "simple_mode"
        )
        self.simple_mode_check.setChecked(simple_mode_value)
        self.simple_mode_check.stateChanged.connect(
            lambda: self.update_setting(
                "window_settings", "simple_mode", self.simple_mode_check.isChecked()
            )
        )
        simple_mode_layout.addWidget(simple_mode_label)
        simple_mode_layout.addWidget(self.simple_mode_check)

        layout.addLayout(width_layout)
        layout.addLayout(height_layout)
        layout.addLayout(always_on_top_layout)
        layout.addLayout(hide_input_layout)
        layout.addLayout(hide_output_layout)
        layout.addLayout(simple_mode_layout)
        layout.addStretch()
        widget.setLayout(layout)
        widget.setFont(QFont("SimSun", 18))
        self.stacked_widget.addWidget(widget)

    def create_runtime_settings(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()
        widget.setLayout(layout)

        auto_hide_layout = QHBoxLayout()
        auto_hide_label = QLabel("自动隐藏:", font=QFont("SimSun", 18))
        self.auto_hide_check = QCheckBox()
        auto_hide_value = self.settings_manager.get_setting(
            "runtime_settings", "auto_hide"
        )
        self.auto_hide_check.setChecked(auto_hide_value)
        self.auto_hide_check.stateChanged.connect(
            lambda: self.update_setting(
                "runtime_settings", "auto_hide", self.auto_hide_check.isChecked()
            )
        )
        auto_hide_layout.addWidget(auto_hide_label)
        auto_hide_layout.addWidget(self.auto_hide_check)

        cancel_mouse_backstage_layout = QHBoxLayout()
        cancel_mouse_backstage_label = QLabel("后台取消划词:", font=QFont("SimSun", 18))
        self.cancel_mouse_backstage_check = QCheckBox()
        cancel_mouse_backstage_value = self.settings_manager.get_setting(
            "runtime_settings", "cancel_mouse_backstage"
        )
        self.cancel_mouse_backstage_check.setChecked(cancel_mouse_backstage_value)
        self.cancel_mouse_backstage_check.stateChanged.connect(
            lambda: self.update_setting(
                "runtime_settings",
                "cancel_mouse_backstage",
                self.cancel_mouse_backstage_check.isChecked(),
            )
        )
        cancel_mouse_backstage_layout.addWidget(cancel_mouse_backstage_label)
        cancel_mouse_backstage_layout.addWidget(self.cancel_mouse_backstage_check)

        use_select_text_layout = QHBoxLayout()
        use_select_text_label = QLabel("划词翻译:", font=QFont("SimSun", 18))
        self.use_select_text_check = QCheckBox()
        use_select_text_value = self.settings_manager.get_setting(
            "runtime_settings", "use_select_text"
        )
        self.use_select_text_check.setChecked(use_select_text_value)
        self.use_select_text_check.stateChanged.connect(
            lambda: self.update_setting(
                "runtime_settings",
                "use_select_text",
                self.use_select_text_check.isChecked(),
            )
        )
        use_select_text_layout.addWidget(use_select_text_label)
        use_select_text_layout.addWidget(self.use_select_text_check)

        use_mouse_listen_layout = QHBoxLayout()
        use_mouse_listen_label = QLabel("鼠标监听:", font=QFont("SimSun", 18))
        self.use_mouse_listen_check = QCheckBox()
        use_mouse_listen_value = self.settings_manager.get_setting(
            "runtime_settings", "use_mouse_listen"
        )
        self.use_mouse_listen_check.setChecked(use_mouse_listen_value)
        self.use_mouse_listen_check.stateChanged.connect(
            lambda: self.update_setting(
                "runtime_settings",
                "use_mouse_listen",
                self.use_mouse_listen_check.isChecked(),
            )
        )
        use_mouse_listen_layout.addWidget(use_mouse_listen_label)
        use_mouse_listen_layout.addWidget(self.use_mouse_listen_check)

        use_button_layout = QHBoxLayout()
        use_button_label = QLabel("按钮翻译:", font=QFont("SimSun", 18))
        self.use_button_check = QCheckBox()
        use_button_value = self.settings_manager.get_setting(
            "runtime_settings", "use_button"
        )
        self.use_button_check.setChecked(use_button_value)
        self.use_button_check.stateChanged.connect(
            lambda: self.update_setting(
                "runtime_settings", "use_button", self.use_button_check.isChecked()
            )
        )
        use_button_layout.addWidget(use_button_label)
        use_button_layout.addWidget(self.use_button_check)

        use_hotkey_layout = QHBoxLayout()
        use_hotkey_label = QLabel("快捷键翻译:", font=QFont("SimSun", 18))
        self.use_hotkey_check = QCheckBox()
        use_hotkey_value = self.settings_manager.get_setting(
            "runtime_settings", "use_hotkey"
        )
        self.use_hotkey_check.setChecked(use_hotkey_value)
        self.use_hotkey_check.stateChanged.connect(
            lambda: self.update_setting(
                "runtime_settings", "use_hotkey", self.use_hotkey_check.isChecked()
            )
        )
        use_hotkey_layout.addWidget(use_hotkey_label)
        use_hotkey_layout.addWidget(self.use_hotkey_check)

        layout.addLayout(auto_hide_layout)
        layout.addLayout(cancel_mouse_backstage_layout)
        layout.addLayout(use_select_text_layout)
        layout.addLayout(use_mouse_listen_layout)
        layout.addLayout(use_button_layout)
        layout.addLayout(use_hotkey_layout)
        layout.addStretch()
        widget.setLayout(layout)
        widget.setFont(QFont("SimSun", 18))
        self.stacked_widget.addWidget(widget)

    def display_settings(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def update_setting(self, category, key, value):
        self.settings_manager.set_setting(category, key, value)
        self.settings_changed.emit()  # Emit signal when settings are updated


class SettingsWindow(QMainWindow):
    closed = pyqtSignal()  # Signal to notify when the window is closed
    settings_applied = pyqtSignal()  # Signal to notify when settings are applied

    def __init__(self, settings_manager):
        super().__init__()
        self.setWindowTitle("设置")
        icon = QIcon()
        icon.addFile(":/candy.ico", QSize(), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        self.setGeometry(300, 300, 700, 500)

        # 设置窗口样式
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }
            QMainWindow::title {
                color: #333333;
                font-size: 16px;
                padding-left: 10px;
            }
        """
        )

        # 添加阴影效果
        self.setWindowFlags(Qt.Window)

        self.settings_panel = SettingsPanel(settings_manager)

        # Add Apply button to the bottom-right corner
        self.apply_button = QPushButton("应用", self)
        self.apply_button.setFont(QFont("SimSun", 13))
        self.apply_button.clicked.connect(self.applySettings)

        # Create a layout for the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push the button to the right
        button_layout.addWidget(self.apply_button)

        # Add the button layout to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.settings_panel)
        main_layout.addLayout(button_layout)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 添加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)
        self.settings_panel.setGraphicsEffect(shadow)

        self.settings_panel.settings_changed.connect(self.onSettingsChanged)

    def onSettingsChanged(self):
        """Handle settings changes."""
        pass

    def closeEvent(self, event):
        self.closed.emit()  # Emit the signal when the window is closed
        super().closeEvent(event)

    def applySettings(self):
        """Apply settings and notify the main window."""
        self.settings_applied.emit()  # Emit signal when settings are applied
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("主窗口")
        self.setGeometry(100, 100, 800, 600)

        menubar = self.menuBar()
        settings_menu = menubar.addMenu("设置")

        open_settings_action = QAction("打开设置", self)
        open_settings_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(open_settings_action)

        # 设置菜单栏和菜单项的样式
        self.setStyleSheet(
            """
            QMenuBar {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'SimSun';
                font-size: 16px;
            }
            QMenuBar::item {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'SimSun';
                font-size: 16px;
            }
            QMenuBar::item:selected {
                background-color: #d0d0d0;
            }
            QMenu {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'SimSun';
                font-size: 16px;
            }
            QMenu::item {
                background-color: #f0f0f0;
                color: #333333;
                font-family: 'SimSun';
                font-size: 16px;
            }
            QMenu::item:selected {
                background-color: #d0d0d0;
            }
            """
        )

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self.settings_manager)
        self.settings_window.settings_applied.connect(self.onSettingsApplied)
        self.settings_window.show()

    def onSettingsApplied(self):
        """Handle the application of settings."""
        # Update the main window based on new settings
        print("Settings have been applied.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
