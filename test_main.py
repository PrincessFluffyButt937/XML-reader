import unittest
from main import *

path_to_test = list(os.path.split(os.path.abspath(__file__)))
sample_path = os.path.join(path_to_test[0], "xml_samples")

class TestMain(unittest.TestCase):
    def test_file_locator0(self):
        sn = [1513028976, 1513054730, 1513562221]
        files = sn_finder(sample_path, sn)
        self.assertEqual(len(files), 14)

    def test_file_locator1(self):
        sn = [1513562221]
        files = sn_finder(sample_path, sn)
        self.assertEqual(len(files), 2)

    def test_data_storage(self):
        sn = [1513562221]
        files = sn_finder(sample_path, sn)
        obj_dict = get_sn_tracibility(files)
    
    def test_hu_test(self):
        hu = ["001012162855"]
        macthes = hu_finder(sample_path, hu)
        print(macthes)


if __name__ == "__main__":
    unittest.main()   