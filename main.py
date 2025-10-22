import os
import sys

from mode import Mode, get_script_mode, read_data, read_cfg
from functions import search, write

# "panel" = hides references + their mounted IDs
# "charge" = actuall component data pairable to IDs

#"2025091504150200" - time format
#"2025 - year[0-3], 09 -month[4-5], 15 - day[6-7], 04 - hours[8-9], 15 - min[10-11] 02 - seconds[12-13] 00-??"

'''
Flags:
search:
-s = serial number search
-h = handling unit search (partial sn search)
-c = full tracibility of located handling units (takes twice as long)

Output formats:
t = text
x = excel table
Input format
r = raw string
p = filepath
'''

            
def main():
    command = sys.argv
    output_path = ""
    search_path = ""

    '''
    command[0] = main.py
    command[1] = flags
    command[2] = input - serial number / handling unit / filepath to read multiple serial numbers from.
    '''
    if len(command) != 3:
        return print('''
    Invalid function call. Please use following fortmat:
    [interpeter] [file_name] [flags] [input]
    python3 main.py -xyz /path/to/file.txt
    '''
    )
    flags = command[1]
    dest_path = ""
    input_string = command[2]
    script_mode = get_script_mode(flags)

    if not isinstance(script_mode, Mode):
        return print(f'''
Invalid function call -> please select compatible flags in format \"-xyz\":
Error explanation:
{script_mode}
'''
        )
    r_data = read_data(input_string, script_mode)
    data = search(r_data, "", script_mode)


    #with open(rep_path, "w") as file:
    #    file.write(text)

if __name__ == "__main__":
    main()


