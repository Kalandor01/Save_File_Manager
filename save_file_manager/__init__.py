"""
This module allows a basic (save) file creation, loading and deletion interface, with (open source) secure encoding.\n
It also has a function for a displaying basic UI elements.\n
Use 'dir_name = os.path.dirname(os.path.abspath(__file__))' as the directory name to save files in the current directory instead of the default path.
"""
__version__ = "1.11.1"


def _imput(ask="Num: "):
    """
    Input but only accepts whole numbers.
    """
    while True:
        try: return int(input(ask))
        except ValueError: print("Not number!")


def encode_save(save_file_lines:list[str]|str, save_num=1, save_name="save*", save_ext="sav", encoding="windows-1250", version=2):
    """
    Creates a file that has been encoded, from a string or a list of strings.\n
    If `save_name` contains a "*", when creating the file, it will be replaced in the name by the `save_num`.\n
    version numbers:
    - 1: normal: weak
    - 2: secure: stronger
    - 3: super-secure: strogest (only works, if opened on the same location, with the same name)
    - 4: stupid secure: v3 but encription "expires" on the next day
    """
    from math import pi, sqrt
    from base64 import b64encode
    from numpy import random as npr

    def encode_line(line, r:npr.RandomState):
        encode_64 = r.randint(2, 5)
        # encoding into bytes
        line_enc = b""
        for line_char in str(line):
            try:
                line_enc += str(line_char).encode(encoding)
            except UnicodeEncodeError:
                line_enc += b"\x3f"
        # encode to base64 x times
        for _ in range(encode_64):
            line_enc = b64encode(line_enc)
        # back to text
        line_enc = line_enc.decode(encoding)
        # shuffling bytes
        line_bytes = bytearray(line_enc, "utf-8")
        line_bytes_enc = bytearray("", "utf-8")
        for byte in line_bytes:
            line_bytes_enc.append(byte + r.randint(-32, 134))
        # \n + write
        line_bytes_enc.append(10)
        return line_bytes_enc

    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "wb")
    rr = npr.RandomState(int(sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi)) % 2**32))
    if type(save_file_lines) == str:
        save_file_lines = [save_file_lines]
    # v1
    if version == 1:
        f.write(bytes(encode_line(1, rr)))
        f.write(bytes(encode_line(-1, rr)))
        rr = npr.RandomState(int(sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi)) % 2**32))
        for line in save_file_lines:
            encoded_line = encode_line(line, rr)
            f.write(bytes(encoded_line))
    else:
        from datetime import datetime
        f.write(bytes(encode_line(version, rr)))
        # v2
        if version == 2:
            seed_num = int(str(datetime.now()).replace(" ", "").replace("-", "").replace(".", "").replace(":", "")) / sqrt((save_num * pi)**17.42 * (0.587 + save_num * pi))
        # v3-4
        elif version == 3 or version == 4:
            import os.path
            path = os.path.dirname(os.path.abspath(__file__)) + f'{save_name.replace("*", str(save_num))}.{save_ext}'
            b_path = bytes(path, "utf-8")
            num_p = 1
            for by in b_path:
                num_p *= int(by)
                num_p = int(str(num_p).replace("0", ""))
            t_now = int(str(datetime.now()).replace(" ", "").replace("-", "").replace(".", "").replace(":", "")) / sqrt((save_num * pi)**1.42 * (0.587 + save_num * pi))
            seed_num = float(str(num_p * t_now).replace("0", "").replace("e+", "")) * 15439813
        else:
            seed_num = sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi))
        encoded_line = encode_line(seed_num, rr)
        # v4
        if version == 4:
            n = datetime.now()
            seed_num *= (n.year + n.month + n.day)
        seed = npr.RandomState(int(seed_num % 2**32))
        f.write(bytes(encoded_line))
        for line in save_file_lines:
            encoded_line = encode_line(line, seed)
            f.write(bytes(encoded_line))
    f.close()


def decode_save(save_num=1, save_name="save*", save_ext="sav", encoding="windows-1250", decode_until=-1):
    """
    Returns a list of strings, decoded fron the encoded file.\n
    If `save_name` contains a "*", when opening the file, it will be replaced in the name by the `save_num`.\n
    `decode_until` controlls how many lines the function should decode (strarting from the beggining, with 1).
    """
    from math import pi, sqrt
    from base64 import b64decode
    from numpy import random as npr

    def decode_line(line:list, r:npr.RandomState):
        encode_64 = r.randint(2, 5)
        line_bytes = bytearray("", "utf-8")
        for byte in line:
            if byte != 10:
                line_bytes.append(byte - r.randint(-32, 134))
        line_enc = line_bytes.decode("utf-8")
        line_enc = line_enc.encode(encoding)
        for _ in range(encode_64):
            line_enc = b64decode(line_enc)
        return line_enc.decode(encoding)

    # get version
    rr = npr.RandomState(int(sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi)) % 2**32))
    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "rb")
    version = int(decode_line(f.readline(), rr))
    seed_num = float(decode_line(f.readline(), rr))
    f.close()
    # decode
    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "rb")
    lines = f.readlines()
    f.close()
    lis = []
    if version == 4:
        from datetime import datetime
        n = datetime.now()
        seed_num *= (n.year + n.month + n.day)
    elif version < 2 or version > 4:
        seed_num = sqrt((save_num * pi)**7.42 * (3853.587 + save_num * pi))
    seed = npr.RandomState(int(seed_num % 2**32))
    for x in range(2, len(lines)):
        if decode_until > -1 and x >= decode_until + 2:
            break
        lis.append(decode_line(lines[x], seed))    
    return lis

