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


# ----------函数定义---------- #
def stop_app(status_code):  # 退出
    sys.exit(status_code)


# ----------主函数---------- #
def main() -> None:
    """
    Apple Launcher的程序入口点。

    :return: None
    """

    # 初始化程序块开始

    if not os.path.isdir('Apple'):  # 如果没有这个文件夹，就造一个
        os.mkdir('Apple')

    if os.path.isfile("./Apple/Log.log"):  # 日志文件
        os.remove("./Apple/Log.log")

    if not os.path.exists("./Apple/Settings.json"):
        with open("./Apple/Settings.json", 'w') as sf:  # 初始化设置文件
            sf.write("""
{
    "debug_mode": "False"
}
""")

    with open('./Apple/Settings.json', 'r') as sf:  # 防止有某些比较喜欢给启动器整点报错的人给设置文件的内容tm删了
        if not sf.read():
            sf.write("""
{
    "debug_mode": "False"
}
""")

    with open('./Apple/Settings.json', 'r') as settings:  # 这一段都是读取调试模式的
        try:
            sj = json.load(settings)
            debug_mode: bool = sj["debug_mode"]
            if not debug_mode:
                logging.info("[Main]: 调试模式已开启")
                logging.basicConfig(filename='./Apple/Log.log', level=logging.DEBUG,
                                    format='[%(asctime)s][%(levelname)s]%(message)s', encoding="utf-8")
            else:
                logging.info("[Main]: 调试模式已关闭")
                logging.basicConfig(filename='./Apple/Log.log', level=logging.INFO,
                                    format='[%(asctime)s][%(levelname)s]%(message)s', encoding="utf-8")
        except KeyError as e:
            logging.error(e)

    show_version = 'a0.0.0'  # 显示出来的版本号

    try:
        import Apple.libs.Apple.AppleSnapshot  # 这玩意是用来检查是不是快照版的，如果是的话在构造程序包的时候会封进去的

        def is_snapshot():
            return True

        def snapshot():
            return 'Snapshot'
    except ImportError:
        def is_snapshot():
            return False

        def snapshot():
            return 'Release'

    system_info: list[str] = [platform.system(),  # 0，系统名称，如Windows、Linux、Mac OS……
                              platform.release(),  # 1，系统版本号，如7、8、10、11……
                              platform.architecture()[0],  # 2，系统的位数，如32bit、64bit
                              ]

    logging.info(f"[Main]: 程序包构建，版本{snapshot()}")

    logging.info(
        f'[Main]: Apple Launcher {show_version}，运行在{system_info[3] + "的" + system_info[0] + " " + system_info[1]}平台上'
        .replace('bit', '位')  # 译名本地化（
    )

    # 初始化程序块结束

    # 主函数实际程序块开始

    root = tk.Tk()
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

    # 主函数实际程序块结束


if __name__ == '__main__':
    main()
