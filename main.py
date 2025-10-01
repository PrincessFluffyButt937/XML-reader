import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

#enums for search modes?
from enum import Enum

# "panel" = hides references + their mounted IDs
# "charge" = actuall component data pairable to IDs

#"2025091504150200" - time format
#"2025 - year[0-3], 09 -month[4-5], 15 - day[6-7], 04 - hours[8-9], 15 - min[10-11] 02 - seconds[12-13] 00-??"

modes = ["SN", "HU", "Ref"]
out_formats = [".txt", ".xls"]

def is_xml(file_path):
    if  os.path.isfile(file_path) and file_path.endswith(".XML"):
        return True
    else:
        return False
    
def ref_key(ref):
    #creates key to for sorted()
    j = 0
    for i in range(0, len(ref)):
        if not ref[i].isdigit():
            j = i
        else:
            break
    key = ref[j:]
    while len(key) < 5:
        key = "0" + key
    return key

def ref_to_str(ref_set):
    #converts set of references to sorted string
    ref_list = sorted(list(ref_set), key=lambda ref: ref_key(ref))
    return str(ref_list).strip("[]").replace("'", "")

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
    files = os.listdir(folder_path)
    for file in files:
        f_path = os.path.join(folder_path, file)
        if is_xml(f_path):
            for sn in sn_list:
                if file.startswith(sn):
                    matches.append(f_path)
        elif os.path.isdir(f_path):
            #recursive call further down the three
            rec_matches = sn_finder(f_path, sn_list)
            if rec_matches:
                matches.extend(rec_matches)
    return matches

def get_data_from_filename(file_name):
    #improve error returns...!!!
    data = {}
    split_name = file_name.split("-", maxsplit=2)
    if len(split_name) != 3:
        data["SN"] = "Error"
        data["PB"] = "Error"
        data["REV"] = "Error"
        data["ERR"] = f"Error 'improper split' -> cannot extract SN + PB from file: {file_name}"
        return data
    else:
        SN = split_name[0]
        PB = split_name[1]
        if len(SN) != 10 or len(PB) != 11:
            data["SN"] = "Error"
            data["PB"] = "Error"
            data["REV"] = "Error"
            data["ERR"] = f"Error -> unkown SN and PB formats from file: {file_name}"
            return data
        else:
            data["SN"] = split_name[0]
            data["PB"] = f"{split_name[1][0:9]}"
            data["REV"] = f"{split_name[1][9:]}"
    #returns folowing dictionary {'SN': '1513054730', 'PB': 'PB5002100', 'REV': '1J'} + error warning if it occures
    return data

def get_sn_tracibility(file_paths):
    #accepts absolute filepaths
    data = []
    for file in file_paths:
        refdes = {}
        file_data = get_data_from_filename(os.path.basename(file))
        file_data["DATA"] = {}
        sn_data = file_data["DATA"]

        file_thee = ET.parse(file)
        tree_root = file_thee.getroot()
        panel_branch = tree_root.find("panel")
        time_stamp = convert_time_stamp(tree_root.attrib["dateComplete"])
        #maybe loop over the tree instead of find()? what if multiple panels? - unlikely
        for id in panel_branch:
            ref_set = set()
            for ref in id:
                ref_set.add(ref.text)
            refdes[id.attrib["id"]] = ref_set
        #after this loop, IDs and references are stored in refdes dictionary for every single file -> ready to be paired with charges.
        for id in refdes:
            references = refdes[id]
            #create red_key func for sorting
            for branch in tree_root:
                if branch.tag == "panel":
                    continue
                if branch.attrib["id"] == id:
                    pn = branch.attrib["barc1"]
                    hu = branch.attrib["barc6"]
                    lc = branch.attrib["barc2"]
                    if hu in sn_data:
                        sn_data[hu]["REF"].update(references)
                    else:
                        sn_data[hu] = {"REF": references, "PN": pn, "LC": lc, "TS": time_stamp }
        data.append(file_data)
    #returns a list of nested dictionaties
    #[{'SN': 'sn', 'PB': 'pb', 'REV': 'rev', 'DATA': {
    # '001013791456': {'REF': {'R26'}, 'PN': '10009080', 'LC': 'R2247Q2320', 'TS': '25/04/2024 04:09:11'},
    # '001014030211': {'REF': {'R21'}, 'PN': 'P2018321', 'LC': '03901026', 'TS': '25/04/2024 04:09:11'}}]
    return data
            

def data_cruncher(data_list):
    pass


def data_to_text(file_name_data, tracibility_data, tracibility_keys):
    #add safeguards
    converted_data = ""
    for key in tracibility_keys:
        ref = key.strip("{}")
        data = tracibility_data[key]
        converted_data = converted_data + f"{file_name_data["SN"]}/{file_name_data["PB"]}/{file_name_data["REV"]} - RefDes:{ref} / PN-{data["PN"]} / HU-{data["HU"]} / Lot-Code-{data["LC"]} / Mounted-{data["TS"]}\n"
    return converted_data

def main():

    M_path = list(os.path.split(os.path.abspath(__file__)))
    #abspath __file__ takes location of main.ps
    #split separates paths like so ['/home/art/projects/XML_reader', 'main.py'] i=0 -> cwd
    cwd = M_path[0]
    sample_dir_name = "xml_samples"
    sample_dir = os.path.join(cwd, sample_dir_name)
    sample_files = os.listdir(sample_dir)

    report_name = "new_report.txt"
    rep_path = os.path.join(cwd, report_name)

    time_filter(1, 3, 2)
    get_timestamp_from_filename("hi")

    test_file_name = sample_files[0]
    

    xml_filepath = os.path.join(sample_dir, test_file_name)
    get_data_from_filename(test_file_name)
    
    test_list = ["C8", "C4", "Q1"]

    file_data = get_data_from_filename(test_file_name)

    paths = sn_finder(sample_dir, ["1513028976", "1513054730", "1513562221"])
    get_sn_tracibility(paths)

    #with open(rep_path, "w") as file:
    #    file.write(text)


main()


