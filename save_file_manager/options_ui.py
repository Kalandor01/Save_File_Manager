from save_file_manager.cursor import Cursor_icon
from save_file_manager.ui_list import UI_list, UI_list_s
from save_file_manager.utils import get_key


class Base_UI:
    """
    Base class for all `options_ui` classes.\n
    Structure: [pre_text][#####][pre_value][value][post_value]
    """
    def __init__(self, value=0, pre_text="", pre_value="", display_value=False, post_value="", multiline=False):
        self.value:int = int(value)
        self.pre_text:str = str(pre_text)
        self.pre_value:str = str(pre_value)
        self.display_value:bool = bool(display_value)
        self.post_value:str = str(post_value)
        self.multiline:bool = bool(multiline)


class Slider(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a slider, with the section specifying it's characteristics.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol and symbol_empty][pre_value][value][post_value]
    """
    def __init__(self, section:int|range, value=0, pre_text="", symbol="#", symbol_empty="-", pre_value="", display_value=False, post_value="", multiline=False):
        super().__init__(value, pre_text, pre_value, display_value, post_value, multiline)
        if type(section) == range:
            self.section = section
        elif type(section) == int:
            self.section = range(section)
        else:
            raise TypeError
        self.symbol = str(symbol)
        self.symbol_empty = str(symbol_empty)


class Choice(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a multiple choice seletion, with the choice_list list specifying the choice names.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][choice name][pre_value][value][post_value]
    """
    def __init__(self, choice_list:list|range, value=0, pre_text="", pre_value="", display_value=False, post_value="", multiline=False):
        super().__init__(value, pre_text, pre_value, display_value, post_value, multiline)
        choice_list = [str(choice) for choice in choice_list]
        self.choice_list = list(choice_list)


class Toggle(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a field that is toggleable with the enter key.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol or symbol_off][post_value]
    """
    def __init__(self, value=0, pre_text="", symbol="on", symbol_off="off", post_value="", multiline=False):
        super().__init__(value, pre_text, "", False, post_value, multiline)
        self.symbol = str(symbol)
        self.symbol_off = str(symbol_off)


def options_ui(elements:list[Slider|Choice|Toggle|UI_list], title:str=None, cursor_icon:Cursor_icon=None, key_mapping=None):
    """
    Prints the title and then a list of elements that the user can cycle between with the up and down arrows, and adjust with either the left and right arrow keys or the enter key depending on the input object type, and exit with Escape.\n
    Accepts mainly a list of objects (Slider, Choice, Toggle (and UI_list)).\n
    if an element in the list is not one of these objects, the value will be printed, (or if it's None, the line will be blank) and cannot be selected.
    """
    if cursor_icon is None:
        cursor_icon = Cursor_icon()
    # icon groups
    s_icons = f"{cursor_icon.s_icon_r}\n{cursor_icon.s_icon}"
    icons = f"{cursor_icon.icon_r}\n{cursor_icon.icon}"
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
                txt += (cursor_icon.s_icon if selected == x else cursor_icon.icon)
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
                txt += (cursor_icon.s_icon_r if selected == x else cursor_icon.icon_r) + "\n"
            # UI_list
            elif type(element) == UI_list or type(element) == UI_list_s:
                # render
                if element.answer_list[0] != None:
                    if selected == x:
                        curr_icon = element.cursor_icon.s_icon
                        curr_icon_r = element.cursor_icon.s_icon_r
                    else:
                        curr_icon = element.cursor_icon.icon
                        curr_icon_r = element.cursor_icon.icon_r
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
                    if elements[selected].exclude_nones:
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