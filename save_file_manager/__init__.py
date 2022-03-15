"""
This module allows a basic (save) file creation, loading and deletion interface, with (open source) secure encoding.\n
It also has a function for a list choice UI.\n
Use 'save_name = os.path.dirname(os.path.abspath(__file__)) + "/save*"' as the save name to save files in the current directory instead of the default path.
"""
__version__ = '1.5.1'

from math import pi
from numpy import random as npr
from base64 import b64encode, b64decode
from os import remove


def _imput(ask="Num: "):
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
    r = npr.RandomState(int(save_num * pi * 3853))
    encode_64 = r.randint(3, 10)
    for line in save_file:
        line_enc = str(line).encode("windows-1250")
        for _ in range(encode_64):
            line_enc = b64encode(line_enc)
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
    r = npr.RandomState(int(save_num * pi * 3853))
    encode_64 = r.randint(3, 10)
    for bytes_enc in lines:
        line_bytes = bytearray("", "utf-8")
        for byte in bytes_enc:
            if byte != 10:
                line_bytes.append(byte - r.randint(1, 134))
        line_enc = line_bytes.decode("utf-8")
        line_enc = line_enc.encode("windows-1250")
        for _ in range(encode_64):
            line_enc = b64decode(line_enc)
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
    \t[-1, x] = deleted file in x slot
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
            option = _imput(f"Select an option: -1: delete mode, 0: new file, {min_file_num}-{file_num}: load file: ")
            # delete
            if option == -1:
                option = _imput(f"Select an option: 0: back, {min_file_num}-{file_num}: delete file: ")
                if min_file_num <= option <= file_num:
                    sure = input(f"Are you sure you want to remove Save file {option}?(Y/N): ")
                    if sure.upper() == "Y":
                        remove(f'{save_name.replace("*", str(option))}.{save_ext}')
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
                    input(f"No empty save files! Delete a file to continue!")
            # load
            else:
                for data in file_data:
                    if data[0] == option:
                        return [0, option]
                print(f"Save file {option} doesn't exist!")
        else:
            input(f"No save files!")
            return [1, 1]
    return [-1, option]


def list_ui(answers=["Yes", "No"], question=None, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right=""):
    """
    Prints the question and then the list of answers that the user can cycle between with the arrow keys and select with enter.\n
    Gives back a number from 0-n acording to the size of the list that was passed in.\n
    if the answer is None the line will be blank and cannot be selected. 
    """
    try:
        from msvcrt import getch
    except ModuleNotFoundError:
        input("\n\nmsvcrt MODULE NOT FOUND!\nTHIS MODULE IS WINDOWS ONLY!\n\n")
    
    selected = 0
    while answers[selected] == None:
        selected += 1
        if selected > len(answers) - 1:
            selected = 0
    action = -1    
    while action != 2:
        # render
        # clear screen
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if question != None:
            print(question + "\n")
        for x in range(len(answers)):
            if answers[x] != None:
                if selected != x:
                    print(not_selected_icon + answers[x] + not_selected_icon_right)
                else:
                    print(selected_icon + answers[x] + selected_icon_right)
            else:
                print()
        # answer select
        arrow = False
        action = -1
        while action == -1:
            key = getch()
            # b"\x1b" = esc
            # print(key)
            if arrow and key == b"P":
                action = 0
            elif arrow and key == b"H":
                action = 1
            elif key == b"\r":
                action = 2
            arrow = False
            if key == b"\xe0" or key == b"\x00":
                arrow = True
        # move selection
        if action != 2:
            while True:
                if action == 0:
                    selected += 1
                    if selected > len(answers) - 1:
                        selected = 0
                else:
                    selected -= 1
                    if selected < 0:
                        selected = len(answers) - 1
                if answers[selected] != None:
                    break
    return selected

def manage_saves_ui(file_data=[], max_saves=5, save_name="save*", save_ext="sav"):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save, with UI selection.\n
    Returns the option the user selected:\n
    \t[0, x] = load, into x slot\n
    \t[1, x] = new file, into x slot\n
    """
    in_main_menu = True
    while True:
        if len(file_data):
            if in_main_menu:
                in_main_menu = False
                option = list_ui(["New save", "Load/Delete save"], " Main menu")
            else:
                option = 1
            # new file
            if option == 0:
                new_slot = 1
                for data in file_data:
                    if data[0] == new_slot:
                        new_slot += 1
                if new_slot <= max_saves:
                    return [1, new_slot]
                else:
                    input(f"No empty save files! Delete a file to continue!")
            # load/delete
            else:
                # get data from file_data
                list_data = []
                for data in file_data:
                    list_data.append(f"{data[0]}. {data[1]}")
                list_data.append(None)
                list_data.append("Delete file")
                list_data.append("Back")
                option = list_ui(list_data, " Level select")
                # load
                if option < len(file_data):
                    return [0, file_data[option][0]]
                # delete
                elif option == len(file_data) + 1:
                    list_data.pop(len(list_data) - 2)
                    delete_mode = True
                    while delete_mode and len(file_data) > 0:
                        option = list_ui(list_data, " Delete mode!", "X ", "  ")
                        if option != len(list_data) - 1:
                            sure = list_ui(["No", "Yes"], f" Are you sure you want to remove Save file {file_data[option][0]}?")
                            if sure == 1:
                                remove(f'{save_name.replace("*", str(file_data[option][0]))}.{save_ext}')
                                list_data.pop(option)
                                file_data.pop(option)
                        else:
                            delete_mode = False
                # back
                else:
                    in_main_menu = True
        else:
            input(f"\n No save files detected!")
            return [1, 1]


def _test_run(max_saves=5, save_name="save*", save_ext="sav", write_out=True, is_file_encoded=True):
    # create files
    save = ["dude thing 42069", "áéűől4"]
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
    
    # menu management
    while True:
        datas = file_reader(max_saves, write_out, save_name, save_ext, is_file_encoded)
        datas_merged = []
        for data in datas:
            lines = ""
            for line in data[1]:
                lines += line
            datas_merged.append([data[0], lines])
        status = manage_saves_ui(datas_merged, max_saves, save_name, save_ext)
        if status[0] == 1:
            input(f"NEW GAME!!! in {status[1]}")
            # INFINITE max saves
            if len(datas) >= max_saves - 1:
                max_saves += 1
            if is_file_encoded:
                encode_save(save_new, status[1], save_name, save_ext)
            else:
                f = open(f'{save_name.replace("*", str(status[1]))}.{save_ext}', "w")
                for line in save_new:
                    f.write(line + "\n")
                f.close()
        elif status[0] == 0:
            input(f"LOADING SAVE {status[1]}!!!")


# _test_run(5, "save*", "sav", True, True)
# test_save = ["test testtest 42096 éáőúűá", "line", "linelinesabnjvaqxcyvíbíxmywjefgsetiuruoúpőáűégfgk,v.mn.--m,1372864594"]
# test_save = ["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/*-+,.-;>*?:_<>#&@{}<¤ß$ŁłÍ÷×¸¨"]
# print(list_ui(["1", "2", "3", None, None, None, "Back", None, None, "lol"], "Are you old?", "-->", "  #", "<--", "#  "))
