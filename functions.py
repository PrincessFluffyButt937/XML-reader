import os

import xml.etree.ElementTree as ET
import xlsxwriter
from mode import SN, HU, HUC, TXT, XLS

from data import Data, Trace, ref_to_str      

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
            for charge in tree_root.findall("charge"):
                if "barc6" not in charge.attrib:
                    continue
                if charge.attrib["barc6"] in hu_list:
                    matches.append(f_path)
    return matches

#warning, function alters inputted err_dict -> no return
def add_error(err_dict, error_key, file_path):
    err_list = {
        "dateComplete": "Error, key 'dateComplete' is missing within the root of the XML. The file does not follow expected format.",
        "panel": "Error, XML file contains no 'panel' data. File is either incomplete, the data format is unexpected or there is no tracibility to be collected. ",
        "id": "Error, there is no identifiable 'id' key inside 'charge' to collect component data.",
        "barc1": "Error, 'barc1' key is missing. Component PN (part number) cannot be captured.",
        "barc6": "Error, 'barc6' key is missing. Component HU (handling unit) cannot be captured.",
        "barc2": "Error, 'barc2' key is missing. Component LC (lot code) cannot be captured."
        }
    if error_key not in err_dict:
        if error_key in err_list:
            err_dict[err_list[error_key]] = {file_path}
        else:
            err_dict[error_key] = {file_path}
    else:
        if error_key in err_list:
            err_dict[err_list[error_key]].add(file_path)
        else:
            err_dict[error_key].add(file_path)

def get_data_from_filename(file_name):
    split_name = file_name.split("-", maxsplit=2)
    if len(split_name) != 3:
        return "Error 'improper split' -> cannot extract SN + PB from filename."
    else:
        SN = split_name[0]
        PB = split_name[1]
        if len(SN) != 10 or len(PB) != 11:
            return "Error -> Unkown SN and PB formats from a filename."
        else:
            sn = split_name[0]
            pb = f"{split_name[1][0:9]}"
            rev = f"{split_name[1][9:]}"
            obj = Data(pb=pb, rev=rev)
            return obj, sn

def get_sn_tracibility(file_paths, error_report=False, verbose=False):
    #accepts absolute filepaths
    #returns a dictionary serial numbers paired with Data objects
    obj_data = {}
    error_data = {}
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        tup_obj = get_data_from_filename(file_name)

        #error handling (potentialy incompatible file)
        if isinstance(tup_obj, str):
            #file_obj is a error string here
            if error_report:
                add_error(error_data, tup_obj, file_path)
            continue
        
        file_obj = tup_obj[0]
        sn = tup_obj [1]
        if verbose:
            file_obj.file_path.add(file_path)

        #XML parsing starts here
        file_thee = ET.parse(file_path)
        tree_root = file_thee.getroot()
        #safety check
        if not "dateComplete" in tree_root.attrib:
            if error_report:
                add_error(error_data, "dateComplete", file_path)
            continue

        time_stamp = convert_time_stamp(tree_root.attrib["dateComplete"])
        file_obj.date = time_stamp
        #object added / updated in dictionary
        if not obj_data:
            obj_data[sn] = file_obj
        else:
            if sn not in obj_data:
                obj_data[sn] = file_obj
            else:
                obj_data[sn].update(file_obj)

        #refdes stores references in "panel" branch in format "id": references
        #required for pairing with actuall data stored in "charge" sections of xml
        refdes = {}
        for branch in tree_root:
            if branch.tag == "panel":
                for id in branch:
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
                #error handling for writing Trace object
                if "id" not in branch.attrib or "barc1" not in branch.attrib or "barc2" not in branch.attrib or "barc6" not in branch.attrib:
                    if error_report:
                        if "id" not in branch.attrib:
                            add_error(error_data, "id", file_path)
                        if "barc1" not in branch.attrib:
                            add_error(error_data, "barc1", file_path)
                        if "barc2" not in branch.attrib:
                            add_error(error_data, "barc2", file_path)
                        if "barc6" not in branch.attrib:
                            add_error(error_data, "barc6", file_path)
                    continue
                if branch.attrib["id"] == id:
                    pn = branch.attrib["barc1"]
                    hu = branch.attrib["barc6"]
                    lc = branch.attrib["barc2"]
                    trace_obj = Trace(pn, lc)
                    trace_obj.ref.update(references)

                    obj_data[sn].add_trace(hu, trace_obj)
    return obj_data, error_data

