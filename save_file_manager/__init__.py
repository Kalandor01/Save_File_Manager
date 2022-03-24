"""
This module allows a basic (save) file creation, loading and deletion interface, with (open source) secure encoding.\n
It also has a function for a list choice UI.\n
Use 'save_name = os.path.dirname(os.path.abspath(__file__)) + "/save*"' as the save name to save files in the current directory instead of the default path.
"""
__version__ = '1.6.3'

from numpy import random as npr


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
    from math import pi
    from base64 import b64encode

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


def manage_saves(file_data=[], max_saves=5, save_name="save*", save_ext="sav"):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save.\n
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


def get_key():
    """
    Function for detecting a keypress (mainly arrow keys)\n
    Returns a number depending on the key type (0-5), and -1 if msvcrt/getch was not found.\n
    Returned keys for numbers (0-5): [ESC][UP][DOWN][LEFT][RIGHT][ENTER]
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
        if arrow and key == b"H":
            return 1
        elif arrow and key == b"P":
            return 2
        elif arrow and key == b"K":
            return 3
        elif arrow and key == b"M":
            return 4
        elif key == b"\r":
            return 5
        arrow = False
        if key == b"\xe0" or key == b"\x00":
            arrow = True

class Slider:
    """
    Object for the slider_ui method\n
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


def slider_ui(sliders=["Template", Slider(pre_text="template", display_value=True)], title=None, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right=""):
    """
    Prints the title and then a list of sliders that the user can cycle between, and adjust with the arrow keys. Exit with enter.\n
    Accepts a list of mainly Slider objects.\n
    if an element in the list is not a slider object, it will be printed, (or if it's None, the line will be blank) and cannot be selected.
    """
    
    selected = 0
    while type(sliders[selected]) != Slider:
        selected += 1
        if selected > len(sliders) - 1:
            selected = 0
    key = 0    
    while key != 5:
        # render
        # clear screen
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if title != None:
            print(title + "\n")
        for x in range(len(sliders)):
            if sliders[x] == None:
                print()
            else:
                try:
                    # icon
                    if selected != x:
                        print(not_selected_icon, end="")
                    else:
                        print(selected_icon, end="")
                    # pre text
                    if sliders[x].multiline:
                        if selected != x:
                            print(sliders[x].pre_text.replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                        else:
                            print(sliders[x].pre_text.replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                    else:
                        print(sliders[x].pre_text, end="")
                    # bar
                    for y in sliders[x].section:
                        if y >= sliders[x].value:
                            print(sliders[x].symbol_empty, end="")
                        else:
                            print(sliders[x].symbol, end="")
                    # pre value
                    if sliders[x].multiline:
                        if selected != x:
                            print(sliders[x].pre_value.replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                        else:
                            print(sliders[x].pre_value.replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                    else:
                        print(sliders[x].pre_value, end="")
                    # value
                    if sliders[x].display_value:
                        print(sliders[x].value, end="")
                    # post value
                    if sliders[x].multiline:
                        if selected != x:
                            print(sliders[x].post_value.replace("\n", f"{not_selected_icon_right}\n{not_selected_icon}"), end="")
                        else:
                            print(sliders[x].post_value.replace("\n", f"{selected_icon_right}\n{selected_icon}"), end="")
                    else:
                        print(sliders[x].post_value, end="")
                    # icon right
                    if selected != x:
                        print(not_selected_icon_right)
                    else:
                        print(selected_icon_right)
                except AttributeError:
                    print(sliders[x])
        # slider select
        key = 0
        while key == 0:
            key = get_key()
        # move selection
        if 1 <= key <= 2:
            while True:
                if key == 2:
                    selected += 1
                    if selected > len(sliders) - 1:
                        selected = 0
                else:
                    selected -= 1
                    if selected < 0:
                        selected = len(sliders) - 1
                if type(sliders[selected]) == Slider:
                    break
        # move slider
        elif 3 <= key <= 4:
            while True:
                if key == 4:
                    if sliders[selected].value + sliders[selected].section.step <= sliders[selected].section.stop:
                        sliders[selected].value += sliders[selected].section.step
                else:
                    if sliders[selected].value - sliders[selected].section.step >= sliders[selected].section.start:
                        sliders[selected].value -= sliders[selected].section.step
                if type(sliders[selected]) == Slider:
                    break


class UI_list:
    def __init__(self, answers=["No", "Yes"], question=None, multiline=False, selected_icon=">", not_selected_icon=" ", selected_icon_right="", not_selected_icon_right=""):
        self.answers = list(answers)
        self.question = str(question)
        self.multiline = bool(multiline)
        self.s_icon = str(selected_icon)
        self.icon = str(not_selected_icon)
        self.s_icon_r = str(selected_icon_right)
        self.icon_r = str(not_selected_icon_right)


    def display(self):
        """
        Prints the question and then the list of answers that the user can cycle between with the arrow keys and select with enter.\n
        Gives back a number from 0-n acording to the size of the list that was passed in.\n
        if the answer is None the line will be blank and cannot be selected. \n
        Multiline makes the "cursor" draw at every line if the text is multiline.
        """
        
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
            key = get_key()
            while key != 1 and key != 2 and key != 5:
                key = get_key()
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
        return selected

def _menu_ui(layers=[]):
    """
    PROTOTYPE AND WRONG!!!
    """
    layers = []
    layers.append("LIST OBJECT HERE?! + FUNCTION?")
    
    while True:
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
                    option = UI_list(list_data, " Delete mode!", "X ", "  ").display()
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


def manage_saves_ui(file_data=[], max_saves=5, save_name="save*", save_ext="sav"):
    """
    Allows the user to pick between creating a new save, loading an old save and deleteing a save, with UI selection.\n
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
                        option = UI_list(list_data, " Delete mode!", "X ", "  ").display()
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
# print(UI_list(["\n1", "\n2", "\n3", None, None, None, "Back", None, None, "\n\n\nlol\n"], "Are you old?", True, "-->", "  #", "<--", "#  ").display())
# sliders = []
# sliders.append(Slider(13, 5, "\ntest 1\n|", "#", "-", "|\n", True, "$\n", True))
# sliders.append(None)
# sliders.append("2. test")
# sliders.append(Slider(range(2, 20, 2), 2, "test 2 |", "#", "-", "| ", True, "l"))
# sliders.append(Slider(range(8), 8, "test 3 |", "#", "-", "| ", True, "kg"))
# sliders.append(Slider())
# slider_ui(sliders, "test", ">", selected_icon_right="<")
# for slider in sliders:
#     try:
#         print(slider.pre_text + str(slider.value))
#     except AttributeError:
#         pass
