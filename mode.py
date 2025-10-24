from enum import Enum
import os
import pandas as pd
import tomllib

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
HU = {Mode.HU_PATH_TXT, Mode.HU_PATH_XLS, Mode.HU_TEXT_TXT, Mode.HU_TEXT_XLS}
HUC = {Mode.HUC_PATH_TXT, Mode.HUC_PATH_XLS, Mode.HUC_TEXT_TXT, Mode.HUC_TEXT_XLS}
TXT = {Mode.SN_PATH_TXT, Mode.SN_TEXT_TXT, Mode.HU_PATH_TXT, Mode.HU_TEXT_TXT, Mode.HUC_PATH_TXT, Mode.HUC_TEXT_TXT}
XLS = {Mode.SN_PATH_XLS, Mode.SN_TEXT_XLS, Mode.HU_PATH_XLS, Mode.HU_TEXT_XLS, Mode.HUC_PATH_XLS, Mode.HUC_TEXT_XLS}
TEXT = {Mode.SN_TEXT_TXT, Mode.SN_TEXT_XLS, Mode.HU_TEXT_TXT, Mode.HU_TEXT_XLS, Mode.HUC_TEXT_TXT, Mode.HUC_TEXT_XLS}
PATH = {Mode.SN_PATH_TXT, Mode.SN_PATH_XLS, Mode.HU_PATH_TXT, Mode.HU_PATH_XLS, Mode.HUC_PATH_TXT, Mode.HUC_PATH_XLS}

HU_ALL = HU | HUC

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

def input_file_check(file_path="", enum=None):
    if file_path.endswith(".txt") and enum in TXT:
        return True
    elif file_path.endswith(".xlsx") and enum in XLS:
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

def data_convertor(input_str=None, enum=None):
    if enum in TEXT:
        lst = input_str.split(",")
        if enum in SN:
            return sn_convert(lst)
        if enum in HU_ALL:
            return hu_convert(lst)
    if enum in PATH:
        if enum in SN:
            return sn_convert(input_str)
        if enum in HU_ALL:
            return hu_convert(input_str)
    else:
        return 1

def read_txt(file_path=""):
    #reads a file, exctracts numerical data and returns a list.
    if not file_path or not os.path.exists(file_path):
        return 2
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
        return 2
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

def read_data(cmd_str="", enum=None):
    if not cmd_str or not enum:
        return 3
    if enum in PATH:
        temp_in = None
        if input_file_check(cmd_str, enum):
            if enum in TXT:
                txt_out = read_txt(cmd_str)
                return data_convertor(txt_out, enum)
            if enum in XLS:
                xls_out = read_excel(cmd_str)
                return data_convertor(xls_out, enum)
        else:
            return 4
    else:
        return data_convertor(cmd_str, enum)
    
def read_cfg(script_path=""):
    cfg_path = os.path.join(script_path, "config.toml")
    with open(cfg_path, "rb") as cfg:
        settings = tomllib.load(cfg)
        if not "output_path" in settings:
            print(
        '''
        Error, ouput_path paramenter is missing in config file.
        Please make sure to specify output_path = \"path/to/file\" within config.toml file.
        '''
        )
            return
        if not "search_path" in settings:
            print(
        '''
        Error, search_path paramenter is missing in config file.
        Please make sure to specify search_path = \"path/to/directory\" within config.toml file.
        '''
        )
            return
        return settings["output_path"], settings["search_path"]