def get_sn(folder_path, file_path_list=[]):
    #accepts a list of absolute filepaths, exctracts sn numbers which are then used to find the rest of the mathing file not caught by hu_finder function.
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
        report = f"{report}SN: {sn}, {obj_dict[sn].to_text()}----------------------------------\n"
    with open(file_path, "a") as file:
        file.write(report)

def write_xcel(obj_dict, dest_path):
    row = 0
    file_mame = "Tracebility report.xlsx"
    file_path = get_filename(dest_path, file_mame, format=".xlsx")
    report = xlsxwriter.Workbook(file_path)
    sheet = report.add_worksheet("Data")
    #sheet fotmating
    sheet.set_column("A:A", 15)
    sheet.set_column("B:B", 15)
    sheet.set_column("C:C", 15)
    sheet.set_column("D:D", 15)
    sheet.set_column("E:E", 25)
    sheet.set_column("F:F", 40)
    sheet.set_column("G:G", 20)
    sheet.autofilter("A1:G1")
    header = report.add_format({"bold": True, "border": 5, "bg_color": "#00B0F0"})
    basic = report.add_format({"left": 1, "bottom": 1, "right": 1})
    #header writing
    sheet.write(row, 0, "Serial Number", header)
    sheet.write(row, 1, "Project/Rev.", header)
    sheet.write(row, 2, "Handling Unit", header)
    sheet.write(row, 3, "Part Number", header)
    sheet.write(row, 4, "Lot Code", header)
    sheet.write(row, 5, "References", header)
    sheet.write(row, 6, "Mounting Date", header)
    row += 1
    for sn in obj_dict:
        obj = obj_dict[sn]
        for hu in obj.trace:
            trace = obj.trace[hu]
            sheet.write(row, 0, sn, basic)
            sheet.write(row, 1, f"{obj.pb}/{obj.rev}", basic)
            sheet.write(row, 2, hu, basic)
            sheet.write(row, 3, trace.pn, basic)
            sheet.write(row, 4, trace.lc, basic)
            sheet.write(row, 5, ref_to_str(trace.ref), basic)
            sheet.write(row, 6, obj.date, basic)
            row += 1
    report.close()

def write_error_report(data, dest_path=""):
    if not dest_check(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    file_name = "Error report.txt"
    error_report = get_filename(dest_path, file_name, ".txt")
    with open(error_report, "a") as file:
        error_data = "-----------------ERROR_REPORT-----------------\n"
        if not data:
            error_data = error_data + "No expected error were registered by this script."
        else:
            for error in data:
                error_data = f"{error_data}{error}\nFile list:\n"
                for file_path in data[error]:
                    error_data = f"{error_data}{file_path}\n"
                error_data = error_data + "----------------------------------\n"
        file.write(error_data)

def search(inp_lst=[], path="", enum=None, error_report=False):
    if not inp_lst:
        return 10
    if enum in SN:
        paths = sn_finder(path, inp_lst)
        return get_sn_tracibility(paths, error_report)
    if enum in HU:
        paths = hu_finder(path, inp_lst)
        return get_sn_tracibility(paths, error_report)
    if enum in HUC:
        hu_paths = hu_finder(path, inp_lst)
        sn_full_path_list = get_sn(path, hu_paths)
        return get_sn_tracibility(sn_full_path_list, error_report)

def write(dest_path="", data={}, enum=None, error_dest="", errors={}, error_report=False):

    if not dest_check(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    if enum in TXT:
        write_txt(data, dest_path)
    if enum in XLS:
        write_xcel(data, dest_path)

    if error_report:
        write_error_report(errors, error_dest)