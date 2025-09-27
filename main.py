import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

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
                    
    print(matches)
    return matches

def get_component_data_from_id(id_dict, xml_path):
    xml_tree = ET.parse(xml_path)
    xml_root = xml_tree.getroot()
    # use xml_root.attrib to capture time stamps + serial number
    print(xml_root.attrib)
    component_data = {}
    for branch in xml_root:
        if branch.tag == "charge":
            for id in id_dict:
                if id == branch.attrib["id"]:
                    temp_time = xml_root.attrib["dateComplete"]
                    if len(temp_time) != 16:
                        formated_time = "UnknownTimeFormat"
                    else:
                        formated_time = f"{temp_time[6:8]}/{temp_time[4:6]}/{temp_time[0:4]} {temp_time[8:10]}:{temp_time[10:12]}:{temp_time[12:14]}"
                    print(formated_time)
                    #set which contains references is converted into string -> set/list.. cannot be used as keys in dictionary.. maybe earlier conversion?
                    component_data[f"{id_dict[id]}"] = {"PN": branch.attrib["barc1"], "HU": branch.attrib["barc6"], "LC": branch.attrib["barc2"], "TS": formated_time}
    print(component_data)
    #returns nested dictionary
    #example with real keys -> {"{'Q1'}": {'PN': '20005985', 'HU': '001014656171', 'LC': '012218', 'TS': '25/04/2024 04:09:11'}}
    return component_data



def main():
    M_path = list(os.path.split(os.path.abspath(__file__)))
    #abspath __file__ takes location of main.ps
    #split separates paths like so ['/home/art/projects/XML_reader', 'main.py'] i=0 -> cwd
    cwd = M_path[0]
    sample_dir_name = "xml_samples"
    sample_dir = os.path.join(cwd, sample_dir_name)
    sample_files = os.listdir(sample_dir)

    print(sample_files[0])

    xml_filepath = os.path.join(sample_dir, sample_files[0])
    
    test_list = ["C8", "C4", "Q1"]

    res_found = ref_des_finder(test_list, xml_filepath)
    tracibility_data = get_component_data_from_id(res_found, xml_filepath)

main()


