"""
This module allows a basic (save) file creation, loading and deletion interface, with (open source) secure encoding.\n
It also has a function for a list choice UI.\n
Use 'save_name = os.path.dirname(os.path.abspath(__file__)) + "/save*"' as the save name to save files in the current directory instead of the default path.
"""
__version__ = '1.8.2.1'

from numpy import random as npr


def _imput(ask="Num: "):
    """
    Input but only accepts whole numbers.
    """
    while True:
        try: return int(input(ask))
        except ValueError: print("Not number!")


def encode_save(save_file_lines, save_num=1, save_name="save*", save_ext="sav"):
    """
    Creates a file that has been encoded, from a list of strings.
    """
    from math import pi
    from base64 import b64encode

    f = open(f'{save_name.replace("*", str(save_num))}.{save_ext}', "wb")
    r = npr.RandomState(int(save_num * pi * 3853))
    encode_64 = r.randint(3, 10)
    for line in save_file_lines:
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
    from math import pi
    from base64 import b64decode

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


def manage_saves(file_data, max_saves=5, save_name="save*", save_ext="sav"):
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


def get_key(mode=0):
    """
    Function for detecting a keypress (mainly arrow keys)\n
    Returns a number depending on the key type (0-5), and -1 if msvcrt/getch was not found.\n
    Returned keys for numbers (0-5): [ESC][UP][DOWN][LEFT][RIGHT][ENTER]\n
    Depending on the mode, it ignores some keys:\n
    \t0: don't ignore
    \t1: ignore left/right
    \t2: ignore up/down
    """
    try:
        from msvcrt import getch
    except ModuleNotFoundError:
        input("\n\nmsvcrt MODULE NOT FOUND!\nTHIS MODULE IS WINDOWS ONLY!\n\n")
        return -1
    
    arrow = False
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


class Slider:
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a slider, with the section specifying it's characteristics.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol and symbol_empty][pre_value][value][post_value]
    """
    def __init__(self, section=range(10), value=0, pre_text="", symbol="#", symbol_empty="-", pre_value="", display_value=False, post_value="", multiline=False):
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
    When used as input in the options_ui function, it draws a multiple choice seletion, with the choices list specifying the choice names.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][choice name][pre_value][value][post_value]
    """
    def __init__(self, choices=["choice"], value=0, pre_text="", symbol="#", symbol_empty="-", pre_value="", display_value=False, post_value="", multiline=False):
        for x in range(len(choices)):
            choices[x] = str(choices[x])
        self.choices = list(choices)
        self.pre_text = str(pre_text)
        self.value = int(value)
        self.symbol = str(symbol)
        self.symbol_empty = str(symbol_empty)
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