# byte 0A = 10 is bad
# r.randint(1, 134)
# base_64_test = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
# test_save = ["test testtest 42096 éáőúűá", "line", "linelinesabnjvaqxcyvíbíxmywjefgsetiuruoúpőáűégfgk,v.mn.--m,1372864594"]
# test_save = ["a", "\n\n\n", "a", "\n\n\n", "a"]
# test_save = ["gfgfggfg", "1234567890", "\n", "", "léláéűűéőűúűűűűűűűűű", "ffffffffffffg", "f"]
# test_save = ["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789áűúőéóüöí0123456789/*-+,.-;>*?:_<>#&@{\\\"}<¤ß$ŁłÍ÷×¸¨"]
# test_save = [input("text:\n")]
# super edge case
# test_save = ["éá山ā人é口ŏ刀ā木ù日ì月è日女ǚ子ĭ馬马ǎ鳥鸟ǎ目ù水ǐǐì指事īī一ī二è三ā大à人天ā大小ǎ上à下à本ě木末"]
# encode_save(test_save, 1, version=3)
# print()
# decoded = decode_save()
# for d_line in decoded:
#     print(d_line)
# print()
# print(decode_save())


def file_reader(max_saves=5, save_name:str|None="save*", save_ext="sav", dir_name:str=None, is_file_encoded=True, decode_until=-1, save_num:int=None):
    """
    Gets data from all save files in a folder, and returns them in a format that save managers can read.\n
    Returns an array, where each element is an array, where the 1. element is the `save_num` or `save_name` (depending on witch one is not given) and the 2. is a list of decripted lines from the file.\n
    `max_saves`=-1 -> infinite max saves\n
    If an encrypted file is corrupted, the data will be replaced with -1\n
    decode_until controlls how many lines the function should decode (strarting from the beggining, with 1).\n
    If `save_name` is `None` and `save_num` is NOT `None` then the function will search for all files with the `save_ext` extension and tries to decode them with the `save_num` as the "seed".
    """
    from os import path, getcwd, listdir

    if dir_name == None:
        dir_name = getcwd()

    # setup vars
    if save_name != None:
        if save_name.find("*") != -1:
            save_name_post = save_name.split("*")[-1] + "." + save_ext
        else:
            save_name_post = "." + save_ext
    else:
        save_count = 0
    # get existing file numbers
    file_names = listdir(dir_name)
    existing_files = []
    for name in file_names:
        # get files by naming pattern
        if save_name != None:
            if path.isfile(path.join(dir_name, name)) and name.startswith(save_name.split("*")[0]) and name.endswith(save_name_post):
                try: file_number = int(name.replace(f".{save_ext}", "").replace(save_name.replace("*", ""), ""))
                except ValueError: continue
                if file_number <= max_saves or max_saves < 0:
                    existing_files.append(file_number)
        # get files by extension only
        elif save_num != None:
            if path.isfile(path.join(dir_name, name)) and name.endswith("." + save_ext):
                    existing_files.append(name)
                    if max_saves >= 0:
                        save_count += 1
                        if save_count >= max_saves:
                            break
        else:
            raise Exception('"save_name" and "save_num" can\'t both be None at the same time')
    existing_files.sort()

    # get file datas
    file_data = []
    for file in existing_files:
        try:
            if is_file_encoded:
                try:
                    if save_name != None:
                        data = decode_save(file, path.join(dir_name, save_name.replace("*", str(file))), save_ext, decode_until=decode_until)
                    else:
                        data = decode_save(save_num, path.join(dir_name, file.replace("." + save_ext, "")), save_ext, decode_until=decode_until)
                except ValueError:
                    data = -1
            else:
                data = []
                if save_name != None:
                    f = open(path.join(dir_name, f'{save_name.replace("*", str(file))}.{save_ext}'), "r")
                else:
                    f = open(path.join(dir_name, name), "r")
                lines = f.readlines()
                f.close()
                for line in lines:
                    data.append(line.replace("\n", ""))
        except FileNotFoundError: pass
        else:
            file_data.append([file, data])
    return file_data

def file_reader_s(save_name="save*", dir_name:str=None, decode_until=-1):
    """
    Short version of `file_reader`.\n
    file_reader(max_saves=-1, save_name, save_ext="sav", dir_name, is_file_encoded=True, decode_until, save_num=None)
    """
    return file_reader(max_saves=-1, save_name=save_name, save_ext="sav", dir_name=dir_name, is_file_encoded=True, decode_until=decode_until, save_num=None)

