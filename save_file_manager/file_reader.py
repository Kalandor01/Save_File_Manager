from typing import Literal
from save_file_manager.file_conversion import decode_save
# from file_conversion import decode_save


class FileReaderArgsError(Exception):
    """This exeption is raired if "save_name" and "save_num" are both None in file_reader"""
    pass


def file_reader(max_saves=5, save_name:str|None="save*", save_ext="sav", dir_name:str|None=None, is_file_encoded=True, decode_until=-1, save_num:int|None=None):
    """
    Gets data from all save files in a folder, and returns them in a format that save managers can read.\n
    Returns an array, where each element is an array, where the 1. element is the `save_num` or `save_name` (depending on witch one is not given) and the 2. is a list of decripted lines from the file.\n
    `max_saves`=-1 -> infinite max saves\n
    If an encrypted file is corrupted, the data will be replaced with -1\n
    decode_until controlls how many lines the function should decode (strarting from the beggining, with 1).\n
    If `save_name` is `None` and `save_num` is NOT `None` then the function will search for all files with the `save_ext` extension and tries to decode them with the `save_num` as the "seed".
    """
    from os import path, getcwd, listdir

    if dir_name is None:
        dir_name = getcwd()

    # setup vars
    save_name_post = ""
    save_count = 0
    if save_name is not None:
        if save_name.find("*") != -1:
            save_name_post = save_name.split("*")[-1] + "." + save_ext
        else:
            save_name_post = "." + save_ext
    # get existing file numbers
    file_names = listdir(dir_name)
    existing_files:list[str] = []
    for name in file_names:
        # get files by naming pattern
        if save_name is not None:
            if path.isfile(path.join(dir_name, name)) and name.startswith(save_name.split("*")[0]) and name.endswith(save_name_post):
                try: file_number = int(name.replace(f".{save_ext}", "").replace(save_name.replace("*", ""), ""))
                except ValueError: continue
                if file_number <= max_saves or max_saves < 0:
                    existing_files.append(str(file_number))
        # get files by extension only
        elif save_num is not None:
            if path.isfile(path.join(dir_name, name)) and name.endswith("." + save_ext):
                    existing_files.append(name)
                    if max_saves >= 0:
                        save_count += 1
                        if save_count >= max_saves:
                            break
        else:
            raise FileReaderArgsError('"save_name" and "save_num" can\'t both be None at the same time')
    existing_files.sort()

    # get file datas
    file_data:list[tuple[str, list[str]|Literal[-1]]] = []
    data:list[str]|Literal[-1] =  []
    for file in existing_files:
        try:
            if is_file_encoded:
                try:
                    if save_name is not None:
                        data = decode_save(int(file), path.join(dir_name, save_name.replace("*", str(file))), save_ext, decode_until)
                    elif save_num is not None:
                        data = decode_save(save_num, path.join(dir_name, file.replace("." + save_ext, "")), save_ext, decode_until)
                except ValueError:
                    data = -1
            else:
                data = []
                file_name = (file if save_name is None else f'{save_name.replace("*", str(file))}.{save_ext}')
                with open(path.join(dir_name, file_name), "r") as f:
                    lines = f.readlines()
                for line in lines:
                    data.append(line.replace("\n", ""))
        except FileNotFoundError: pass
        else:
            if save_name is not None:
                file_data.append((file, data))
            else:
                file_data.append((file.replace("." + save_ext, ""), data))
    return file_data


def file_reader_s(save_name="save*", dir_name:str|None=None, decode_until=-1):
    """
    Short version of `file_reader`.\n
    file_reader(max_saves=-1, save_name, save_ext="sav", dir_name, is_file_encoded=True, decode_until, save_num=None)
    """
    return file_reader(max_saves=-1, save_name=save_name, save_ext="sav", dir_name=dir_name, is_file_encoded=True, decode_until=decode_until, save_num=None)


def file_reader_blank(save_num, dir_name:str|None=None, decode_until=-1):
    """
    Short version of `file_reader`, but for save files with different names, but same `save_num`s.\n
    file_reader(max_saves=-1, save_name=None, save_ext="sav", dir_name, is_file_encoded=True, decode_until, save_num)
    """
    return file_reader(max_saves=-1, save_name=None, save_ext="sav", dir_name=dir_name, is_file_encoded=True, decode_until=decode_until, save_num=save_num)