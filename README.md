# XML-reader
This script was written as a temporary replacement for more sophisticated software.<br>
It is only meant for very specific use case. It is designed to parse through already generated XML files in specific format.<br>
Expected XML sample files are available in "Expected XML format samples" directory from this repository.

## The script function
This script is meant to parse through (user defined) direcrory of XML files, searching for mathing data requested by the user.<br>
Searching phase inludes data in nested directories.<br>
The script capable of searching for **matching serial numbers and handling units**. If any matching XML file is located, the most important data is captured to be written into "human" readable format -> either excel table or text file.

## Dependecies
This script utilizes third party packages and relies to read and write .xlsx (Excel) files.<br>
Without these packages, this script cannot function.<br>

**<ins>The list of dependencies:</ins>**<br>

|**<ins>Dependencies</ins>**|**<ins>Versions</ins>**|
|------|------|
|**python**|**3.13.9** or newer<br>
|**xlsxwriter**|**3.2.9** or newer<br>
|**Pandas excel package:**|Packages bellow<br>
|**xlrd**|**2.0.2** or newer|<br>
|**openpyxl**|**3.1.5** or newer|<br>
|**pyxlsb**|**1.0.10** or newer|<br>
|**python-calamine**|**0.5.3** or newer|<br>

**Links to third party packages:**<br>
[XlsxWriter instalation guide](https://xlsxwriter.readthedocs.io/getting_started.html)<br>
[Pandas excel package intalation guide](https://pandas.pydata.org/docs/getting_started/install.html#excel-files)<br>

_Note:_<br>
_The entirity of Pandas can be installed instead of just excel package, however only excel pakcage is essential for function of this sctript._

## Execution and capabilites
### Execution
This script is written solely in Python language, and ut can only be executed by typing following command in command prompt / shell:

**<ins>For windows:</ins>**<br>
py main.py -xyz user_input

**<ins>For linux:</ins>**<br>
python3 main.py -xyz user_input

**<ins>Command explanation:</ins>**

|**<ins>Command portion</ins>**|**<ins>Brief explanation</ins>**|
|------|------|
|**py / python3**|Tells the command to run a file through python interpreter|<br>
|**main.py**|Absolute path of the main.py (script location). For example "C:\XML_reader\main.py"|<br>
|**-xyz**|Flags used to deretmine scripts mode. All flags will listed further down this file.|<br>
|**user_input**|User input (data). Either raw text "0123456789" or absolute path to a file "c:\user1\Desktop\input.txt"|<br>

### Capabilites
<ins>**Reading data**</ins>

The script is capable to read user_input either directly from **1\*** commad line or from **2\*** provided .txt (text file) or .xls and .xlsx (excel) files.<br>

**<ins>Only numerical values in folowing format can be read:</ins>**<br>
Leading 0s can be ommited -> For example if you need to search for 0045678956, input without leading 0s is acceptale = 45678956. The script is designed to handle such input.<br>
If any letter added in between the input numbers (For example 014a123456) or if the input number is too long (10 for serial numbers and 12 for handling units), the entry is ommited by the script.<br>

__1*__ "0123456789,8321456987" or "0123456789, 8321456987" -> will result is search for these numbers 0123456789 8321456987. The input **must be separated** with either a space " "  or comma "," (or both ", ").<br>

__2*__ Designated columm in excell or text file.<br>
The expected data format can be found in "Expected input files" directory inside this reposiory.<br>
*Note for excel:*<br>
*It does not matter which columm contains the data. However, it is preferable for the sheet to contain only desired input data (serial numbers of handling units).*

### Directories (search and outut)

**This script is using a config file** "config.toml" to specify the searching location and output location.<br>
This congfig file can be found in the root directory of this repository.<br>
**Search location** (directory) -> directory which contains compatible XML which need to be parsed through -> this script only reads XML files. No alterations occurs during the search.<br>
**Output location** (directory) -> directory where generated reports are being exported to (optional parameter).<br>

## Flag system
Flags define what kind of input is recieved, what kind of data it should look for and what output is desired by the user. **They all fall into 3 exclusive categories -> search, input type, output type.**<br>
Flags are written in a sequence of 4 charachters. **The flag starts with a dash symbol "-"** and 3 letters which define the mode for the script. For examle "-srx".<br>

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

## NoticeS
This scripts main function is to eliminate unnecessary human labor as software used to gather the data became incompatible with out current solution.

The script is capable of gathering the data withoSut issues from very limited sample size. It should work reliably, however real life testing is required to improve it's function.
