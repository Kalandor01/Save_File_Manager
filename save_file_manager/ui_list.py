from cursor import Cursor_icon
from utils import get_key

class UI_list:
    """
    From the `display` function:\n
    Prints the `question` and then the list of answers from the `answer_list` that the user can cycle between with the arrow keys and select with enter.\n
    Gives back a number from 0-n acording to the size of the list that was passed in.\n
    If `exclude_nones` is `True`, the selected option will not see non-selectable elements as part of the list. This also makes it so you don't have to put a placeholder value in the `action_list` for every `None` value in the `answer_list`.\n
    if the answer is None the line will be blank and cannot be selected. \n
    `multiline` makes the "cursor" draw at every line if the text is multiline.\n
    `can_esc` allows the user to press esc to exit the menu. In this case the function returns -1.\n
    If the `action_list` is not empty, each element coresponds to an element in the `answer_list`, and if the value is a function (or a list with a function as the 1. element, and arguments as the 2-n. element, including 1 or more dictionaries as **kwargs), it will run that function.\n
    - If the function returns -1 the `display` function will instantly exit.\n
    - If the function returns a list where the first element is -1 the `display` function will instantly return that list with the first element replaced by the selected element number of that `UI_list` object.\n
    - If it is a `UI_list` object, the object's `display` function will be automaticly called, allowing for nested menus.\n
    - If `modify_list` is `True`, any function (that is not a `UI_list` object) that is in the `action_list` will get a list containing the `answer_list` and the `action_list` as it's first argument (and can modify it) when the function is called.\n
    """

    def __init__(self, answer_list:list, question:str=None, cursor_icon:Cursor_icon=None, multiline=False, can_esc=False, action_list:list=None, exclude_nones=False, modify_list=False):
        if cursor_icon is None:
            cursor_icon = Cursor_icon()
        answer_list = [(ans if ans == None else str(ans)) for ans in answer_list]
        self.answer_list = list(answer_list)
        self.question = str(question)
        self.cursor_icon = cursor_icon
        self.multiline = bool(multiline)
        self.can_esc = bool(can_esc)
        if action_list == None:
            self.action_list = []
        else:
            self.action_list = list(action_list)
        self.exclude_nones = exclude_nones
        self.modify_list = bool(modify_list)

    def display(self, key_mapping=None):
        """
        Prints the `question` and then the list of answers from the `answer_list` that the user can cycle between with the arrow keys and select with enter.\n
        Gives back a number from 0-n acording to the size of the list that was passed in.\n
        If `exclude_nones` is `True`, the selected option will not see non-selectable elements as part of the list. This also makes it so you don't have to put a placeholder value in the `action_list` for every `None` value in the `answer_list`.\n
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
                            curr_icon = self.cursor_icon.s_icon
                            curr_icon_r = self.cursor_icon.s_icon_r
                        else:
                            curr_icon = self.cursor_icon.icon
                            curr_icon_r = self.cursor_icon.icon_r
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
            if self.exclude_nones:
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
    __init__(answer_list, question, cursor_icon=None, multiline=False, can_esc, action_list=None, exclude_nones, modify_list=False)
    """
    def __init__(self, answer_list:list, question:str=None, can_esc=False, exclude_nones=False):
        super().__init__(answer_list, question, None, False, can_esc, None, exclude_nones, False)