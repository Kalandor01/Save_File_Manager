from ui_list import UI_list
from file_reader import file_reader
from utils import _imput

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