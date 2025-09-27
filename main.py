import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# "panel" = hides references + their mounted IDs
# "charge" = actuall component data pairable to IDs

def main():
    M_path = list(os.path.split(os.path.abspath(__file__)))
    #abspath __file__ takes location of main.ps
    #split separates paths like so ['/home/art/projects/XML_reader', 'main.py'] i=0 -> cwd
    cwd = M_path[0]
    sample_dir_name = "xml_samples"
    sample_dir = os.path.join(cwd, sample_dir_name)
    sample_files = os.listdir(sample_dir)


    tree = ET.parse(os.path.join(sample_dir, sample_files[0]))
    root = tree.getroot()
    print(root.tag)
    for child in root:
        print(child)
main()