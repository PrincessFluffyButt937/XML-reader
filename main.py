import os
import sys

from mode import Mode, get_script_mode, read_data, read_cfg
from functions import search, write, dest_check

#"2025091504150200" - time format
#"2025 - year[0-3], 09 -month[4-5], 15 - day[6-7], 04 - hours[8-9], 15 - min[10-11] 02 - seconds[12-13] 00-??"

#absolute paths of the scripts location
path_main = list(os.path.split(os.path.abspath(__file__)))
script_folder = path_main[0]
report_folder = os.path.join(script_folder, "Generated reports")
error_folder = os.path.join(script_folder, "Error reports")

def main():
    command = sys.argv
    output_path, search_path, error_report = read_cfg(script_folder)

#destination checks
    if not dest_check(search_path) or search_path == "//":
        print(
            f'''
Invalid search path -> "{search_path}"
Make sure to select valid directory path to conduct the search.
'''
        )
        return

    if output_path == "//":
        if not dest_check(report_folder):
            os.makedirs(report_folder, exist_ok=True)
        output_path = report_folder

#function call check
    if len(command) != 3:
        print(
            '''
Invalid function call. Please use following fortmat:
[interpeter] [file_name] [flags] [input]
python3 main.py -xyz 0123456789             # raw text variant
or
python3 main.py -xyz /path/to/file.txt      # input file variat
'''
        )
        return

#flag decode segment
    flags = command[1]
    input_string = command[2]
    script_mode = get_script_mode(flags)

    if not isinstance(script_mode, Mode):
        print(f'''
Invalid function call -> please select compatible flags in format \"-xyz\":
Error explanation:
{script_mode}
'''
        )
        return
#data reading, searching and writing
    r_data = read_data(input_string, script_mode)
    data, errors = search(r_data, search_path, script_mode, error_report)
    write(output_path, data, script_mode, error_folder, errors, error_report)
    print(f'''
Report generated succesfully at {output_path}
''')


if __name__ == "__main__":
    main()