def file_reader_blank(save_num, dir_name:str=None, decode_until=-1):
    """
    Short version of `file_reader`, but for save files with different names, but same `save_num`s.\n
    file_reader(max_saves=-1, save_name=None, save_ext="sav", dir_name, is_file_encoded=True, decode_until, save_num)
    """
    return file_reader(max_saves=-1, save_name=None, save_ext="sav", dir_name=dir_name, is_file_encoded=True, decode_until=decode_until, save_num=save_num)


def manage_saves(file_data:list, max_saves=5, save_name="save*", save_ext="sav"):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save.\n
    Reads in file data as a 2D array where element 0 is the save file number, and element 1 is the array of strings read in from file reader.\n
    Returns the option the user selected:\n
    \t[0, x] = load, into x slot\n
    \t[1, x] = new file, into x slot\n
    \t[-1, x] = deleted file in x slot
    """
    from os import remove

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
                if new_slot <= max_saves or max_saves < 0:
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


def get_key(mode=0, key_map:list=None):
    """
    Function for detecting a keypress (mainly arrow keys)\n
    Returns a number depending on the key type (0-5).\n
    Throws an error if msvcrt/getch was not found. (this module is windows only)\n
    Returned keys for numbers (0-5): [ESC][UP][DOWN][LEFT][RIGHT][ENTER]\n
    Depending on the mode, it ignores some keys:\n
    \t0: don't ignore
    \t1: ignore left/right
    \t2: ignore up/down\n
    You can set custom keys keybinds by providing a key_map:\n
    [[list of keys in order (the 2. value in the list signals that the key gives back two keys (arrow keys))], [double key detector(s)]]\n
    key_map = [[[b"\\x1b"], [b"H", 1], [b"P", 1], [b"K", 1], [b"M", 1], [b"\\r"]], [b"\\xe0", b"\\x00"]]
    """
    try:
        from msvcrt import getch
    except ModuleNotFoundError:
        input("\n\nmsvcrt MODULE NOT FOUND!\nTHIS MODULE IS WINDOWS ONLY!\n\n")
        raise ModuleNotFoundError
    
    arrow = False
    if key_map == None:
        while True:
            key = getch()
            # print(key)
            if key == b"\x1b":
                return 0
            if arrow and mode != 2 and key == b"H":
                return 1
            elif arrow and mode != 2 and key == b"P":
                return 2
            elif arrow and mode != 1 and key == b"K":
                return 3
            elif arrow and mode != 1 and key == b"M":
                return 4
            elif key == b"\r":
                return 5
            arrow = False
            if key == b"\xe0" or key == b"\x00":
                arrow = True
    else:
        # key_map = [[[b"\x1b"], [b"H", 1], [b"P", 1], [b"K", 1], [b"M", 1], [b"\r"]], [b"\xe0", b"\x00"]]
        while True:
            key = getch()
            arrow = False
            if len(key_map) != 1 and key in key_map[1]:
                arrow = True
                key = getch()
            # print(key)
            if ((len(key_map[0][0]) == 1 and not arrow) or (len(key_map[0][0]) > 1 and arrow)) and key == key_map[0][0][0]:
                return 0
            elif ((len(key_map[0][1]) == 1 and not arrow) or (len(key_map[0][1]) > 1 and arrow)) and mode != 2 and key == key_map[0][1][0]:
                return 1
            elif ((len(key_map[0][2]) == 1 and not arrow) or (len(key_map[0][2]) > 1 and arrow)) and mode != 2 and key == key_map[0][2][0]:
                return 2
            elif ((len(key_map[0][3]) == 1 and not arrow) or (len(key_map[0][3]) > 1 and arrow)) and mode != 1 and key == key_map[0][3][0]:
                return 3
            elif ((len(key_map[0][4]) == 1 and not arrow) or (len(key_map[0][4]) > 1 and arrow)) and mode != 1 and key == key_map[0][4][0]:
                return 4
            elif ((len(key_map[0][5]) == 1 and not arrow) or (len(key_map[0][5]) > 1 and arrow)) and key == key_map[0][5][0]:
                return 5


class UI_list:
    """
    From the `display` function:\n
    Prints the `question` and then the list of answers from the `answer_list` that the user can cycle between with the arrow keys and select with enter.\n
    Gives back a number from 0-n acording to the size of the list that was passed in.\n
    If `exclude_none` is `True`, the selected option will not see non-selectable elements as part of the list. This also makes it so you don't have to put a placeholder value in the `action_list` for every `None` value in the `answer_list`.\n
    if the answer is None the line will be blank and cannot be selected. \n
    `multiline` makes the "cursor" draw at every line if the text is multiline.\n
    `can_esc` allows the user to press esc to exit the menu. In this case the function returns -1.\n
    If the `action_list` is not empty, each element coresponds to an element in the `answer_list`, and if the value is a function (or a list with a function as the 1. element, and arguments as the 2-n. element, including 1 or more dictionaries as **kwargs), it will run that function.\n
    - If the function returns -1 the `display` function will instantly exit.\n
    - If the function returns a list where the first element is -1 the `display` function will instantly return that list with the first element replaced by the selected element number of that `UI_list` object.\n
    - If it is a `UI_list` object, the object's `display` function will be automaticly called, allowing for nested menus.\n
    - If `modify_list` is `True`, any function (that is not a `UI_list` object) that is in the `action_list` will get a list containing the `answer_list` and the `action_list` as it's first argument (and can modify it) when the function is called.\n
    """
    
    def __init__(self, answer_list:list, question:str=None, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right="", multiline=False, can_esc=False, action_list:list=None, exclude_none=False, modify_list=False):
        answer_list = [(ans if ans == None else str(ans)) for ans in answer_list]
        self.answer_list = list(answer_list)
        self.question = str(question)
        self.s_icon = str(selected_icon)
        self.icon = str(not_selected_icon)
        self.s_icon_r = str(selected_icon_right)
        self.icon_r = str(not_selected_icon_right)
        self.multiline = bool(multiline)
        self.can_esc = bool(can_esc)
        if action_list == None:
            self.action_list = []
        else:
            self.action_list = list(action_list)
        self.exclude_none = exclude_none
        self.modify_list = bool(modify_list)

    def display(self, key_mapping=None):
        """
        Prints the `question` and then the list of answers from the `answer_list` that the user can cycle between with the arrow keys and select with enter.\n
        Gives back a number from 0-n acording to the size of the list that was passed in.\n
        If `exclude_none` is `True`, the selected option will not see non-selectable elements as part of the list. This also makes it so you don't have to put a placeholder value in the `action_list` for every `None` value in the `answer_list`.\n
        if the answer is None the line will be blank and cannot be selected. \n
        `multiline` makes the "cursor" draw at every line if the text is multiline.\n
        `can_esc` allows the user to press esc to exit the menu. In this case the function returns -1.\n
        If the `action_list` is not empty, each element coresponds to an element in the `answer_list`, and if the value is a function (or a list with a function as the 1. element, and arguments as the 2-n. element, including 1 or more dictionaries as **kwargs), it will run that function.\n
        - If the function returns -1 the `display` function will instantly exit.\n
        - If the function returns a list where the first element is -1 the `display` function will instantly return that list with the first element replaced by the selected element number of that `UI_list` object.\n
        - If it is a `UI_list` object, the object's `display` function will be automaticly called, allowing for nested menus.\n
        - If `modify_list` is `True`, any function (that is not a `UI_list` object) that is in the `action_list` will get a list containing the `answer_list` and the `action_list` as it's first argument (and can modify it) when the function is called.\n
        """
        while True:
            selected = 0
            while self.answer_list[selected] == None:
                selected += 1
                if selected > len(self.answer_list) - 1:
                    selected = 0
            key = 0
            while key != 5:
                # render
                # clear screen
                txt = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                if self.question != None:
                    txt += self.question + "\n\n"
                for x in range(len(self.answer_list)):
                    if self.answer_list[x] != None:
                        if selected == x:
                            curr_icon = self.s_icon
                            curr_icon_r = self.s_icon_r
                        else:
                            curr_icon = self.icon
                            curr_icon_r = self.icon_r
                        txt += curr_icon + (self.answer_list[x].replace("\n", f"{curr_icon_r}\n{curr_icon}") if self.multiline else self.answer_list[x]) + f"{curr_icon_r}\n"
                    else:
                        txt += "\n"
                print(txt)
                # answer select
                key = get_key(1, key_mapping)
                if self.can_esc and key == 0:
                    return -1
                while key == 0:
                    key = get_key(1, key_mapping)
                # move selection
                if key != 5:
                    while True:
                        if key == 2:
                            selected += 1
                            if selected > len(self.answer_list) - 1:
                                selected = 0
                        else:
                            selected -= 1
                            if selected < 0:
                                selected = len(self.answer_list) - 1
                        if self.answer_list[selected] != None:
                            break
            # menu actions
            if self.exclude_none:
                selected_f = selected
                for x in range(len(self.answer_list)):
                    if self.answer_list[x] == None:
                        selected_f -= 1
                    if x == selected:
                        selected = selected_f
                        break
            if self.action_list != [] and selected < len(self.action_list) and self.action_list[selected] != None:
                # list
                if type(self.action_list[selected]) == list and len(self.action_list[selected]) >= 2:
                    lis = []
                    di = dict()
                    for elem in self.action_list[selected]:
                        if type(elem) == dict:
                            di.update(elem)
                        else:
                            lis.append(elem)
                    if self.modify_list:
                        func_return = lis[0]([self.answer_list, self.action_list], *lis[1:], **di)
                    else:
                        func_return = lis[0](*lis[1:], **di)
                    if func_return == -1:
                        return selected
                    elif type(func_return) == list and func_return[0] == -1:
                        func_return[0] = selected
                        return func_return
                # normal function
                elif callable(self.action_list[selected]):
                    if self.modify_list:
                        func_return = self.action_list[selected]([self.answer_list, self.action_list])
                    else:
                        func_return = self.action_list[selected]()
                    if func_return == -1:
                        return selected
                    elif type(func_return) == list and func_return[0] == -1:
                        func_return[0] = selected
                        return func_return
                # ui
                else:
                    # display function or lazy back button
                    try:
                        self.action_list[selected].display(key_mapping=key_mapping)
                    except AttributeError:
                        # print("Option is not a UI_list object!")
                        return selected
            else:
                return selected


class UI_list_s(UI_list):
    """
    Short version of `UI_list`.\n
    __init__(..., selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right="", ...)
    """
    def __init__(self, answer_list:list, question:str=None, multiline=False, can_esc=False, action_list:list=None, exclude_none=False, modify_list=False):
        answer_list = [(ans if ans == None else str(ans)) for ans in answer_list]
        self.answer_list = list(answer_list)
        self.question = str(question)
        self.s_icon = ">"
        self.icon = " "
        self.s_icon_r = ""
        self.icon_r = ""
        self.multiline = bool(multiline)
        self.can_esc = bool(can_esc)
        if action_list == None:
            self.action_list = []
        else:
            self.action_list = list(action_list)
        self.exclude_none = exclude_none
        self.modify_list = modify_list

# def over(a=5, b=1, c="def c", d="def d", e="def e", f="def f", g="def g"):
#     input(f"{a}, {b}, {c}, {d}, {e}, {f}")

# def mod(li:list):
#     li[0].pop(-1)
#     li[1].pop(-1)

# l3_0 = UI_list(["option 1", "option 2", "back"], "l3_0", can_esc=True, action_list=[[over, 15, "gfg", UI_list, {"d":"d"}, {"f":59}], [_imput, "nummm: "], None])
# l2_0 = UI_list(["option 1", "option 2", "l3_0", "back"], "l2_0", can_esc=True, action_list=[_imput, _imput, l3_0, None])
# l2_1 = UI_list(["option 1", "option 2", "back"], "l2_1", can_esc=True, action_list=[_imput, _imput, 0])
# l2_2 = UI_list(["option 1", "option 2", "back"], "l2_2", can_esc=True, action_list=[_imput, _imput, 0])
# l1_0 = UI_list(["option 1", "option 2", "l2_2", "back"], "l1_0", can_esc=True, action_list=[_imput, _imput, l2_2, 0])
# l1_1 = UI_list(["option 1", "option 2", "l2_1", "l2_0", "back"], "l1_1", can_esc=True, action_list=[_imput, _imput, l2_1, l2_0, None])
# l0 = UI_list(["function", "l1_0", "\nl1_1", "\nExit", "function", "l1_0\n", "l1_1", "Exit", "function", "l1_0", "l1_1", "Exit"], "Main menu", multiline=False, action_list=[mod, l1_0, l1_1, None], modify_list=True)

# l0.display()


class Slider:
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a slider, with the section specifying it's characteristics.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol and symbol_empty][pre_value][value][post_value]
    """
    def __init__(self, section:int|range, value=0, pre_text="", symbol="#", symbol_empty="-", pre_value="", display_value=False, post_value="", multiline=False):
        if type(section) == range:
            self.section = section
        elif type(section) == int:
            self.section = range(section)
        else:
            raise TypeError
        self.pre_text = str(pre_text)
        self.value = int(value)
        self.symbol = str(symbol)
        self.symbol_empty = str(symbol_empty)
        self.pre_value = str(pre_value)
        self.display_value = bool(display_value)
        self.post_value = str(post_value)
        self.multiline = bool(multiline)


