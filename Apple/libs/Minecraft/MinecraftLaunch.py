import json
import os
from os.path import join, exists
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


def splitting_string_into_list_by_char(string: str, character: str) -> list[str]:  # 把传入的字符串按照某个字符分割成一个列表
    return_list: list[str] = []
    char1: str = ''
    for char in string:
        if char == character:
            return_list.append(char1)
            char1 = ''
        else:
            char1 += char
    return_list.append(char1)
    return return_list


def is_new_json_f(ver_json_path: str) -> bool:  # 判断一个版本json文件是不是新格式
    try:
        with open(ver_json_path) as j:
            ver_json = json.loads(j.read())
        if "arguments" in ver_json:  # 新版json（>= 1.13）
            return True
        else:  # 旧版json（< 1.13）
            return False
    except UnicodeDecodeError:
        return -1


def is_forge_ver(ver_json_path: str) -> bool:  # 判断一个版本是不是安装了Forge
    try:
        with open(ver_json_path) as j:
            ver_j = json.loads(j.read())
        if is_new_json_f(ver_json_path):
            logging.info('[Launch]: Json格式为新版格式')
            if "net.minecraftforge" in ver_j["arguments"]["game"]:
                return True
            else:
                return False
        else:
            logging.info('[Launch]: Json格式为旧版格式')
            if "net.minecraftforge.fml.common.launcher.FMLTweaker" in ver_j["minecraftArguments"]:
                return True
            else:
                return False
    except UnicodeDecodeError:
        return -1


def is_found_ver(ver: str, appdata: str) -> bool:  # 检查版本是否存在
    if os.path.exists(f"{appdata}/versions/{ver}/{ver}.json"):
        return True
    else:
        return False


