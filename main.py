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

def ref_des_finder(ref_list, xml_path):
    #returns reference matches from a single xml file in dictionary format -> "ID": set{ref1, ref2}
    xml_tree = ET.parse(xml_path)
    xml_root = xml_tree.getroot()
    matches = {}
    for child in xml_root:
        if child.tag == "panel":
            for id in child:
                for refdes in id:
                    for ref in ref_list:
                        if refdes.text == ref:
                            if id.attrib["id"] not in matches:
                                matches[id.attrib["id"]] = {refdes.text}
                            else:
                                matches[id.attrib["id"]].add(refdes.text)
                    
    return matches

def get_component_data_from_id(id_dict, xml_path):
    xml_tree = ET.parse(xml_path)
    xml_root = xml_tree.getroot()
    # use xml_root.attrib to capture time stamps + serial number
    component_data = {}
    ref_keys = set()
    for branch in xml_root:
        if branch.tag == "charge":
            for id in id_dict:
                if id == branch.attrib["id"]:
                    temp_time = xml_root.attrib["dateComplete"]
                    #maybe create separate function for date conversion?
                    if len(temp_time) != 16:
                        formated_time = "UnknownTimeFormat"
                    else:
                        formated_time = f"{temp_time[6:8]}/{temp_time[4:6]}/{temp_time[0:4]} {temp_time[8:10]}:{temp_time[10:12]}:{temp_time[12:14]}"
                    refset_key = f"{id_dict[id]}"
                    component_data[refset_key] = {"PN": branch.attrib["barc1"], "HU": branch.attrib["barc6"], "LC": branch.attrib["barc2"], "TS": formated_time}
                    ref_keys.add(refset_key)

    #returns nested dictionary and set of keys
    #example of an output -> {"{'Q1'}": {'PN': '20005985', 'HU': '001014656171', 'LC': '012218', 'TS': '25/04/2024 04:09:11'}}, {"{'Q1'}"}
    #tuple 1 -> nested dictionary, 2 -> set of strings (keys for nested dictionary)
    return component_data, ref_keys

def format_check(file_name, file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path) or not file_name.endswith(".XML"):
        return False
    else:
        return True

    
def get_data_from_filename(file_name):
    data = {}
    split_name = file_name.split("-", maxsplit=2)
    if len(split_name) != 3:
        return f"Error 'improper split' -> cannot extract SN + PB from file: {file_name}"
    else:
        SN = split_name[0]
        PB = split_name[1]
        if len(SN) != 10 or len(PB) != 11:
            return f"Error -> unkown SN and PB formats from file: {file_name}"
        else:
            data["SN"] = split_name[0]
            data["PB"] = f"{split_name[1][0:9]}"
            data["REV"] = f"{split_name[1][9:]}"
    #returns folowing dictionary {'SN': '1513054730', 'PB': 'PB5002100', 'REV': '1J'}
    return data

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




    test_file_name = sample_files[0]
    print(test_file_name)

    xml_filepath = os.path.join(sample_dir, test_file_name)
    get_data_from_filename(test_file_name)
    
    test_list = ["C8", "C4", "Q1"]

    res_found = ref_des_finder(test_list, xml_filepath)
    tracibility_data = get_component_data_from_id(res_found, xml_filepath)
    file_data = get_data_from_filename(test_file_name)
    data = tracibility_data[0]
    keys = tracibility_data[1]

    text = data_to_text(file_data, data, keys)

    with open(rep_path, "w") as file:
        file.write(text)


main()


