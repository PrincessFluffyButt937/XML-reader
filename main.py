import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# "panel" = hides references + their mounted IDs
# "charge" = actuall component data pairable to IDs


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

    ref_des_finder(test_list, xml_filepath)
main()

