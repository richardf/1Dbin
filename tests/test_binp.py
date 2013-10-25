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

        self.assertIsInstance(ret[0], Instance)
        self.assertEqual("inst_01", ret[0].instance_name)
        self.assertEqual(90, ret[0].bin_capacity)
        self.assertEqual(2, ret[0].best_known_sol)
        self.assertEqual([42, 69, 30], ret[0].objects)

    def test_get_instances_with_inst2_should_return_2_instances(self):
        ret = ORLibraryInstanceReader.get_instances(os.path.join(DATA_DIR, "inst2.txt"))

        self.assertIsInstance(ret[0], Instance)
        self.assertEqual("inst_01", ret[0].instance_name)
        self.assertEqual(90, ret[0].bin_capacity)
        self.assertEqual(2, ret[0].best_known_sol)
        self.assertEqual([42, 69, 30], ret[0].objects)

        self.assertIsInstance(ret[1], Instance)
        self.assertEqual("inst_02", ret[1].instance_name)
        self.assertEqual(50, ret[1].bin_capacity)
        self.assertEqual(2, ret[1].best_known_sol)
        self.assertEqual([10, 20, 30, 40], ret[1].objects)


class InstanceTest(unittest.TestCase):
    def test_Instance_object_should_receive_data_in_init_method(self):
        inst = Instance("name", 100, [30, 20], 1)
        
        self.assertIsInstance(inst, Instance)
        self.assertEqual("name", inst.instance_name)
        self.assertEqual(100, inst.bin_capacity)
        self.assertEqual([30, 20], inst.objects)


class SolutionTest(unittest.TestCase):
    def test_solution_of_size_3_should_have_sol_with_zeros(self):
        solution = Solution(3)
        self.assertEqual(3, len(solution.sol))
        self.assertEqual([0, 0, 0], solution.sol)
        
    def test_solution_of_invalid_size_should_raise_error(self):
        with self.assertRaises(ValueError):
            solution = Solution(-1)
