import unittest
import os
from binp import *

TEST_DIR = os.path.join(os.curdir, "tests")
DATA_DIR = os.path.join(TEST_DIR, "data")

class ORLibraryInstanceReaderTest(unittest.TestCase):

    def test_get_instance_definition_with_non_numeric_data_should_raise_valueerror(self):
        with self.assertRaises(ValueError):
            ORLibraryInstanceReader._get_instance_definition("10 AA 20")

    def test_get_instance_definition_with_invalid_data_should_raise_valueerror(self):
        with self.assertRaises(ValueError):
            ORLibraryInstanceReader._get_instance_definition("invalid line")

    def test_get_instance_definition_with_ivalid_data_should_return_1_10_20(self):
        cap, num, best = ORLibraryInstanceReader._get_instance_definition("1 10 20")
        self.assertEqual(1, cap)
        self.assertEqual(10, num)
        self.assertEqual(20, best)

    def test_get_number_of_instances_with_valid_data_should_return_4(self):
        data = ["20", "1 2 3", "22"]
        ret = ORLibraryInstanceReader._get_number_of_instances(data)
        self.assertEqual(20, ret)
        
    def test_get_number_of_instances_with_invalid_data_should_raise_valueerror(self):
        data = ["A", "1 2 3", "22"]
        with self.assertRaises(ValueError):
            ORLibraryInstanceReader._get_number_of_instances(data)

    def test_get_instances_with_inst1_should_return_1_instance(self):
        ret = ORLibraryInstanceReader.get_instances(os.path.join(DATA_DIR, "inst1.txt"))
        self.assertIsInstance(ret, Instance)
        self.assertEqual("inst_01", ret.instance_name)
        self.assertEqual(90, ret.bin_capacity)
        self.assertEqual(3, ret.n_itens)
        self.assertEqual(2, ret.best_known_sol)
        self.assertEqual([42, 69, 30], ret.objects)
