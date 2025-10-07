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
class Data:
    def __init__(self, sn=None, pb=None, rev=None, err=None, date=None, trace=None, file_path=None):
        self.sn = sn
        self.pb = pb
        self.rev = rev
        self.err = err
        self.date = date
        self.trace = trace
        self.file_path = file_path

    def __repr__(self):
        trace_str = "\n"
        for hu in self.trace:
            trace_str = trace_str + f"HU: {hu} / {self.trace[hu]}"
        return f"SN: {self.sn}, PB: {self.pb} {self.rev}, Date: {self.date}, / Error: {self.err}, File: {self.file_path}" + trace_str
        
    def add_trace(self, hu, trace_dict):
        if not hu or trace_dict:
            return
        if hu in self.trace:
            self.trace[hu]["REF"].update(trace_dict["REF"])
        else:
            self.trace[hu] = trace_dict

    def add_error(self, error):
        if self.err:
            self.err = self.err + " / " + error
        else:
            self.err = error  


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
    #!!! implement os.scandir instead of listdir!!!!
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
        data["ERR"] = "Error 'improper split' -> cannot extract SN + PB from filename"
        return data
    else:
        SN = split_name[0]
        PB = split_name[1]
        if len(SN) != 10 or len(PB) != 11:
            data["SN"] = "Error"
            data["PB"] = "Error"
            data["REV"] = "Error"
            data["ERR"] = "Error -> unkown SN and PB formats from file"
            return data
        else:
            data["SN"] = split_name[0]
            data["PB"] = f"{split_name[1][0:9]}"
            data["REV"] = f"{split_name[1][9:]}"
    #returns folowing dictionary {'SN': '1513054730', 'PB': 'PB5002100', 'REV': '1J'} + error warning if it occures
    return data

def get_sn_tracibility(file_paths):
    #accepts absolute filepaths
    obj_data = {} 

    for file in file_paths:
        refdes = {}
        file_name = os.path.basename(file)
        file_data = get_data_from_filename(file_name)

        file_thee = ET.parse(file)
        tree_root = file_thee.getroot()
        #maybe loop over the tree instead of find()? what if multiple panels? - unlikely
        panel_branch = tree_root.find("panel")
        time_stamp = convert_time_stamp(tree_root.attrib["dateComplete"])

        sn = file_data["SN"]
        if sn == "Error":
            if time_stamp.startswith("Err"):
                sn = file_name
            else:
                sn = time_stamp


        if sn in obj_data:
            pass
        else:
            obj_data[sn] = Data(sn=sn, pb=file_data["PB"],rev=file_data["REV"],date=time_stamp, err=file_data["ERR"], file_path=file)


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

                    obj_data[sn].add_trace(hu, {"REF": references, "PN": pn, "LC": lc})

    #returns a dictionary serial numbers paired with Data objects
    #TEST this function!!!

    return obj_data
            

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


