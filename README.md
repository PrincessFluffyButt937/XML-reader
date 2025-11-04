# XML-reader
This script was written as a temporary replacement for more sophisticated software.<br>
It is only meant for very specific use case. It is designed to parse through already generated XML files in specific format.<br>
Expected XML sample files are available in "Expected XML format - samples" directory from this repository.

## The script function
This script is meant to parse through (user defined) direcrory of XML files, searching for mathing data requested by the user.<br>
Searching phase inludes data in nested directories.<br>
The script capable of searching for **matching serial numbers and handling units**. If any matching XML file is located, the most important data is captured to be written into "human" readable format -> either excel table or text file.

## Execution and capabilites
### Execution
This script is written solely in Python language, and ut can only be executed by typing following command in command prompt / shell:

**<ins>For windows:</ins>**<br>
py main.py -xyz user_input

**<ins>For linux:</ins>**<br>
python3 main.py -xyz user_input

**<ins>Command explanation:</ins>**

**py / python3**&ensp;-> Tells the command to run a file through python interpreter<br>
**main.py**&ensp;&ensp;&ensp;&ensp;&ensp; -> Absolute path of the main.py (script location). For example "C:/folder1/folder2/XML_reader/main.py"<br>
**-xyz**&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-> Flags used to deretmine scripts mode.All flags will listed further down this file.<br>
**user_input**&ensp;&ensp;&ensp;&ensp;-> User input (data). Either raw text "0123456789" or absolute path to a file "c:/folder1/folder2/input.txt"<br>

## Capabilites
### Reading data

The script is capable to read user_input either directly from **1\*** commad line or from **2\*** provided .txt or .xlsx (excel) files.<br>

**<ins>Only numerical values in folowing format can be read:</ins>**<br>
Leading 0s can be ommited -> For example if you need to search for 0045678956, input without leading 0s is acceptale = 45678956. The script is designed to handle such input.
If any letter added in between the input numbers (For example 014a123456) or if the input number is too long (10 for serial numbers and 12 for handling units), the entry is ommited by the script.

__1*__ "0123456789,8321456987" -> will result is search for these numbers 0123456789 8321456987 (The comma "," serves as separator -> do not use spaces!)

__2*__ Designated columm in excell or text file.<br>
The expected data format can be found in "Expected input files".<br>
*Note for excel:*<br>
*It does not matter which columm contains the data. However, it is preferable for the sheet to contain only desired input data (serial numbers of handling units).*

### Directories

This script is using a config file "config.toml" to specify the searching location and output location.
Search location (directory) -> directory which contains compatible XML which need to be parsed through -> this script only reads XML files. No alterations occurs during the search.
Output location (directory) -> directory where generated reports are being exported to.

## Flag system
Flags define what kind of input is recieved, what kind of data it should look for, and what output is desired by the user. They fall into 3 categories -> search, input type, output type.
Flags are written in a sequence of 4 charachters. The flag starts with a dash symbol "-" and 3 letters which define the mode for the script. For examle "-srx"

**<ins>Search:</ins>**<br>
_Tells the sctipt what it is searching for._

**s** -> search for serial numbers.<br>
**h** -> search for handling units. This returns partial tracibility data -> only as much as file comtaining the handling unit.<br>
**c** -> seatch for handling units. This returns full tracibility of every serial number which contains the handling unit. (search takes roughly twice as long since 2 searches are required to gather all the data)<br>

**<ins>user_input type:</ins>**<br>
_Defines what kind of input data has been inputed by the used._

**r** -> raw text<br>
**p** -> path to a file<br>

**<ins>Output type:</ins>**<br>
_Tell the sctipt what format should be used to write down the tracibility data._

**t** -> text file<br>
**x** -> excel table <br>

**<ins>General rules for flags:</ins>**<br>
Flags from each category are unique -> mutliple flags from the same category cannot be selected together. For example, flag "s" cannot be selected together with either "h" or "c".
Flags from each category must be spefied.
Flags can be writen in any order -> For example "-hpx" causes the same actions within a script as -"-pxh".

## Notice
This scripts main function is to eliminate unnecessary human labor as software used to gather the data became incompatible with out current solution.

For now, the software is capable of gathering the data without issues from very limited sample size. However, i cannot say for sure how would the script fare in cases when data from thousands of files might be stored and written.
