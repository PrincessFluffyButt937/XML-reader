# XML-reader
This reader is only meant for very specific use case. It is designed to parse through already generated XML files.
This script searches for a specific keys within XML file -> not aplicable to just any XML file.

## The script function
This script searches for matching data based on users input.
It's capable of searching for mathing serial numbers and handling units. If any matching XML file is located, the most important data is captured to be written into "human" readable format.

## Execution and capabilites
### Execution
This scrit is written solely in Python language, and ut can only be executed by typing following command in command prompt / shell:

**For windows:**
py main.py -xyz user_input

**For linux:**
python3 main.py -xyz user_input

**Command explanation:**
py / python3    -> Tells the command to run a file through python interpreter 
main.py         -> Absolute path of the script location. For example "C:/folder1/folder2/XML_reader/main.py"
-xyz            -> Flags used to deretmine scripts mode. Flags define input, serach mode, and output. All flags will listed further down this file.
user_input      -> User input (data). Either raw text "0123456789" or absolute path to a file "c:/folder1/folder2/input.txt"

### Capabilites
**Reading data**
The script is capable to read user_input either directly from 1* commad line or from 2* provided .txt or .xlsx (excel) files.
Only numerical values in folowing format:
Leading 0s can be ommited -> For example if you need to search for 0045678956, input without leading 0s is acceptale = 45678956. The script is designed to handle such input.
If any letter added in between the input numbers (For example 014a123456) or if the input number is too long (10 for serial numbers and 12 for handling units), the entry is ommited by the script.

__1*__ "0123456789,8321456987" -> will result is search for these numbers 0123456789 8321456987 (The comma "," serves as separator -> do not use spaces!)

__2*__ Designated columm in excell or text file in format bellow:
"
0123456789
1517896472
815446687
"
*Note for excel:*
*It does not matter which columm contains the data. However, it is preferable for the sheet to contain only desired input data (serial numbers of handling units).*

**Directories**
This script is using a config file "config.toml" to specify the searching location and output location.
Search location (directory) -> directory which contains compatible XML which need to be parsed through -> this script only reads XML files. No alterations occurs during the search.
Output location (directory) -> directory where generated reports are being exported to.

## Flag system
Flags define what kind of input is recieved, what kind of data it should look for, and what output is desired by the user. They fall into 3 categories -> search, input type, output type.
Flags are written in a sequence of 4 charachters. The flag starts with a dash symbol "-" and 3 letters which define the mode for the script. For examle "-srx"

**Search:**
_Tells the sctipt what it is searching for._

**s** -> search for serial numbers.
**h** -> search for handling units. This returns partial tracibility data -> only as much as file comtaining the handling unit.
**c** -> seatch for handling units. This returns full tracibility of every serial number which contains the handling unit. (search takes roughly twice as long since 2 searches are required to gather all the data)

**user_input type:**
_Defines what kind of input data has been inputed by the used._

**r** -> raw text
**p** -> path to a file

**Output type:**
_Tell the sctipt what format should be used to write down the tracibility data._

**t** -> text file
**x** -> excel table 

**General rules for flags:**
Flags from each category are unique -> mutliple flags from the same category cannot be selected together. For example, flag "s" cannot be selected together with either "h" or "c".
Flags from each category must be spefied.
Flags can be writen in any order -> For example "-hpx" causes the same actions within a script as -"-pxh".