class Choice:
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a multiple choice seletion, with the choice_list list specifying the choice names.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][choice name][pre_value][value][post_value]
    """
    def __init__(self, choice_list:list|range, value=0, pre_text="", pre_value="", display_value=False, post_value="", multiline=False):
        choice_list = [str(choice) for choice in choice_list]
        self.choice_list = list(choice_list)
        self.pre_text = str(pre_text)
        self.value = int(value)
        self.pre_value = str(pre_value)
        self.display_value = bool(display_value)
        self.post_value = str(post_value)
        self.multiline = bool(multiline)


class Toggle:
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a field that is toggleable with the enter key.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol or symbol_off][post_value]
    """
    def __init__(self, value=0, pre_text="", symbol="on", symbol_off="off", post_value="", multiline=False):
        self.pre_text = str(pre_text)
        self.value = int(value)
        self.symbol = str(symbol)
        self.symbol_off = str(symbol_off)
        self.post_value = str(post_value)
        self.multiline = bool(multiline)


def options_ui(elements:list[Slider|Choice|Toggle|UI_list], title:str=None, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right="", key_mapping=None):
    """
    Prints the title and then a list of elements that the user can cycle between with the up and down arrows, and adjust with either the left and right arrow keys or the enter key depending on the input object type, and exit with Escape.\n
    Accepts mainly a list of objects (Slider, Choice, Toggle (and UI_list)).\n
    if an element in the list is not one of these objects, the value will be printed, (or if it's None, the line will be blank) and cannot be selected.
    """
    # icon groups
    s_icons = f"{selected_icon_right}\n{selected_icon}"
    icons = f"{not_selected_icon_right}\n{not_selected_icon}"
    # is toggle in list
    no_enter = True
    for element in elements:
        if type(element) == Toggle or type(element) == UI_list or type(element) == UI_list_s:
            no_enter = False
            break
    selected = 0
    while type(elements[selected]) != Slider and type(elements[selected]) != Choice and type(elements[selected]) != Toggle:
        selected += 1
        if selected > len(elements) - 1:
            selected = 0
    key = -2    
    while key != 0:
        # render
        # clear screen
        txt = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        if title != None:
            txt += title + "\n\n"
        for x in range(len(elements)):
            element = elements[x]
            if element == None:
                txt += "\n"
            # UI elements
            elif type(element) == Slider or type(element) == Choice or type(element) == Toggle:
                # common
                # icon
                txt += (selected_icon if selected == x else not_selected_icon)
                # pre text
                if element.multiline and element.pre_text.find("\n") != -1:
                    txt += element.pre_text.replace("\n", (s_icons if selected == x else icons))
                else:
                    txt += element.pre_text
                # current value display
                # slider
                if type(element) == Slider:
                    # bar
                    for y in element.section:
                        txt += (element.symbol_empty if y >= element.value else element.symbol)
                # choice
                if type(element) == Choice:
                    # current choice
                    if element.multiline and element.choice_list[element.value].find("\n") != -1:
                        txt += element.choice_list[element.value].replace("\n", (s_icons if selected == x else icons))
                    else:
                        txt += element.choice_list[element.value]
                # toggle
                if type(element) == Toggle:
                    # on/off
                    txt += (element.symbol_off if element.value == 0 else element.symbol)
                # (pre) value
                if type(element) == Slider or type(element) == Choice:
                    # pre value
                    if element.multiline and element.pre_value.find("\n") != -1:
                        txt += element.pre_value.replace("\n", (s_icons if selected == x else icons))
                    else:
                        txt += element.pre_value
                    # value
                    if element.display_value:
                        if type(element) == Slider:
                            txt += str(element.value)
                        else:
                            txt += f"{element.value}/{len(element.choice_list)}"
                # common end
                # post value
                if element.multiline and element.post_value.find("\n") != -1:
                    txt += element.post_value.replace("\n", (s_icons if selected == x else icons))
                else:
                    txt += element.post_value
                # icon right
                txt += (selected_icon_right if selected == x else not_selected_icon_right) + "\n"
            # UI_list
            elif type(element) == UI_list or type(element) == UI_list_s:
                # render
                if element.answer_list[0] != None:
                    if selected == x:
                        curr_icon = element.s_icon
                        curr_icon_r = element.s_icon_r
                    else:
                        curr_icon = element.icon
                        curr_icon_r = element.icon_r
                    if element.multiline and element.answer_list[0].find("\n") != -1:
                        txt += curr_icon + element.answer_list[0].replace("\n", f"{curr_icon_r}\n{curr_icon}") + curr_icon_r + "\n"
                    else:
                        txt += curr_icon + element.answer_list[0] + curr_icon_r + "\n"
                else:
                    txt += "\n"
            else:
                txt += element + "\n"
        print(txt)
        # move selection/change value
        actual_move = False
        while not actual_move:
            # to prevent useless screen re-render at slider
            actual_move = True
            # get key
            key = 5
            if type(elements[selected]) == Toggle or type(elements[selected]) == UI_list or type(elements[selected]) == UI_list_s:
                key = get_key(1, key_mapping)
            else:
                while key == 5:
                    key = get_key(0, key_mapping)
                    if key == 5 and no_enter:
                        key = 0
            # move selection
            if 1 <= key <= 2:
                while True:
                    if key == 2:
                        selected += 1
                        if selected > len(elements) - 1:
                            selected = 0
                    else:
                        selected -= 1
                        if selected < 0:
                            selected = len(elements) - 1
                    if type(elements[selected]) == Slider or type(elements[selected]) == Choice or type(elements[selected]) == Toggle or type(elements[selected]) == UI_list or type(elements[selected]) == UI_list_s:
                        break
            # move slider/choice
            elif 3 <= key <= 4:
                if type(elements[selected]) == Slider:
                    if key == 4:
                        if elements[selected].value + elements[selected].section.step <= elements[selected].section.stop:
                            elements[selected].value += elements[selected].section.step
                        else:
                            actual_move = False
                    else:
                        if elements[selected].value - elements[selected].section.step >= elements[selected].section.start:
                            elements[selected].value -= elements[selected].section.step
                        else:
                            actual_move = False
                else:
                    if key == 4:
                        elements[selected].value += 1
                        if elements[selected].value >= len(elements[selected].choice_list):
                            elements[selected].value = 0
                    else:
                        elements[selected].value -= 1
                        if elements[selected].value < 0:
                            elements[selected].value = len(elements[selected].choice_list) - 1
            # toggle
            elif key == 5:
                if type(elements[selected]) == Toggle:
                    elements[selected].value += 1
                    elements[selected].value %= 2
                # UI_list
                elif type(elements[selected]) == UI_list or type(elements[selected]) == UI_list_s:
                    # menu actions
                    if elements[selected].exclude_none:
                        selected_f = selected
                        if elements[selected].answer_list[0] == None:
                            selected_f -= 1
                        if y == selected:
                            selected = selected_f
                    if elements[selected].action_list != [] and 0 < len(elements[selected].action_list) and elements[selected].action_list[0] != None:
                        # list
                        if type(elements[selected].action_list[0]) == list and len(elements[selected].action_list[0]) >= 2:
                            lis = []
                            di = dict()
                            for elem in elements[selected].action_list[0]:
                                if type(elem) == dict:
                                    di.update(elem)
                                else:
                                    lis.append(elem)
                            if elements[selected].modify_list:
                                func_return = lis[0]([elements[selected].answer_list, elements[selected].action_list], *lis[1:], **di)
                            else:
                                func_return = lis[0](*lis[1:], **di)
                            if func_return == -1:
                                return selected
                            elif type(func_return) == list and func_return[0] == -1:
                                func_return[0] = selected
                                return func_return
                        # normal function
                        elif callable(elements[selected].action_list[0]):
                            if elements[selected].modify_list:
                                func_return = elements[selected].action_list[0]([elements[selected].answer_list, elements[selected].action_list])
                            else:
                                func_return = elements[selected].action_list[0]()
                            if func_return == -1:
                                return selected
                            elif type(func_return) == list and func_return[0] == -1:
                                func_return[0] = selected
                                return func_return
                        # ui
                        else:
                            # display function or lazy back button
                            try:
                                elements[selected].action_list[selected].display(key_mapping=key_mapping)
                            except AttributeError:
                                # print("Option is not a UI_list object!")
                                return selected
                    else:
                        return selected


