import os

from enum import Enum

import xml.etree.ElementTree as ET
import xlsxwriter

from data import Data, Trace, ref_to_str

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

def get_script_mode(command_str):
    if len(command_str) != 4 or not command_str.startswith("-"):
        return f"Invalid mode format: {command_str}"
    s, h, c = False, False, False
    t, x = False, False
    r, p = False,
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
        

def dest_check(dest_path):
    if os.path.exists(dest_path):
        if os.path.isdir(dest_path):
            return True
        else:
            return False
    else:
        return False

def get_filename(dest_path, file_name, format=".txt"):
    #function check for whether filename already exists in folder. If so, a number is added to the file_name to avoid overwriting existing reports.
    #returns absolute paths
    file_path = os.path.join(dest_path, file_name)
    if not os.path.exists(file_path):
        return file_path
    else:
        counter = 1
        split_name = file_name.split(".")
        base_name = split_name[0]
        while True:
            temp = f"{base_name}({counter}){format}"
            temp_path = os.path.join(dest_path, temp)
            if os.path.exists(temp_path):
                counter += 1
            else:
                return temp_path

def is_xml(file_path):
    if  os.path.isfile(file_path) and file_path.endswith(".XML"):
        return True
    else:
        return False

def convert_time_stamp(time_stamp):
    if len(time_stamp) != 16:
        return "UnknownTimeFormat"
    else:
        return f"{time_stamp[6:8]}/{time_stamp[4:6]}/{time_stamp[0:4]} {time_stamp[8:10]}:{time_stamp[10:12]}:{time_stamp[12:14]}"

def time_filter(start, end, timestamp):
    timestamp = int(timestamp)
    #accepts time formats YYYYMMDD
    if timestamp >= start and timestamp <= end:
        return True
    else:
        return False

def get_timestamp_from_filename(filename):
    filename = "1513028976-PB30577001I-1-NO-PCB-BARCODE2545-20240405063324.XML"
    spl = filename.rsplit("-", maxsplit=1)
    if len(spl) != 2:
        return f"Error - unkown file format -> {filename}"
    time = spl[1].rstrip(".XML")
    if time.isdecimal() and len(time) == 14:
        return time[0:8]
    else:
        return f"Error - unkown time format -> {filename}"

def sn_finder(folder_path, sn_list):
    #returns a list of absolute filepaths of maches sn files
    #if folder is found, call this function recursively with updated path
    matches = []
    for entry in os.scandir(folder_path):
        file = entry.name
        f_path = os.path.join(folder_path, file)
        if is_xml(f_path):
            for sn in sn_list:
                if file.startswith(str(sn)):
                    matches.append(f_path)
        elif os.path.isdir(f_path):
            #recursive call further down the three
            rec_matches = sn_finder(f_path, sn_list)
            if rec_matches:
                matches.extend(rec_matches)
    return matches

def hu_finder(folder_path, hu_list):
    #returns a list of absolute filepaths of maches sn files
    #if folder is found, call this function recursively with updated path
    matches = []
    for entry in os.scandir(folder_path):
        file = entry.name
        f_path = os.path.join(folder_path, file)
        if os.path.isdir(f_path):
            rec_matches = hu_finder(f_path, hu_list)
            if rec_matches:
                matches.extend(rec_matches)
        elif is_xml(f_path):
            file_thee = ET.parse(f_path)
            tree_root = file_thee.getroot()
            for test in tree_root.findall("charge"):
                if test.attrib["barc6"] in hu_list:
                    matches.append(f_path)
    return matches

def get_data_from_filename(file_name):
    split_name = file_name.split("-", maxsplit=2)
    if len(split_name) != 3:
        sn = "Error"
        pb = None
        rev = None
        err = "Error 'improper split' -> cannot extract SN + PB from filename."
    else:
        SN = split_name[0]
        PB = split_name[1]
        if len(SN) != 10 or len(PB) != 11:
            sn = "Error"
            pb = None
            rev = None
            err["ERR"] = "Error -> Unkown SN and PB formats from a filename."
        else:
            sn = split_name[0]
            pb = f"{split_name[1][0:9]}"
            rev = f"{split_name[1][9:]}"
            err = None
    obj = Data(sn=sn, pb=pb, rev=rev, err=err)
    return obj

