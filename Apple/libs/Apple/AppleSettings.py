import json
import logging
import os

from .AppleErrors import FilePathNotFoundException


class Settings:
    """Apple Launcher的设置类"""

    def __init__(self, setting_file: str) -> None:
        self.setting_file: str = setting_file

        self.initial_settings: dict = {
            "debug_mode": False,
            "minecraft_dic": "./.minecraft",
            "current_minecraft": "",
            "javaw_path": "",
            "max_memory": "1024m",
            "username": "",
            "uuid": "",
            "access_token": "",
            "width": "873",
            "height": "501",
        }

        if not os.path.isfile("./Apple/Settings.json"):
            with open("./Apple/Settings.json", "w") as f:
                f.write(self.initial_settings)

        try:
            with open(setting_file) as s:
                self._settings: dict = json.loads(s.read())
        except Exception as e:
            logging.error(e)
            with open(setting_file, 'w') as s:  # 初始化设置文件
                s.write(json.dumps(self.initial_settings))
            self._settings: dict = self.initial_settings

    def write_settings(self) -> None:
        if self.setting_file is False: raise FilePathNotFoundException("File's path is not found")
        with open(self.setting_file) as s:
            s.write(json.dumps(self._settings))

    def get_settings(self) -> dict:
        return self._settings