def manage_saves_ui(file_data, max_saves=5, save_name="save*", save_ext="sav", can_exit=False, key_mapping:list=None):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save, with UI selection.\n
    Reads in file data as a 2D array where element 0 is the save file number, and element 1 is the array of strings read in from file reader.\n
    Returns the option the user selected:\n
    \t[0, x] = load, into x slot\n
    \t[1, x] = new file, into x slot\n
    \t[-1, -1] = exit
    """
    from os import remove

    in_main_menu = True
    while True:
        if len(file_data):
            if in_main_menu:
                in_main_menu = False
                option = UI_list(["New save", "Load/Delete save"], " Main menu", can_esc=can_exit).display(key_mapping=key_mapping)
            else:
                option = 1
            # new file
            if option == 0:
                new_slot = 1
                for data in file_data:
                    if data[0] == new_slot:
                        new_slot += 1
                if new_slot <= max_saves or max_saves < 0:
                    return [1, new_slot]
                else:
                    input(f"No empty save files! Delete a file to continue!")
            elif option == -1:
                return [-1, -1]
            # load/delete
            else:
                # get data from file_data
                list_data = []
                for data in file_data:
                    list_data.append(f"{data[0]}. {data[1]}")
                list_data.append(None)
                list_data.append("Delete file")
                list_data.append("Back")
                option = UI_list(list_data, " Level select", can_esc=True).display(key_mapping)
                # load
                if option != -1 and option < len(file_data):
                    return [0, file_data[option][0]]
                # delete
                elif option == len(file_data) + 1:
                    list_data.pop(len(list_data) - 2)
                    delete_mode = True
                    while delete_mode and len(file_data) > 0:
                        option = UI_list(list_data, " Delete mode!", "X ", "  ", multiline=False, can_esc=True).display(key_mapping)
                        if option != -1 and option != len(list_data) - 1:
                            sure = UI_list(["No", "Yes"], f" Are you sure you want to remove Save file {file_data[option][0]}?", can_esc=True).display(key_mapping)
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


def manage_saves_ui_2(new_save_function:list, load_save_function:list, get_data_function:list=None, max_saves=5, save_name="save*", save_ext="sav", can_exit=False, key_mapping:str=None):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save, with UI selection.\n
    The new_save_function and the load_save_function run, when the user preforms these actions, and both WILL get the file number, that was refrenced as their first argument.\n
    The get_data_function should return a list with all of the save file data, similar to the file_redaer function.\n
    The first element of all function lists should allways be the function. All other elements will be treated as arguments for that function.
    """
    from os import remove

    def new_save_pre(new_func):
        file_data = get_data_function[0](*get_data_function[1:])
        new_slot = 1
        for data in file_data:
            if data[0] == new_slot:
                new_slot += 1
        if new_slot <= max_saves or max_saves < 0:
            new_func[0](new_slot, *new_func[1:])
        else:
            input(f"No empty save files! Delete a file to continue!")

    def load_or_delete(load_func):
        while True:
            # get data from file_data
            file_data = get_data_function[0](*get_data_function[1:])
            list_data = []
            for data in file_data:
                list_data.append(f"{data[0]}. {data[1]}")
                list_data.append(None)
            list_data.append("Delete file")
            list_data.append("Back")
            option = UI_list(list_data, " Level select", can_esc=True).display(key_mapping)
            # load
            if option != -1 and option / 2 < len(file_data):
                load_func[0](file_data[int(option / 2)][0], *load_func[1:])
            # delete
            elif option / 2 == len(file_data):
                list_data.pop(len(list_data) - 2)
                delete_mode = True
                while delete_mode and len(file_data) > 0:
                    option = UI_list(list_data, " Delete mode!", "X ", "  ", multiline=False, can_esc=True).display(key_mapping)
                    if option != -1 and option != len(list_data) - 1:
                        option = int(option / 2)
                        sure = UI_list(["No", "Yes"], f" Are you sure you want to remove Save file {file_data[option][0]}?", can_esc=True).display(key_mapping)
                        if sure == 1:
                            remove(f'{save_name.replace("*", str(file_data[option][0]))}.{save_ext}')
                            list_data.pop(option)
                            list_data.pop(option)
                            file_data.pop(option)
                    else:
                        delete_mode = False
                if len(file_data) == 0:
                    input(f"\n No save files detected!")
                    new_save_function[0](1, *new_save_function[1:])
            else:
                break
    
    # actual function
    # get_fuction default
    if get_data_function == None:
        get_data_function = [file_reader, max_saves, save_name, save_ext]
    file_data = get_data_function[0](*get_data_function[1:])
    # main
    if len(file_data):
        option = UI_list(["New save", "Load/Delete save"], " Main menu", can_esc = can_exit, action_list = [[new_save_pre, new_save_function], [load_or_delete, load_save_function]]).display(key_mapping)
        if option == -1:
            return -1
    else:
        input(f"\n No save files detected!")
        new_save_function[0](1, *new_save_function[1:])



