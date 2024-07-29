"""
    Apple Launcher by MimiRabbit
"""

# ----------导入支持库---------- #
# Python内置库
import logging
import os
import platform
import sys
import json
import subprocess
import threading

# 第三方库
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

# Apple Launcher
from Apple.libs.Apple import AppleSettings
from Apple.libs.Minecraft import MinecraftLaunch


class LauncherUI(QMainWindow):
    def __init__(self, launch_game: any) -> None:
        super().__init__()
        self.load_done = False
        self.launch_game = launch_game
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle("Apple Launcher")
        self.setFixedSize(800, 450)
        self.setStyleSheet("background-color: black;")

        launch_mc: QPushButton = QPushButton("启动Minecraft", self)
        launch_mc.setFixedSize(200, 50)
        launch_mc.setStyleSheet("background-color: #52a435; "
                                "border: 1px solid green; "
                                "outline: none; "
                                "border-radius: 5px;")
        launch_mc.move(590, 390)
        launch_mc.clicked.connect(self.launch_game)
        # TODO: 添加更多按钮和功能
        self.load_done = True

    def is_loaded(self) -> bool:
        return self.load_done


class Launcher:
    """启动器类"""

    def __init__(self) -> None:
        # 初始化程序块开始

        if not os.path.isdir('Apple'):  # 如果没有这个文件夹，就造一个
            os.mkdir('Apple')

        if os.path.isfile("./Apple/Log.log"):  # 日志文件
            os.remove("./Apple/Log.log")

        with open("./Apple/Log.log", "w"):
            pass

        self.system_info: list[str] = [platform.system(),  # 0，系统名称，如Windows、Linux、Mac OS……
                                       platform.release(),  # 1，系统版本号，如7、8、10、11……
                                       platform.architecture()[0],  # 2，系统的位数，如32bit、64bit
                                       os.getcwd(),  # 3，程序运行路径
                                       ]

        self.settings: AppleSettings.Settings = AppleSettings.Settings(f"{self.system_info[3]}/Apple/Settings.json")
        self.dumped_settings: dict = self.settings.get_settings()

        if not os.path.exists("./Apple/Settings.json"):
            with open("./Apple/Settings.json", 'w') as sf:  # 初始化设置文件
                sf.write(self.dumped_settings)

        debug_mode: bool = self.settings.get_settings()["debug_mode"]
        if debug_mode:
            logging.basicConfig(level=logging.DEBUG, filename="./Apple/Log.log",
                                format='[%(asctime)s][%(levelname)s]%(message)s', encoding="utf-8")
        else:
            logging.basicConfig(level=logging.INFO, filename="./Apple/Log.log",
                                format='[%(asctime)s][%(levelname)s]%(message)s', encoding="utf-8")
        logging.debug("[Main]: 调试模式已开启")

        self.large_version: str = "0"  # 大版本号
        self.show_version: str = 'a0.0.0'  # 显示出来的版本号

        logging.info(f"[Main]: 程序包版本{self.snapshot()}")

        logging.info(
            f'[Main]: Apple Launcher {self.show_version}, 运行在{self.system_info[2] + "的" + self.system_info[0] + " " + self.system_info[1]}平台上'
            .replace('bit', '位')  # 译名本地化（
        )

        # 初始化程序块结束

    @staticmethod
    def stop_app(status_code: int) -> None:  # 退出
        sys.exit(status_code)

    @staticmethod
    def is_snapshot() -> bool:
        return True

    @staticmethod
    def snapshot() -> str:
        return 'Snapshot'


    # ----------主函数---------- #
    def main(self) -> None:
        """
        Apple Launcher类的主函数。

        :return: None
        """

        # 定义临时函数

        def launch_game():
            final_arg: str = MinecraftLaunch.McLauncher.launch_mc(self.large_version,
                                                                  self.dumped_settings["minecraft_dic"],
                                                                  self.dumped_settings["current_minecraft"],
                                                                  self.dumped_settings["javaw_path"],
                                                                  self.dumped_settings["max_memory"],
                                                                  self.dumped_settings["username"],
                                                                  self.dumped_settings["uuid"],
                                                                  self.dumped_settings["access_token"],
                                                                  self.dumped_settings["width"],
                                                                  self.dumped_settings["height"],
                                                                  )
            with open("Launch.bat", 'w') as l:
                l.write(final_arg)

            process = subprocess.Popen("Launch.bat", stdout=True, text=True)
            return_code = process.poll()
            if return_code is None:
                # 子进程仍在运行
                pass
            else:
                # 子进程已结束，根据返回码记录日志
                if return_code == 0:
                    logging.info("[Launch]: Minecraft正常退出")
                else:
                    logging.warning(f"[Launch]: Minecraft非正常退出，返回码为{return_code}")

        # 主函数实际程序块开始

        root: QApplication = QApplication(sys.argv)
        l = LauncherUI(launch_game)
        logging.debug('[Main]: 创建窗体')

        while not l.is_loaded(): pass

        l.show()
        sys.exit(root.exec_())
        # TODO: 启动器的主方法

        # ...

        # 主函数实际程序块结束


class Main:
    """Apple Launcher的主类"""

    @staticmethod
    def main() -> None:
        """Apple Launcher的程序入口点"""
        launcher: Launcher = Launcher()
        launcher.main()


if __name__ == '__main__':
    Main.main()
