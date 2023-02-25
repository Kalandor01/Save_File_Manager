from copy import deepcopy
from enum import Enum, auto
from typing import Any

try:
    from msvcrt import kbhit, getwch
except ModuleNotFoundError:
    raise ModuleNotFoundError("msvcrt module not found!\nThis module is windows only!")


class Get_key_modes(Enum):
    NO_IGNORE = auto()
    IGNORE_HORIZONTAL = auto()
    IGNORE_VERTICAL = auto()
    IGNORE_ESCAPE = auto()
    IGNORE_ENTER = auto()
    IGNORE_ARROWS = auto()
    ONLY_ARROWS = auto()



class Keys(Enum):
    ESCAPE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5


def get_key(mode:Get_key_modes=Get_key_modes.NO_IGNORE, key_map:tuple[list[list[list[str]]], list[str]]|None=None, allow_buffered_inputs=False):
    """
    Function for detecting a keypress (mainly arrow keys)\n
    Returns a value from the `Key` enum depending on the key type.\n
    If `allow_buffered_inputs` is `False`, if the user pressed some buttons before this function was called the function will not register those button presses.\n
    Depending on the mode, it ignores some keys:\n
    \tNO_IGNORE: don't ignore any key
    \tIGNORE_HORIZONTAL: ignore left/right
    \tIGNORE_VERTICAL: ignore up/down
    \tIGNORE_ESCAPE: ignore escape
    \tIGNORE_ENTER: ignore enter\n
    You can set custom keys keybinds by providing a key_map:\n
    [[a list for each value in the `Key` enum, with each list having 2 lists of keys (the 1. list containing the keys that aren't arrow keys, the 2. containing the ones that are)], [double (arrow) key 1. halfs]]\n
    Examles:\n
    \tdefault: ([[["\\x1b"]], [[], ["H"]], [[], ["P"]], [[], ["K"]], [[], ["M"]], [["\\r"]]], ["\\xe0", "\\x00"])
    \tarrow/WASD: ([[["\\x1b", "e"]], [["w"], ["H"]], [["s"], ["P"]], [["a"], ["K"]], [["d"], ["M"]], [["\\r", " "]]], ["\\xe0", "\\x00"])
    \tonly W, A, and D without setting the mode: ([[], [["w"]], [], [["a"]], [["d"]], []])
    \tunintended/compressed: ([["\\x1b"], [[], "H"], [[], "P"], [[], "K"], [[], "M"], ["\\r"]], "\\xe0\\x00")
    """
    
    ignore_list = [Get_key_modes.IGNORE_ESCAPE, Get_key_modes.IGNORE_VERTICAL, Get_key_modes.IGNORE_VERTICAL,
                   Get_key_modes.IGNORE_HORIZONTAL, Get_key_modes.IGNORE_HORIZONTAL, Get_key_modes.IGNORE_ENTER]
    response_list = [Keys.ESCAPE, Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT, Keys.ENTER]
    
    if not allow_buffered_inputs:
        while kbhit():
            getwch()

    arrow = False
    if key_map is None:
        key_map = ([[["\x1b"]], [[], ["H"]], [[], ["P"]], [[], ["K"]], [[], ["M"]], [["\r"]]], ["\xe0", "\x00"])
    while True:
        key = getwch()
        # print(key)
        arrow = False
        if len(key_map) != 1 and len(key_map) > 1 and key in key_map[1]:
            arrow = True
            key = getwch()
            # print("arrow", key)
        
        for x, response in enumerate(response_list):
            if ((not arrow and len(key_map[0][x]) > 0 and key in key_map[0][x][0]) or
                (arrow and len(key_map[0][x]) > 1 and key in key_map[0][x][1])) and mode != ignore_list[x]:
                return response


def imput(ask="Num: "):
    """Input but only accepts whole numbers."""
    while True:
        try: return int(input(ask))
        except ValueError: print("Not a number!")


