from enum import Enum
import os
import pandas as pd

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
TEXT = {Mode.SN_TEXT_TXT, Mode.SN_TEXT_XLS, Mode.HU_TEXT_TXT, Mode.HU_TEXT_XLS, Mode.HUC_TEXT_TXT, Mode.HUC_TEXT_XLS}
PATH = {Mode.SN_PATH_TXT, Mode.SN_PATH_XLS, Mode.HU_PATH_TXT, Mode.HU_PATH_XLS, Mode.HUC_PATH_TXT, Mode.HUC_PATH_XLS}

#bound to be reworked
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

def input_file_check(command_str="", enum=None):
    if not command_str or not enum:
        return
    if command_str.endswith(".txt") and enum in TXT:
        return True
    elif command_str.endswith(".xlsx") and enum in XLS:
        return True
    else:
        return False

def sn_convert(entries=[]):
    converted = set()
    for entry in entries:
        temp = entry.strip()
        if entry:
            if temp.isdecimal() and len(temp) == 10:
                converted.add(temp)
    return list(converted)


def hu_convert(entries=[]):
    converted = set()
    for entry in entries:
        temp = entry.strip()
        if temp:
            if temp.isdecimal():
                if len(temp) > 12:
                    continue
                while len(temp) < 12:
                    temp = "0" + temp
                converted.add(temp)
    return list(converted)

def data_convertor(command_str=None, enum=None):
    if not command_str or not enum:
        return
    if enum in TEXT:
        lst = command_str.split(",")
        if enum in SN:
            return sn_convert(lst)
        if enum in HU:
            return hu_convert(lst)
    if enum in PATH:
        if enum in SN:
            return sn_convert(command_str)
        if enum in HU:
            return hu_convert(command_str)

def read_txt(file_path=""):
    #reads a file, exctracts numerical data and returns a list.
    if not file_path or not os.path.exists(file_path):
        return 1
    output = []
    with open(file_path, "r") as file:
        text = file.read()
        for line in text.split():
            if not line:
                continue
            temp = line.strip()
            if temp:
                output.append(temp)
    return output
    
    
def read_excel(file_path=""):
    if not file_path or not os.path.exists(file_path):
        return 1
    output = []
    df = pd.read_excel(file_path, index_col=None, header=None)
    temp_dict = df.to_dict("list")
    for key in temp_dict:
        for entry in temp_dict[key]:
            if not entry:
                continue
            temp = str(entry).strip()
            if temp:
                output.append(temp)
    return output