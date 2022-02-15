"""
This module allows a basic (save) file creation, loading and deletion interface, with "secure" encoding support.
"""
__version__ = 'dev'

import numpy as np
import base64
import os


def imput(ask="Num: "):
    """
    Input but only accepts whole numbers.
    """
    while True:
        try: return int(input(ask))
        except ValueError: print("Not number!")


def encode_save(save_file=[], save_num=1, save_name="save*", save_ext="sav"):
    """
    Creates a file that has been encoded, from a list.
    """
    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "wb")
    r = np.random.RandomState(int(save_num * np.pi * 3853))
    encode_64 = r.randint(3, 10)
    for line in save_file:
        line_enc = str(line).encode("windows-1250")
        for _ in range(encode_64):
            line_enc = base64.b64encode(line_enc)
        line_enc = line_enc.decode("windows-1250")
        line_bytes = bytearray(line_enc, "utf-8")
        line_bytes_enc = bytearray("", "utf-8")
        for byte in line_bytes:
            line_bytes_enc.append(byte + r.randint(1, 134))
        line_bytes_enc.append(10)
        f.write(bytes(line_bytes_enc))
    f.close()


def decode_save(save_num=1, save_name="save*", save_ext="sav"):
    """
    Returns a list of strings, decoded fron the encoded file.
    """
    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "rb")
    lines = f.readlines()
    f.close()
    lis = []
    r = np.random.RandomState(int(save_num * np.pi * 3853))
    encode_64 = r.randint(3, 10)
    for bytes_enc in lines:
        line_bytes = bytearray("", "utf-8")
        for byte in bytes_enc:
            if byte != 10:
                line_bytes.append(byte - r.randint(1, 134))
        line_enc = line_bytes.decode("utf-8")
        line_enc = line_enc.encode("windows-1250")
        for _ in range(encode_64):
            line_enc = base64.b64decode(line_enc)
        line = line_enc.decode("windows-1250")
        lis.append(line)
    return lis


def file_reader(max_saves=5, write_out=False, save_name="save*", save_ext="sav", is_file_encoded=True):
    """
    Returns (encripted) data from all save files with the save file number.
    """
    file_data = []
    file_num = 0
    if write_out:
        print("\n")
    while max_saves > file_num:
        file_num += 1
        try:
            f = open(f'{save_name.replace("*", str(file_num))}.{save_ext}', "r")
            f.close()
        except FileNotFoundError:
            pass
        else:
            if is_file_encoded:
                data = decode_save(file_num, save_name, save_ext)
            else:
                data = []
                f = open(f'{save_name.replace("*", str(file_num))}.{save_ext}', "r")
                lines = f.readlines()
                f.close()
                for line in lines:
                    data.append(line.replace("\n", ""))
            file_data.append([file_num, data])
            if write_out:
                print(f"Save File {file_num}:")
                print(data)
                print("\n")
    return file_data


def manage_saves(file_data=[], max_saves=5, save_name="save*", save_ext="sav"):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save.\n
    Returns the option the user selected:\n
    \t[0, x] = load, into x slot\n
    \t[1, x] = new file, into x slot\n
    \t[-1] = deleted file
    """
    manage_exit = False
    while not manage_exit:
        if len(file_data):
            # get file range
            file_num = 0
            min_file_num = file_data[0][0]
            for data in file_data:
                if data[0] > file_num:
                    file_num = data[0]
                if data[0] < min_file_num:
                    min_file_num = data[0]
            option = imput(f"Select an option: -1: delete mode, 0: new file, {min_file_num}-{file_num}: load file: ")
            # delete
            if option == -1:
                option = imput(f"Select an option: 0: back, {min_file_num}-{file_num}: delete file: ")
                if min_file_num <= option <= file_num:
                    sure = input(f"Are you sure you want to remove Save file {option}?(Y/N): ")
                    if sure.upper() == "Y":
                        os.remove(f'{save_name.replace("*", str(option))}.{save_ext}')
                        manage_exit = True
            # new file
            elif option == 0:
                new_slot = 1
                for data in file_data:
                    if data[0] == new_slot:
                        new_slot += 1
                if new_slot <= max_saves:
                    return [1, new_slot]
                else:
                    fff = input(f"No empty save files! Delete a file to continue!")
            # load
            else:
                for data in file_data:
                    if data[0] == option:
                        return [0, option]
                print(f"Save file {option} doesn't exist!")
        else:
            fff = input(f"No save files!")
            return [1, 1]
    return [-1]


def default_run(max_saves=5, save_name="save*", save_ext="sav", write_out=True, is_file_encoded=True):
    save = ["bro dude 42069", "áéűől4"]
    save_new = ["loading lol 69", "űűűűűűűűűűűűűűűűűűűűűűááááááááááááűáűáűááááááááá"]
    if is_file_encoded:
        encode_save(save, 1, save_name, save_ext)
        encode_save(save, 2, save_name, save_ext)
        encode_save(save, 4, save_name, save_ext)
    else:
        f = open(f'{save_name.replace("*", str(1))}.{save_ext}', "w")
        for line in save:
            f.write(line + "\n")
        f.close()
        f = open(f'{save_name.replace("*", str(2))}.{save_ext}', "w")
        for line in save:
            f.write(line + "\n")
        f.close()
        f = open(f'{save_name.replace("*", str(4))}.{save_ext}', "w")
        for line in save:
            f.write(line + "\n")
        f.close()
    options_status = True
    while options_status:
        datas = file_reader(max_saves, write_out, save_name, save_ext, is_file_encoded)
        status = manage_saves(datas, max_saves, save_name, save_ext)
        if status[0] == 1 or status[0] == 0:
            options_status = False
    if status[0] == 1:
        fff = input(f"NEW GAME!!! in {status[1]}")
        if is_file_encoded:
            encode_save(save_new, status[1], save_name, save_ext)
        else:
            f = open(f'{save_name.replace("*", str(status[1]))}.{save_ext}', "w")
            for line in save_new:
                f.write(line + "\n")
            f.close()
    elif status[0] == 0:
        fff = input(f"LOADING SAVE {status[1]}!!!")


# default_run(5, "save*", "sav", True, False)

# test_save = ["test testtest 42096 éáőúűá", "line", "linelinesabnjvaqxcyvíbíxmywjefgsetiuruoúpőáűégfgk,v.mn.--m,1372864594"]