def _test_run(new_method=True, max_saves=5, save_name="save*", save_ext="sav", is_file_encoded=True, can_exit=True):
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
    if not new_method:
        while True:
            datas = file_reader(max_saves, save_name, save_ext, None, is_file_encoded)
            datas_merged = []
            for data in datas:
                lines = ""
                for line in data[1]:
                    lines += line
                datas_merged.append([data[0], lines])
            status = manage_saves_ui(datas_merged, max_saves, save_name, save_ext, can_exit)
            if status[0] == -1:
                break
            elif status[0] == 1:
                input(f"NEW GAME!!! in {status[1]}")
                if is_file_encoded:
                    encode_save(save_new, status[1], save_name, save_ext)
                else:
                    f = open(f'{save_name.replace("*", str(status[1]))}.{save_ext}', "w")
                    for line in save_new:
                        f.write(line + "\n")
                    f.close()
            else:
                input(f"LOADING SAVE {status[1]}!!!")
    else:
        def neww(num, new_data):
            input(f"NEW GAME!!! in {num}")
            encode_save(new_data, num)
            # INFINITE max saves ?

        def loadd(num):
            input(f"LOADING SAVE {num}!!!")

        def gettt(max_saves_in, save_name_in, save_ext_in, is_file_encoded_in):
            datas = file_reader(max_saves_in, save_name_in, save_ext_in, None, is_file_encoded_in)
            datas_merged = []
            for data in datas:
                lines = ""
                for line in data[1]:
                    lines += line
                datas_merged.append([data[0], lines])
            return datas_merged

        # menu management
        while True:
            status = manage_saves_ui_2([neww, save_new], [loadd], [gettt, max_saves, save_name, save_ext, is_file_encoded], max_saves, can_exit = can_exit)
            if status == -1:
                break

# _test_run(False, -1, "save*", "sav", True, True)

# print(UI_list(["\n1", "\n2", "\n3", None, None, None, "Back", None, None, "\n\n\nlol\n"], "Are you old?", "-->", "  #", "<--", "#  ", True).display())

# elements = []
# elements.append(Slider(13, 5, "\nslider test 1\n|", "#", "-", "|\n", True, "$\n", True))
# elements.append(None)
# elements.append("2. test")
# elements.append(Slider(range(2, 20, 2), 2, "slider test 2 |", "#", "-", "| ", True, "l"))
# elements.append(Choice(["h", "j\nt", "l", 1], 2, "choice test ", " lol ", True, "$", True))
# elements.append(Toggle(1, "toggle test ", post_value=" $"))
# elements.append(UI_list_s(["one"]))
# elements.append(UI_list_s(["two"]))
# elements.append(None)
# elements.append(UI_list_s(["three"]))

# print(options_ui(elements, "test", ">", selected_icon_right="<"))

# for element in elements:
#     if type(element) == Slider or type(element) == Choice or type(element) == Toggle:
#         print(element.pre_text + str(element.value))
