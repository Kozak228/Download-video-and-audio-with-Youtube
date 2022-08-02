from os import path, mkdir, chdir

def proverka_path(path_user, video):
    name_folder = "Відео" if video else "Аудіо"

    if path_user == "":
        path_file = path.abspath(__file__)

        path_file = path_file[:path_file.rindex("\\") + 1]

        path_file += name_folder

        if path.exists(path_file):
            path_file += "\\"
            chdir(path_file)
            return path_file
        else:
            mkdir(path_file)
            path_file += "\\"
            chdir(path_file)
            return path_file
    else:
        path_file = path_user

        path_file += f"\\{name_folder}"

        if path.exists(path_file):
            path_file += "\\"
            chdir(path_file)
            return path_file
        else:
            mkdir(path_file)
            path_file += "\\"
            chdir(path_file)
            return path_file