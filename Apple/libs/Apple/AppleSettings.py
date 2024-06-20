from AppleErrors import FilePathNotFoundException


def write_settings_into_path_file(file_path: str):
    if file_path is False: raise FilePathNotFoundException("File's path is not found")
    with open(file_path) as sf:
        sf.write()
