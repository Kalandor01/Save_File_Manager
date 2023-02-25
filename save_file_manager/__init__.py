"""
This module provides a basic (save) file creation, loading and deletion interface, with (open source) secure encoding.\n
It also has ojects/functions for displaying basic UI elements, like sliders, (toggle)buttons, and choice lists.
"""
__version__ = "1.15.3"


if __name__ == "__main__":
    from file_reader import FileReaderArgsError, file_reader, file_reader_s, file_reader_blank
    from file_conversion import encode_save, decode_save
    from cursor import Cursor_icon
    from ui_list import UI_list, UI_list_s, UI_list_button
    from options_ui import Base_UI, Choice, Slider, Toggle, Button, UINoSelectablesError, options_ui
    from save_manager import manage_saves, manage_saves_ui, manage_saves_ui_2
    from utils import get_key, Get_key_modes, Keys, imput, Keybinds, Key_action, get_key_with_obj
else:
    from save_file_manager.file_reader import FileReaderArgsError, file_reader, file_reader_s, file_reader_blank
    from save_file_manager.file_conversion import encode_save, decode_save
    from save_file_manager.cursor import Cursor_icon
    from save_file_manager.ui_list import UI_list, UI_list_s, UI_list_button
    from save_file_manager.options_ui import Base_UI, Choice, Slider, Toggle, Button, UINoSelectablesError, options_ui
    from save_file_manager.save_manager import manage_saves, manage_saves_ui, manage_saves_ui_2
    from save_file_manager.utils import get_key, Get_key_modes, Keys, imput, Keybinds, Key_action, get_key_with_obj


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
# print(test_save)
# print()
# decoded_save = decode_save()
# print(decoded_save)
# print(test_save == decoded_save)


# def over(a=5, b=1, c="def c", d="def d", e="def e", f="def f", g="def g"):
#     input(f"{a}, {b}, {c}, {d}, {e}, {f}")

# def mod(li:list[list]):
#     print(li)
#     if len(li[0]) == len(li[1]):
#         li[1].pop(-1)
#     li[0].pop(-1)
#     if len(li[0]) == 0:
#         return -1


# l3_0 = UI_list(["option 1", "option 2", "back"], "l3_0", can_esc=True, action_list=[[over, 15, "gfg", UI_list, {"d":"d"}, {"f":59}], [input, "nummm: "], None])
# l2_0 = UI_list(["option 1", "option 2", "l3_0", "back"], "l2_0", can_esc=True, action_list=[imput, imput, l3_0, None])
# l2_1 = UI_list(["option 1", "option 2", "back"], "l2_1", can_esc=True, action_list=[imput, imput, 0])
# l2_2 = UI_list(["option 1", "option 2", "back"], "l2_2", can_esc=True, action_list=[imput, imput, 0])
# l1_0 = UI_list(["option 1", "option 2", "l2_2", "back"], "l1_0", can_esc=True, action_list=[imput, imput, l2_2, 0])
# l1_1 = UI_list(["option 1", "option 2", "l2_1", "l2_0", "back"], "l1_1", can_esc=True, action_list=[imput, imput, l2_1, l2_0, None])
# l0 = UI_list(["function", "l1_0", "\nl1_1", "\nExit", "function", "l1_0\n", "l1_1", "Exit", "function", "l1_0", "l1_1", "Exit"], "Main menu", multiline=False, action_list=[mod, l1_0, l1_1, None], modify_list=True)

# l0.display()


