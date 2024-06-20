import json
import os
import zipfile
import logging

logging.basicConfig(level=logging.INFO,
                                    format='[%(asctime)s][%(levelname)s]%(message)s', encoding="utf-8")

def unzip(file: str, to_path: str) -> None:  # 解压文件的函数
    try:
        with zipfile.ZipFile(file) as _zip:
            for f in _zip.namelist():
                _zip.extract(f, to_path)
    except Exception:
        return None


def is_found_ver(ver: str, appdata: str) -> bool:  # 检查版本是否存在
    if os.path.exists(f"{appdata}/versions/{ver}/{ver}.json"):
        return True
    else:
        return False


def launch_mc(appdata: str, ver: str, java_path: str, xmx: str, username: str, uuid: str, access_token: str,
              width: str="873", height: str="501"):  # 启动mc
    # 初始化
    command: str = ""  # 启动命令行
    jvm: str = java_path  # JVM参数
    cp: str = ""  # -ClassPath（-cp）传入参数
    game: str = ""  # 游戏参数
    logging.info('[Launch]: 已初始化启动参数')

    if (
        java_path != "" and
        ver != "" and
        xmx != "" and
        username != "" and
        appdata != "" and
        uuid != "" and
        access_token != ""
    ):  # 启动前检查参数

        if not is_found_ver(ver, appdata): return -1
        ver_json_f = open(f"{appdata}/versions/{ver}/{ver}.json", 'r')
        ver_json = json.loads(ver_json_f.read())
        ver_json_f.close()

        # 将包含artifact键的库解压到natives临时文件夹
        for lib in ver_json["libraries"]:
            if "classifiers" in lib["downloads"]:
                for n in lib["downloads"]:  # 直接将全平台的库都解压了，懒得做平台检测了
                    if n == "artifact":
                        dic_path = f"{appdata}/versions/{ver}/{ver}-natives"  # natives临时文件夹路径
                        file_path = f"{appdata}/libraries/{lib['downloads'][n]['path']}"  # 库
                        unzip(file_path, dic_path)
                    elif n == "classifiers":
                        for native in lib["downloads"][n].values():
                            dic_path = f"{appdata}/versions/{ver}/{ver}-natives"
                            file_path = f"{appdata}/libraries/{native['path']}"  # classifiers' path（突然发癫（）
                            unzip(file_path, dic_path)
        jvm += " "
        if "arguments" in ver_json:  # 新版json（>= 1.13）
            for arg in ver_json["arguments"]["jvm"]:
                if "value" in arg:
                    if type(arg["value"]) is list:
                        for a in arg["value"]:
                            jvm += f"{a} "
                    else:
                        jvm += f"{arg['value']} "
                    print(jvm)
        else:  # 旧版json（< 1.13）
            pass

    else:
        return -1

launch_mc("J:\\xixide\\PCL2.4.4\\.minecraft", "1.16.5",
          "J:\\xixide\\openjdk-17+35_windows-x64_bin\\jdk-17\\bin\\javaw.exe", "1024m", "114514", "Legacy",
          "{}", "{}")