class Key_action:
    """
    Object for `Keybinds` for `get_key_with_obj()`.\n
    If the current key_mode is in the `ignore_modes` tuple, the keypress will be ignores if it is a normal key and the key mode is in the first list, or it is an arrow key and the key mode is in the secound list.\n
    If a normal list is passed in, it will act as the ignore mode list for both normal and arrow keys. (IGNORE_ARROWS and ONLY_ARROWS is added automatically)\n
    Raises `ValueError` if both `normal_keys` and `arrow_keys` are empty lists.
    """
    def __init__(self, response:Any, normal_keys:list[str]|None=None, arrow_keys:list[str]|None=None, ignore_modes:list[Get_key_modes]|tuple[list[Get_key_modes], list[Get_key_modes]]|None=None):
        if normal_keys is None:
            normal_keys = []
        if arrow_keys is None:
            arrow_keys = []
        if len(normal_keys) == 0 and len(arrow_keys) == 0:
            raise ValueError("Both normal_keys and arrow_keys can't be empty lists.")
        self.normal_keys = normal_keys
        self.arrow_keys = arrow_keys
        if ignore_modes is None:
            ignore_modes_tuple:tuple[list[Get_key_modes], list[Get_key_modes]] = ([], [])
        elif type(ignore_modes) is list:
            ignore_modes_tuple = (deepcopy(ignore_modes), deepcopy(ignore_modes))
        else:
            ignore_modes_tuple = (deepcopy(ignore_modes[0]), deepcopy(ignore_modes[1]))
        ignore_modes_tuple[0].append(Get_key_modes.ONLY_ARROWS)
        ignore_modes_tuple[1].append(Get_key_modes.IGNORE_ARROWS)
        self.ignore_modes:tuple[list[Get_key_modes], list[Get_key_modes]] = ignore_modes_tuple
        self.response = response



class Keybinds:
    """
    Object for `get_key_with_obj()`.\n
    Raises `ValueError` if `actions` is an empty list.
    """
    def __init__(self, actions:list[Key_action], arrow_key_modifiers:list[str]|None=None):
        if len(actions) == 0:
            raise ValueError("actions can't be an empty list.")
        self._actions = actions
        if arrow_key_modifiers is None:
            arrow_key_modifiers = []
        self._arrow_key_modifiers = list(arrow_key_modifiers)



def get_key_with_obj(mode:Get_key_modes|list[Get_key_modes]=Get_key_modes.NO_IGNORE, keybinds:Keybinds|None=None, allow_buffered_inputs=False):
    """
    Function for detecting one key from a list of keypresses.\n
    Depending on the mode, it ignores some keys.\n
    Returns the `response` of the `Key_action` object that maches the key the user pressed.\n
    If `allow_buffered_inputs` is `False`, if the user pressed some buttons before this function was called the function will not register those button presses.\n
    """
    if type(mode) is Get_key_modes:
        mode_list:list[Get_key_modes] = [mode]
    else:
        mode_list = mode

    if keybinds is None:
        keybinds = Keybinds([
            Key_action(Keys.ESCAPE, ["\x1b"], [], [Get_key_modes.IGNORE_ESCAPE]),
            Key_action(Keys.UP, [], ["H"], [Get_key_modes.IGNORE_VERTICAL]),
            Key_action(Keys.DOWN, [], ["P"], [Get_key_modes.IGNORE_VERTICAL]),
            Key_action(Keys.LEFT, [], ["K"], [Get_key_modes.IGNORE_HORIZONTAL]),
            Key_action(Keys.RIGHT, [], ["M"], [Get_key_modes.IGNORE_HORIZONTAL]),
            Key_action(Keys.ENTER, ["\r"], [], [Get_key_modes.IGNORE_ENTER]),
        ], ["\xe0", "\x00"])
        

    if not allow_buffered_inputs:
        while kbhit():
            getwch()

    arrow = False
    while True:
        key = getwch()
        arrow = False
        if key in keybinds._arrow_key_modifiers:
            arrow = True
            key = getwch()
        
        for action in keybinds._actions:
            ignore = False
            for mod in mode_list:
                if mod in action.ignore_modes[int(arrow)]:
                    ignore = True
                    break
            if (not arrow and not ignore and key in action.normal_keys) or (arrow and not ignore and key in action.arrow_keys):
                return action.response
