import unittest
from functions import *
from mode import *

path_to_test = list(os.path.split(os.path.abspath(__file__)))
sample_path = os.path.join(path_to_test[0], "xml_samples")
input_path = os.path.join(path_to_test[0], "Sample_files")
report_folder = os.path.join(path_to_test[0], "reports")

sn_1 = ["1513562221"]
files_1 = sn_finder(sample_path, sn_1)
obj_dict = get_sn_tracibility(files_1)
test_obj_1 = obj_dict[sn_1[0]]


class TestMain(unittest.TestCase):
    def test_file_locator0(self):
        sn = [1513028976, 1513054730, 1513562221]
        files = sn_finder(sample_path, sn)
        self.assertEqual(len(files), 14)

    def test_file_locator1(self):
        self.assertEqual(len(files_1), 2)

    #def test_obj_to_text(self):
        #obj_text = test_obj_1.to_text()
        #expected = 'Serial number: 1513562221, Project: PB5302000 / 1B, Time stamp: 15/09/2025 04:15:02\nHU: 001014389333 - PN: N711259 / Lot Code: SL21308541 / References: U2\nHU: 001016387737 - PN: N704820 / Lot Code: 1TBKARP5K / References: C6, C21, C22, C23, C24, C25, C38, C39, C40, C41, C42, C43, C44, C45\nHU: 001016503530 - PN: 10030957 / Lot Code: ** / References: U50\nHU: 001015716466 - PN: N708009 / Lot Code: T2034B05GP / References: R40, R41\nHU: 001016064831 - PN: N708566 / Lot Code: TBPB4303440A / References: T1, T2, T3, T4\nHU: 001014965295 - PN: N706735 / Lot Code: 1T38N0420954 / References: R10, R12, R13, R14, R15, R16\nHU: 001015989079 - PN: N704575 / Lot Code: 1T100P062651 / References: C1, C2, C4, C5, C7, C14, C15, C16, C20, C26, C27, C28, C29, C30, C31, C32, C33, C34, C35, C36, C37\nHU: 001015885031 - PN: N710776 / Lot Code: 242785350000TRX / References: U3\nHU: 001014998170 - PN: N711381 / Lot Code: 1TD23384G730 / References: D1, D2, D3\nHU: 001015704724 - PN: N706906 / Lot Code: 1T38N0810433 / References: R1, R11\nHU: 001014798180 - PN: N709657 / Lot Code: ** / References: U6\nHU: 001016347954 - PN: N706601 / Lot Code: 1T38N34307710058 / References: R2, R3, R4, R5\nHU: 001015157605 - PN: N708101 / Lot Code: TBPC4511030A / References: D10, D11, D12\nExtracted from files:\n/home/art/projects/XML_reader/xml_samples/1513562221-PB53020001B-2-NO-PCB-BARCODE139-20250915041503.XML\n/home/art/projects/XML_reader/xml_samples/1513562221-PB53020001B-1-NO-PCB-BARCODE139-20250915040237.XML\n'
        #self.assertEqual(obj_text, expected)

    #def test_obj_to_xcel(self):
        #write_xcel(obj_dict, report_folder)

    #def test_obj_to_txt(self):
        #write_txt(obj_dict, report_folder)
    
    def test_hu_test(self):
        hu = ["001012162855"]
        macthes = hu_finder(sample_path, hu)
        pass

    def test_mode_01(self):
        command_str = "1234"
        result = get_script_mode(command_str)
        expected = f"Invalid mode format: {command_str}"
        self.assertEqual(result, expected)
    
    def test_mode_02(self):
        command_str = "-234"
        result = get_script_mode(command_str)
        expected = f"Invalid mode: \"2\" is not recognized by this script."
        self.assertEqual(result, expected)
    
    def test_mode_03(self):
        command_str = "-srt"
        result = get_script_mode(command_str)
        expected = Mode.SN_TEXT_TXT
        self.assertEqual(result, expected)

    def test_mode_04(self):
        command_str = "-ssr"
        result = get_script_mode(command_str)
        expected = "Invalid mode - \"s\" selected multiple times"
        self.assertEqual(result, expected)

    def test_mode_05(self):
        command_str = "-shx"
        result = get_script_mode(command_str)
        expected = "Invalid mode \"h\" is not allowed to be selected together with either \"s\" or \"c\"."
        self.assertEqual(result, expected)

    def test_mode_06(self):
        command_str = "-cpx"
        result = get_script_mode(command_str)
        expected = Mode.HUC_PATH_XLS
        self.assertEqual(result, expected)

    def test_mode_07(self):
        command_str = "Hello world"
        result = get_script_mode(command_str)
        expected = f"Invalid mode format: {command_str}"
        self.assertEqual(result, expected)

    def test_text_read(self):
        sn_txt = os.path.join(input_path, "SN text.txt")
        lst = set(read_txt(sn_txt))
        expected = {'1513266000', '1513028976', '1513054781', '1513054730', '1513562220', '1513562221', '1513265919'}
        self.assertEqual(lst, expected)

    def test_excel_read(self):
        sn_xls = os.path.join(input_path, "SN table.xlsx")
        lst = set(read_excel(sn_xls))
        expected = {'1513266000', '1513028976', '1513054781', '1513054730', '1513562220', '1513562221', '1513265919'}
        self.assertEqual(lst, expected)
        
if __name__ == "__main__":
    unittest.main()   