def launch_mc(launcher_version: str, appdata: str, ver: str, java_path: str, xmx: str, username: str, uuid: str,
              access_token: str, width: str="873", height: str="501"):  # 启动mc
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

        if is_new_json_f(f"{appdata}/versions/{ver}/{ver}.json"):  # 新版json（>= 1.13）
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
        else:  # 旧版json（< 1.13）
            for lib in ver_json["libraries"]:
                if "classifiers" in lib:
                    for n in lib:  # 直接将全平台的库都解压了，懒得做平台检测了
                        if n == "artifact":
                            dic_path = f"{appdata}/versions/{ver}/{ver}-natives"  # natives临时文件夹路径
                            file_path = f"{appdata}/libraries/{lib['downloads'][n]['path']}"  # 库
                            unzip(file_path, dic_path)
                        elif n == "classifiers":
                            for native in lib["downloads"][n].values():
                                dic_path = f"{appdata}/versions/{ver}/{ver}-natives"
                                file_path = f"{appdata}/libraries/{native['path']}"  # classifiers' path（突然发癫（）
                                unzip(file_path, dic_path)

        jvm: str = '"' + java_path + '" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow ' \
                                 '-Dfml.ignoreInvalidMinecraftCertificates=True -Dfml.ignorePatchDiscrepancies=True ' \
                                 '-Dlog4j2.formatMsgNoLookups=true'

        if is_new_json_f(f"{appdata}/versions/{ver}/{ver}.json"):  # 新版json（>= 1.13）
            for arg in ver_json['arguments']['jvm']:
                if isinstance(arg, str):
                    jvm += arg + " "
                elif isinstance(arg, dict):  # 无论是什么，只要是在大括号里括着的，都被python认为是字典类型
                    if isinstance(arg["value"], list):
                        for a in arg["value"]:
                            jvm += a + " "
                    elif isinstance(arg["value"], str):
                        jvm += arg["value"] + " "
        else:  # 旧版json（< 1.13）
            jvm += '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump ' + \
                   '-Dos.name="Windows 10" -Dos.version=10.0 -Djava.library.path="' + \
                   f"{appdata}/versions/{ver}/{ver}-natives" + \
                   f'" -Dminecraft.launcher.brand=Python ' + \
                   f'-Dminecraft.launcher.version={launcher_version} -cp'

        jvm = jvm.replace("${natives_directory}", f"\"{appdata}/versions/{ver}/{ver}-natives\"")
        jvm = jvm.replace("${launcher_name}", "Python")
        jvm = jvm.replace("${launcher_version}", launcher_version)
        jvm = jvm.replace("${classpath} ", "")
        jvm = jvm.replace("-XstartOnFirstThread ", "")
        jvm = jvm.replace("-Dos.name=Windows 10", "-Dos.name=\"Windows 10\"")

        classpath = '"'

        for library in ver_json['libraries']:  # 某个Forge tm把json格式改了，我说怎么启动不了，上网一搜才知道，现在重写的是适配
            lib_list = splitting_string_into_list_by_char(library["name"], ':')
            f_path = splitting_string_into_list_by_char(lib_list[0], '.')
            final_path = ''
            for p in f_path:
                final_path += f"{p}/"
            final_path += lib_list[1] + '/' + lib_list[2] + '/' + f"{lib_list[1]}-{lib_list[2]}.jar"
            classpath += f"{appdata}/libraries/{final_path};"
        for libraries in ver_json['libraries']:
            try:
                if not 'classifiers' in libraries['downloads']:
                    normal_lib_path = join(
                        join(appdata, "libraries"), libraries['downloads']['artifact']['path'])
                    if exists('C:\\Program Files (x86)'):  # 64位操作系统
                        if "3.2.1" in normal_lib_path:
                            continue
                        else:
                            classpath += normal_lib_path + ";"
                    else:  # 32位操作系统
                        if "3.2.2" in normal_lib_path:
                            continue
                        else:
                            classpath += normal_lib_path + ";"
            except Exception:
                try:
                    if not 'classifiers' in libraries:
                        normal_lib_path = join(
                            join(appdata, "libraries"), libraries['downloads']['artifact']['path'])
                        if exists('C:\\Program Files (x86)'):  # 64位操作系统
                            if "3.2.1" in normal_lib_path:
                                continue
                            else:
                                classpath += normal_lib_path + ";"
                        else:  # 32位操作系统
                            if "3.2.2" in normal_lib_path:
                                continue
                            else:
                                classpath += normal_lib_path + ";"
                except Exception:
                    pass

        classpath = set(splitting_string_into_list_by_char(classpath, ';'))
        cp: str = ''
        for c in classpath:
            cp += f"{c};"
            print(cp)
        cp = cp.replace('"', '')
        classpath = '"' + cp.lstrip(';')

        # 将客户端文件传入-cp参数
        classpath = classpath + f"{appdata}/versions/{ver}/{ver}.jar\""
        jvm = jvm.replace("-cp ", "")
        jvm += '-cp '
        # 设置最大运行内存
        jvm += ("" + classpath + f" -Xmn{str(int(xmx.replace('m', '')) / 4).replace('.', '').replace('0', '') + 'm'}"
                + " -Xmx" + xmx + ' -Xmn256m -Dlog4j.formatMsgNoLookups=true ')

        logging.info(f'[Launch]: JVM参数拼接完成')

        mc_args = ''
        mc_args += ver_json["mainClass"] + " "
        try:
            for arg in ver_json["arguments"]["game"]:
                if isinstance(arg, str):
                    mc_args += arg + " "
                elif isinstance(arg, dict):  # 无论是什么，只要是在大括号里括着的，都被python认为是字典类型
                    if isinstance(arg["value"], list):
                        for a in arg["value"]:
                            mc_args += a + " "
                    elif isinstance(arg["value"], str):
                        mc_args += arg["value"] + " "
        except Exception:
            mc_args += ver_json["minecraftArguments"]
        mc_args = mc_args.replace("${auth_player_name}", username)  # 玩家名称
        mc_args = mc_args.replace("${version_name}", ver)  # 版本名称
        mc_args = mc_args.replace("${game_directory}", '"' + appdata + '"')  # mc路径
        mc_args = mc_args.replace("${assets_root}", '"' + appdata + "\\assets\"")  # 资源文件路径
        mc_args = mc_args.replace("${game_assets}", '"' + appdata + "\\assets\"")  # 旧版资源文件路径
        mc_args = mc_args.replace("${assets_index_name}", ver_json["assetIndex"]["id"])  # 资源索引文件名称
        mc_args = mc_args.replace("${auth_uuid}", uuid)  # 没写微软登录,uuid空填
        mc_args = mc_args.replace("${auth_access_token}", access_token)  # 同上
        mc_args = mc_args.replace("${clientid}", ver)  # 客户端id
        mc_args = mc_args.replace("${auth_xuid}", "{}")  # 离线登录,不填
        mc_args = mc_args.replace("${user_type}", "msa")  # 用户类型,离线模式是Legacy
        mc_args = mc_args.replace("${version_type}", ver_json["type"])  # 版本类型
        mc_args = mc_args.replace("${resolution_width}", width)  # 窗口宽度
        mc_args = mc_args.replace("${resolution_height}", height)  # 窗口高度
        mc_args = mc_args.replace("-demo ", "")  # 去掉-demo参数，退出试玩版
        mc_args = mc_args.replace("---width", "--width")  # 可能多了一个短横线，给它去掉
        mc_args = mc_args.replace("${auth_session}", access_token)  # accessToken
        mc_args = mc_args.replace("${auth_session}", "")
        mc_args = mc_args.replace("--quickPlayPath ${quickPlayPath}", "").replace(
            "--quickPlaySingleplayer ${quickPlaySingleplayer}", "")
        mc_args = mc_args.replace("--quickPlayMultiplayer ${quickPlayMultiplayer}", "").replace(
            "--quickPlayRealms ${quickPlayRealms}", "")

        logging.info(f'[Launch]: 新版Game参数拼接完成')
        logging.info('[Launch]: 启动参数拼接完成')
        final_arg = (jvm + mc_args).replace("-cp-cp", "-cp")
        with open("Launch.bat", 'w') as l:
            l.write(final_arg)
        os.system("start /b .\\Launch.bat")
        return final_arg
    else:
        return -1

print(launch_mc("114", "J:\\xixide\\PCL2.4.4\\.minecraft", "rd-132211",
          "I:\\Java\\bin\\javaw.exe", "1024m",
          "114514", "FFFF", "FFFF"))