def _test_run(new_method=True, max_saves=5, save_name="save*", save_ext="sav", is_file_encoded=True, can_exit=True):
    from typing import Literal
    
    # create files
    save = ["dude thing 42069", "áéűől4"]
    save_new = ["loading lol 69", "űűűűűűűűűűűűűűűűűűűűűűááááááááááááűáűáűááááááááá"]
    if is_file_encoded:
        encode_save(save, 1, save_name, save_ext)
        encode_save(save, 2, save_name, save_ext)
        encode_save(save, 4, save_name, save_ext)
    else:
        with open(f'{save_name.replace("*", str(1))}.{save_ext}', "w") as f:
            for line in save:
                f.write(line + "\n")
        with open(f'{save_name.replace("*", str(2))}.{save_ext}', "w") as f:
            for line in save:
                f.write(line + "\n")
        with open(f'{save_name.replace("*", str(4))}.{save_ext}', "w") as f:
            for line in save:
                f.write(line + "\n")
    
    # menu management
    if not new_method:
        while True:
            datas = file_reader(max_saves, save_name, save_ext, None, is_file_encoded)
            datas_merged:list[tuple[int, str | Literal[-1]]] = []
            for data in datas:
                lines = ""
                if data[1] != -1:
                    for line in data[1]:
                        lines += line
                    try: datas_merged.append((int(data[0]), lines))
                    except ValueError: pass
            status = manage_saves_ui(datas_merged, max_saves, save_name, save_ext, can_exit)
            if status[0] == -1:
                break
            elif status[0] == 1:
                input(f"NEW GAME!!! in {status[1]}")
                if is_file_encoded:
                    encode_save(save_new, status[1], save_name, save_ext)
                else:
                    with open(f'{save_name.replace("*", str(status[1]))}.{save_ext}', "w") as f:
                        for line in save_new:
                            f.write(line + "\n")
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
                if data[1] != -1:
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

# def lolno():
#     return False

# elements = []
# elements.append(Slider(13, 5, "\nslider test 1\n|", "#", "-", "|\n", True, "$\n", True))
# elements.append(None)
# elements.append("2. test")
# elements.append(Slider(range(2, 20, 2), 15, "slider test 2 |", "#", "-", "| ", True, "l"))
# elements.append(Choice(["h", "j\nt", "l", 1], 2, "choice test ", " lol ", True, "$", True))
# elements.append(Toggle(1, "toggle test ", post_value=" $"))
# elements.append(UI_list_s(["one"]))
# elements.append(UI_list_s(["two"]))
# elements.append(None)
# elements.append(UI_list_button("three", lolno))
# elements.append(Button("yes", lolno))
# elements.append(Button("hmmm", UI_list_s(["hm", "l"], "kk", can_esc=True)))

# acts = [
#     Key_action("quit", ["q"], [], [Get_key_modes.IGNORE_ESCAPE]),
#     Key_action("^", ["w"], [], [Get_key_modes.IGNORE_VERTICAL]),
#     Key_action("V", ["s"], [], [Get_key_modes.IGNORE_VERTICAL]),
#     Key_action("<", ["a"], [], [Get_key_modes.IGNORE_HORIZONTAL]),
#     Key_action("right lol", ["d"], [], [Get_key_modes.IGNORE_HORIZONTAL]),
#     Key_action("E", ["e"], [], [Get_key_modes.IGNORE_ENTER]),
# ]
# kb = Keybinds(acts, ["\xe0", "\x00"])
# result_list = ("quit", "^", "V", "<", "right lol", "E")

# print(options_ui(elements, "test", Cursor_icon(">", "<"), kb, False, result_list))

# for element in elements:
#     if isinstance(Base_UI, element):
#         print(element.pre_text + str(element.value))


# acts = [
#     Key_action(Keys.ESCAPE, ["\x1b"], [], [Get_key_modes.IGNORE_ESCAPE]),
#     Key_action(Keys.UP, [], ["H"], [Get_key_modes.IGNORE_VERTICAL]),
#     Key_action(Keys.DOWN, [], ["P"], [Get_key_modes.IGNORE_VERTICAL]),
#     Key_action(Keys.LEFT, [], ["K"], [Get_key_modes.IGNORE_HORIZONTAL]),
#     Key_action(Keys.RIGHT, [], ["M"], [Get_key_modes.IGNORE_HORIZONTAL]),
#     Key_action(Keys.ENTER, ["\r"], [], [Get_key_modes.IGNORE_ENTER]),
# ]
# kb = Keybinds(acts, ["\xe0", "\x00"])
# while True: print(get_key_with_obj([Get_key_modes.IGNORE_HORIZONTAL, Get_key_modes.IGNORE_ESCAPE], kb))
