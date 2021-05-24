import time
import os


def create_log_file(file=None, prefix="", extension=".txt"):
    dir_name = "Logs"
    sub_dir_name = dir_name + "\\" + time.strftime("%Y_%m_%d", time.localtime()) + " Лог ДЭПы"
    try:
        os.makedirs(sub_dir_name)
    except (OSError, AttributeError) as error:
        pass
    try:
        if file:
            file.close()
    except (OSError, NameError, AttributeError) as error:
        pass
    file_name_1 = sub_dir_name + "\\" + time.strftime("%Y_%m_%d %H-%M-%S ",
                                                    time.localtime()) + prefix + extension

    return file_name_1, sub_dir_name

def open_log_file(file_name_1):
    if file_name_1:
        try:
            file_1 = open(file_name_1, 'a')
        except (OSError, NameError, AttributeError) as error:
            pass
    pass
    return file_1

def close_log_file(file_1):
    if file_1:
        try:
            file_1.close()
            print('close')
        except (OSError, NameError, AttributeError) as error:
            pass
    pass

