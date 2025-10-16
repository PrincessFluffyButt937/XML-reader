import os
import sys

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
    '''
    command[0] = main.py
    command[1] = flags
    command[2] = input - serial number / handling unit / filepath to read multiple serial numbers from.
    '''
    flags = command[1]
    input_string = command[2]

    print(command)

    #with open(rep_path, "w") as file:
    #    file.write(text)

if __name__ == "__main__":
    main()


