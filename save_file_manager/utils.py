
def get_key(mode=0, key_map:list[list]=None):
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


def _imput(ask="Num: "):
    """Input but only accepts whole numbers."""
    while True:
        try: return int(input(ask))
        except ValueError: print("Not number!")