def options_ui(elements, title=None, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right=""):
    """
    Prints the title and then a list of elements that the user can cycle between with the up and down arrows, and adjust with either the left and right arrow keys or the enter key depending on the input object type, and exit with Escape.\n
    Accepts mainly a list of objects (Slider, Choice and Toggle).\n
    if an element in the list is not one of these objects, the value will be printed, (or if it's None, the line will be blank) and cannot be selected.
    """
    
    selected = 0
    while type(elements[selected]) != Slider and type(elements[selected]) != Choice and type(elements[selected]) != Toggle:
        selected += 1
        if selected > len(elements) - 1:
            selected = 0
    key = -2    
    while key != 0:
        # render
        # clear screen
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if title != None:
            print(title + "\n")
        for x in range(len(elements)):
            if elements[x] == None:
                print()
            elif type(elements[x]) == Slider or type(elements[x]) == Choice or type(elements[x]) == Toggle:
                # common
                # icon
                if selected != x:
                    print(not_selected_icon, end="")
                else:
                    print(selected_icon, end="")
                # pre text
                if elements[x].multiline and elements[x].pre_text.find("\n") != -1:
                    if selected != x:
                        print(elements[x].pre_text.replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                    else:
                        print(elements[x].pre_text.replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                else:
                    print(elements[x].pre_text, end="")
                # current value display
                # slider
                if type(elements[x]) == Slider:
                    # bar
                    for y in elements[x].section:
                        if y >= elements[x].value:
                            print(elements[x].symbol_empty, end="")
                        else:
                            print(elements[x].symbol, end="")
                # choice
                if type(elements[x]) == Choice:
                    # current choice
                    if elements[x].multiline and elements[x].choices[elements[x].value].find("\n") != -1:
                        if selected != x:
                            print(elements[x].choices[elements[x].value].replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                        else:
                            print(elements[x].choices[elements[x].value].replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                    else:
                        print(elements[x].choices[elements[x].value], end="")
                # toggle
                if type(elements[x]) == Toggle:
                    # on/off
                    if elements[x].value == 0:
                        print(elements[x].symbol_off, end="")
                    else:
                        print(elements[x].symbol, end="")
                # (pre) value
                if type(elements[x]) == Slider or type(elements[x]) == Choice:
                    # pre value
                    if elements[x].multiline and elements[x].pre_value.find("\n") != -1:
                        if selected != x:
                            print(elements[x].pre_value.replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                        else:
                            print(elements[x].pre_value.replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                    else:
                        print(elements[x].pre_value, end="")
                    # value
                    if elements[x].display_value:
                        if type(elements[x]) == Slider:
                            print(elements[x].value, end="")
                        else:
                            print(f"{elements[x].value}/{len(elements[x].choices)}", end="")
                # common end
                # post value
                if elements[x].multiline and elements[x].post_value.find("\n") != -1:
                    if selected != x:
                        print(elements[x].post_value.replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                    else:
                        print(elements[x].post_value.replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                else:
                    print(elements[x].post_value, end="")
                # icon right
                if selected != x:
                    print(not_selected_icon_right)
                else:
                    print(selected_icon_right)
            else:
                print(elements[x])
        # move selection/change value
        actual_move = False
        while not actual_move:
            # to prevent useless screen re-render at slider
            actual_move = True
            # get key
            key = 5
            if type(elements[selected]) == Toggle:
                key = get_key(1)
            else:
                while key == 5:
                    key = get_key()
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
                    if type(elements[selected]) == Slider or type(elements[selected]) == Choice or type(elements[selected]) == Toggle:
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
                        if elements[selected].value >= len(elements[selected].choices) - 1:
                            elements[selected].value = 0
                    else:
                        elements[selected].value -= 1
                        if elements[selected].value < 0:
                            elements[selected].value = len(elements[selected].choices) - 1
            # toggle
            elif key == 5:
                elements[selected].value += 1
                elements[selected].value %= 2


class UI_list:
    def __init__(self, answers=["No", "Yes"], question=None, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right="", multiline=False, can_esc=False, menu_actions=[]):
        self.answers = list(answers)
        self.question = str(question)
        self.s_icon = str(selected_icon)
        self.icon = str(not_selected_icon)
        self.s_icon_r = str(selected_icon_right)
        self.icon_r = str(not_selected_icon_right)
        self.multiline = bool(multiline)
        self.can_esc = bool(can_esc)
        self.menu_actions = list(menu_actions)


    def display(self):
        """
        Prints the question and then the list of answers that the user can cycle between with the arrow keys and select with enter.\n
        Gives back a number from 0-n acording to the size of the list that was passed in.\n
        if the answer is None the line will be blank and cannot be selected. \n
        Multiline makes the "cursor" draw at every line if the text is multiline.\n
        Can_esc allows the user to press esc to exit the menu. In this case the function returns -1.\n
        If the menu_actions list is not empty, each element coresponds to an element in the answers list, and if the value is a function (or a list with a function as the 1. element, and arguments as the 2-n. element, including 1 or more dictionaries as **kwargs), it will run that function.\n
        If the function returns -1 the display function will instantly exit.\n
        If it is a UI_list object, the object's display function will be automaticly called.
        """
        while True:
            selected = 0
            while self.answers[selected] == None:
                selected += 1
                if selected > len(self.answers) - 1:
                    selected = 0
            key = 0
            while key != 5:
                # render
                # clear screen
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                if self.question != None:
                    print(self.question + "\n")
                for x in range(len(self.answers)):
                    if self.answers[x] != None:
                        if selected != x:
                            if self.multiline:
                                print(self.icon + self.answers[x].replace("\n", f"{self.icon_r}\n{self.icon}") + self.icon_r)
                            else:
                                print(self.icon + self.answers[x] + self.icon_r)
                        else:
                            if self.multiline:
                                print(self.s_icon + self.answers[x].replace("\n", f"{self.s_icon_r}\n{self.s_icon}") + self.s_icon_r)
                            else:
                                print(self.s_icon + self.answers[x] + self.s_icon_r)
                    else:
                        print()
                # answer select
                key = get_key(1)
                if self.can_esc and key == 0:
                    return -1
                while key == 0:
                    key = get_key(1)
                # move selection
                if key != 5:
                    while True:
                        if key == 2:
                            selected += 1
                            if selected > len(self.answers) - 1:
                                selected = 0
                        else:
                            selected -= 1
                            if selected < 0:
                                selected = len(self.answers) - 1
                        if self.answers[selected] != None:
                            break
            # menu actions
            if self.menu_actions != [] and selected < len(self.menu_actions) and self.menu_actions[selected] != None:
                # list
                if type(self.menu_actions[selected]) == list and len(self.menu_actions[selected]) >= 2:
                    lis = []
                    di = dict()
                    for elem in self.menu_actions[selected]:
                        if type(elem) == dict:
                            di.update(elem)
                        else:
                            lis.append(elem)
                    if lis[0](*lis[1:], **di) == -1:
                        return selected
                # normal function
                elif callable(self.menu_actions[selected]):
                    if self.menu_actions[selected]() == -1:
                        return selected
                # ui
                else:
                    # lazy back button
                    try:
                        self.menu_actions[selected].display
                    except AttributeError:
                        print("Option is not a UI_list object!")
                        return selected
                    else:
                        self.menu_actions[selected].display()
            else:
                return selected

# def over(a=5, b=1, c="def c", d="def d", e="def e", f="def f", g="def g"):
#     input(f"{a}, {b}, {c}, {d}, {e}, {f}")

# l3_0 = UI_list(["option 1", "option 2", "back"], "l3_0", can_esc=True, menu_actions=[[over, 15, "gfg", UI_list, {"d":"d"}, {"f":59}], [_imput, "nummm: "], None])
# l2_0 = UI_list(["option 1", "option 2", "l3_0", "back"], "l2_0", can_esc=True, menu_actions=[_imput, _imput, l3_0, None])
# l2_1 = UI_list(["option 1", "option 2", "back"], "l2_1", can_esc=True, menu_actions=[_imput, _imput, None])
# l2_2 = UI_list(["option 1", "option 2", "back"], "l2_2", can_esc=True, menu_actions=[_imput, _imput, None])
# l1_0 = UI_list(["option 1", "option 2", "l2_2", "back"], "l1_0", can_esc=True, menu_actions=[_imput, _imput, l2_2, None])
# l1_1 = UI_list(["option 1", "option 2", "l2_1", "l2_0", "back"], "l1_1", can_esc=True, menu_actions=[_imput, _imput, l2_1, l2_0, None])
# l0 = UI_list(["function", "l1_0", "l1_1", "Exit"], "Main menu", menu_actions=[_imput, l1_0, l1_1, None])
# l0.display()


def manage_saves_ui(file_data, max_saves=5, save_name="save*", save_ext="sav"):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save, with UI selection.\n
    Reads in file data as a 2D array where element 0 is the save file number, and element 1 is the array of strings read in from file reader.\n
    Returns the option the user selected:\n
    \t[0, x] = load, into x slot\n
    \t[1, x] = new file, into x slot\n
    """
    from os import remove

    in_main_menu = True
    while True:
        if len(file_data):
            if in_main_menu:
                in_main_menu = False
                option = UI_list(["New save", "Load/Delete save"], " Main menu").display()
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
                option = UI_list(list_data, " Level select").display()
                # load
                if option < len(file_data):
                    return [0, file_data[option][0]]
                # delete
                elif option == len(file_data) + 1:
                    list_data.pop(len(list_data) - 2)
                    delete_mode = True
                    while delete_mode and len(file_data) > 0:
                        option = UI_list(list_data, " Delete mode!", "X ", "  ", multiline=False).display()
                        if option != len(list_data) - 1:
                            sure = UI_list(["No", "Yes"], f" Are you sure you want to remove Save file {file_data[option][0]}?").display()
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
# print(UI_list(["\n1", "\n2", "\n3", None, None, None, "Back", None, None, "\n\n\nlol\n"], "Are you old?", "-->", "  #", "<--", "#  ", True).display())
# elements = []
# elements.append(Slider(13, 5, "\nslider test 1\n|", "#", "-", "|\n", True, "$\n", True))
# elements.append(None)
# elements.append("2. test")
# elements.append(Slider(range(2, 20, 2), 2, "slider test 2 |", "#", "-", "| ", True, "l"))
# elements.append(Choice(["h", "j\nt", "l", 1], 2, "choice test ", "X", "O", " lol ", True, "$", True))
# elements.append(Toggle(1, "toggle test ", post_value=" $"))
# options_ui(elements, "test", ">", selected_icon_right="<")
# for element in elements:
#     if type(element) == Slider or type(element) == Choice or type(element) == Toggle:
#         print(element.pre_text + str(element.value))