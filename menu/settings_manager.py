import json
import os


class SettingsManager:
    def __init__(self, filepath="settings.json"):
        self.filepath = filepath
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.filepath):
            self.create_default_settings()
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

    def create_default_settings(self):
        default_settings = {
            "shortcut_settings": {
                "save": "Ctrl+S",
                "open": "Ctrl+O",
                "hotkey": "Alt+Q",
            },
            "general_settings": {
                "language": "English",
                "theme": "Light",
                "font_size": 12,
            },
            "service_settings": {
                "proxy": "http://localhost:7890",
                "translation_engine": "Google",
                "OPENAI_API_BASE": "https://api.openai.com/v1",
                "OPENAI_API_KEY": "sk-xxxxxxxx",
                "BAIDU_APP_ID": "xxxxxxxx",
                "BAIDU_KEY": "xxxxxxxx",
                "OPENAI_MODEL": "gpt-4o-mini",
            },
            "runtime_settings": {
                "use_select_text": True,
                "use_mouse_listen": True,
                "use_button": True,
                "use_hotkey": True,
                "auto_hide": False,
                "cancel_mouse_backstage": False,
            },
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)

    def get_setting(self, category, key, default=None):
        return self.settings.get(category, {}).get(key, default)

    def set_setting(self, category, key, value):
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        # self.save_settings()

    def save_settings(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)
