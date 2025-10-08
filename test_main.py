import unittest
from main import *

path_to_test = list(os.path.split(os.path.abspath(__file__)))
sample_path = os.path.join(path_to_test[0], "xml_samples")

class TestMain(unittest.TestCase):
    def test_file_locator0(self):
        #sn = [1513028976, 1513054730, 1513562221]
        sn = ["1513028976", "1513054730", "1513562221"]
        files = sn_finder(sample_path, sn)
        self.assertEqual(len(files), 14)

if __name__ == "__main__":
    unittest.main()   