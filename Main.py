"""
    Apple Launcher by MimiRabbit
"""

# ----------导入支持库---------- #
# Python内置库
import logging
import os
import platform
import sys
import tkinter as tk
import json

# 第三方库
import pywinstyles

# Apple Launcher
from Apple.libs.Apple import AppleSettings


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
        self.dumped_settings: str = json.dumps(self.settings.get_settings())

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

        self.show_version: str = 'a0.0.0'  # 显示出来的版本号

        logging.info(f"[Main]: 程序包版本{self.snapshot()}")

        logging.info(
            f'[Main]: Apple Launcher {self.show_version}, 运行在{self.system_info[2] + "的" + self.system_info[0] + " " + self.system_info[1]}平台上'
            .replace('bit ', '位 ')  # 译名本地化（
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

        # 主函数实际程序块开始

        root: tk.Tk = tk.Tk()
        logging.debug('[Main]: 创建窗体')

        root.iconphoto(False, tk.PhotoImage(file='Apple/icon/icon.ico'))  # 图标
        pywinstyles.apply_style(root, 'acrylic')  # 主题
        pywinstyles.change_border_color(root, color="#000000")  # 边框颜色
        root.title(" ")  # 设置窗口标题
        root.minsize(800, 450)  # 应该都看得懂吧？
        root.geometry("800x450")

        root.mainloop()  # 窗体循环
        logging.debug('[Window]: 窗体循环启动')
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