def get_sn_tracibility(file_paths):
    #accepts absolute filepaths
    obj_data = {}

    for file in file_paths:

        refdes = {}
        file_name = os.path.basename(file)
        file_obj = get_data_from_filename(file_name)
        file_obj.file_path.add(file)

        file_thee = ET.parse(file)
        tree_root = file_thee.getroot()
        #maybe loop over the tree instead of find()? what if multiple panels? - unlikely
        panel_branch = tree_root.find("panel")
        time_stamp = convert_time_stamp(tree_root.attrib["dateComplete"])

        sn = file_obj.sn
        if sn == "Error":
            if time_stamp.startswith("Err"):
                sn = file_name
            else:
                sn = time_stamp

        file_obj.date = time_stamp
        if not obj_data:
            obj_data[sn] = file_obj
        else:
            if sn not in obj_data:
                obj_data[sn] = file_obj
            else:
                obj_data[sn].update(file_obj)

        for id in panel_branch:
            ref_set = set()
            for ref in id:
                ref_set.add(ref.text)
            refdes[id.attrib["id"]] = ref_set
        #after this loop, IDs and references are stored in refdes dictionary for every single file -> ready to be paired with charges.
        for id in refdes:

            references = refdes[id]

            for branch in tree_root:
                if branch.tag == "panel":
                    continue
                if branch.attrib["id"] == id:
                    pn = branch.attrib["barc1"]
                    hu = branch.attrib["barc6"]
                    lc = branch.attrib["barc2"]
                    trace_obj = Trace(references, pn, lc)

                    obj_data[sn].add_trace(hu, trace_obj)

    #returns a dictionary serial numbers paired with Data objects
    #TEST this function!!!

    return obj_data

def get_sn(folder_path, file_path_list=[]):
    #accepts a list of filepaths, exctracts sn numbers which are then used to find the rest of the mathing file not caught by hu_finder functions.
    #optional function
    sn_list = set()
    for file_path in file_path_list:
        file_name = os.path.basename(file_path)
        sn = file_name.split("-", maxsplit=1)
        sn_list.add(sn[0])

    matching_file_paths = sn_finder(folder_path, list(sn_list))
    return matching_file_paths

def write_txt(obj_dict, dest_path):
    file_name ="Tracebility report.txt"
    file_path = get_filename(dest_path, file_name)
    report = "-----------------REPORT-----------------\n"
    for sn in obj_dict:
        print(obj_dict[sn].to_text())
        report = report + obj_dict[sn].to_text() + "----------------------------------\n"
    with open(file_path, "a") as file:
        file.write(report)



def write_xcel(obj_dict, dest_path):
    row = 0
    file_mame = "Tracebility report.xlsx"
    file_path = get_filename(dest_path, file_mame, format=".xlsx")
    report = xlsxwriter.Workbook(file_path)
    sheet = report.add_worksheet("Data")
    sheet.write(row, 0, "Serial Number")
    sheet.write(row, 1, "Project/Rev.")
    sheet.write(row, 2, "Handling Unit")
    sheet.write(row, 3, "Part Number")
    sheet.write(row, 4, "Lot Code")
    sheet.write(row, 5, "References")
    sheet.write(row, 6, "Mounting Date")
    row += 1
    for sn in obj_dict:
        obj = obj_dict[sn]
        for hu in obj.trace:
            trace = obj.trace[hu]
            sheet.write(row, 0, obj.sn)
            sheet.write(row, 1, f"{obj.pb}/{obj.rev}")
            sheet.write(row, 2, hu)
            sheet.write(row, 3, trace.pn)
            sheet.write(row, 4, trace.lc)
            sheet.write(row, 5, ref_to_str(trace.ref))
            sheet.write(row, 6, obj.date)
            row += 1
    report.close()
    