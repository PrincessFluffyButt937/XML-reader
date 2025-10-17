from enum import Enum

class Mode(Enum):
    #search mode__input mode__output format
    SN_TEXT_TXT = 1
    SN_TEXT_XLS = 2
    SN_PATH_TXT = 3
    SN_PATH_XLS = 4

    HU_TEXT_TXT = 5
    HUC_TEXT_TXT = 6
    HU_PATH_TXT = 7
    HUC_PATH_TXT = 8

    HU_TEXT_XLS = 9
    HUC_TEXT_XLS = 10
    HU_PATH_XLS = 11
    HUC_PATH_XLS = 12

SN = {Mode.SN_PATH_TXT, Mode.SN_PATH_XLS, Mode.SN_TEXT_TXT, Mode.SN_TEXT_XLS}
HU = {Mode.HU_PATH_TXT, Mode.HU_PATH_XLS, Mode.HU_TEXT_TXT, Mode.HU_TEXT_XLS, Mode.HUC_PATH_TXT, Mode.HUC_PATH_XLS, Mode.HUC_TEXT_TXT, Mode.HUC_TEXT_XLS}
TXT = {Mode.SN_PATH_TXT, Mode.SN_TEXT_TXT, Mode.HU_PATH_TXT, Mode.HU_TEXT_TXT, Mode.HUC_PATH_TXT, Mode.HUC_TEXT_TXT}
XLS = {Mode.SN_PATH_XLS, Mode.SN_TEXT_XLS, Mode.HU_PATH_XLS, Mode.HU_TEXT_XLS, Mode.HUC_PATH_XLS, Mode.HUC_TEXT_XLS}

def get_script_mode(command_str):
    if len(command_str) != 4 or not command_str.startswith("-"):
        return f"Invalid mode format: {command_str}"
    s, h, c = False, False, False
    t, x = False, False
    r, p = False, False
    for i in range(1, 4):
        if command_str[i] == "s":
            if h or c:
                return "Invalid mode \"s\" is not allowed to be selected together with either \"h\" or \"c\"."
            elif s:
                return "Invalid mode - \"s\" selected multiple times"
            else:
                s = True
        elif command_str[i] == "h":
            if s or c:
                return "Invalid mode \"h\" is not allowed to be selected together with either \"s\" or \"c\"."
            elif h:
                return "Invalid mode - \"h\" selected multiple times"
            else:
                h = True
        elif command_str[i] == "c":
            if s or h:
                return "Invalid mode \"c\" is not allowed to be selected together with either \"s\" or \"h\"."
            elif c:
                return "Invalid mode - \"c\" selected multiple times"
            else:
                c = True
        elif command_str[i] == "t":
            if x:
                return "Invalid mode \"t\" is not allowed to be selected together with \"x\"."
            elif t:
                return "Invalid mode - \"t\" selected multiple times"
            else:
                t = True  
        elif command_str[i] == "x":
            if t:
                return "Invalid mode \"x\" is not allowed to be selected together with \"t\"."
            elif x:
                return "Invalid mode - \"x\" selected multiple times"
            else:
                x = True  
        elif command_str[i] == "r":
            if p:
                return "Invalid mode \"r\" is not allowed to be selected together with \"p\"."
            elif r:
                return "Invalid mode - \"r\" selected multiple times"
            else:
                r = True  
        elif command_str[i] == "p":
            if r:
                return "Invalid mode \"p\" is not allowed to be selected together with \"r\"."
            elif p:
                return "Invalid mode - \"p\" selected multiple times"
            else:
                p = True  
        else:
            return f"Invalid mode: \"{command_str[i]}\" is not recognized by this script."
    #mode selection below
    #serial number search variants
    if s:
        if r:
            if t:
                return Mode.SN_TEXT_TXT
            if x:
                return Mode.SN_TEXT_XLS   
        if p:
            if t:
                return Mode.SN_PATH_TXT
            if x:
                return Mode.SN_PATH_XLS
    #handling unit search - partial variants
    if h:
        if r:
            if t:
                return Mode.HU_TEXT_TXT
            if x:
                return Mode.HU_TEXT_XLS  
        if p:
            if t:
                return Mode.HU_PATH_TXT
            if x:
                return Mode.HU_TEXT_XLS
    #handling unit search - complete variants
    if c:
        if r:
            if t:
                return Mode.HUC_TEXT_TXT
            if x:
                return Mode.HUC_TEXT_XLS  
        if p:
            if t:
                return Mode.HUC_PATH_TXT
            if x:
                return Mode.HUC_PATH_XLS

def input_file_check(command_str, enum):
    if command_str.endswith(".txt"):
        if enum in TXT:
            return True
        else:
            return False
    elif command_str.endswith(".xlsx"):
        if enum in XLS:
            return True
        else:
            return False
    else:
        return False

def raw_data_convertor(command_str, enum):
    pass