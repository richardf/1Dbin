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
    def test_solution_of_size_3_should_have_weights_with_zeros(self):
        solution = Solution(1, 3)
        self.assertEqual(3, len(solution.weights))
        self.assertEqual([0, 0, 0], solution.weights)
        
    def test_solution_of_invalid_size_should_raise_error(self):
        with self.assertRaises(ValueError):
            solution = Solution(1, -1)

    def test_has_space_box_with_weight_bigger_than_box_should_return_false(self):
        solution = Solution(5, 2)
        self.assertFalse(solution.has_space_box(0, 10))
    
    def test_has_space_box_with_weight_smaller_than_box_should_return_true(self):
        solution = Solution(5, 2)
        self.assertTrue(solution.has_space_box(0, 4))
        
    def test_add_solution_with_weight_bigger_than_box_size_should_return_false(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        self.assertFalse(solution.add_object(0, 10, 0))
        
    def test_add_solution_with_weight_smaller_than_box_size_should_return_true(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        self.assertTrue(solution.add_object(0, 3, 0))        
        
    def test_add_solution_with_invalid_object_should_raise_error(self):
        solution = Solution(5, 2)
        with self.assertRaises(ValueError):
            solution.add_object(-1, 3, 0)
            
    def test_add_solution_with_invalid_object_size_should_raise_error(self):
        solution = Solution(5, 2)
        with self.assertRaises(ValueError):
            solution.add_object(0, -3, 0)            
            
    def test_add_solution_with_invalid_box_should_raise_error(self):
        solution = Solution(5, 2)
        with self.assertRaises(ValueError):
            solution.add_object(0, 3, -1)                        

    def test_add_solution_in_a_full_box_should_return_false(self):
        solution = Solution(5, 2)
        solution.add_object(0, 5, 0)
        self.assertFalse(solution.add_object(0, 3, 0))

    def test_add_solution_in_a_box_that_can_hold_it_should_return_true(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        solution.add_object(0, 3, 0)
        self.assertTrue(solution.add_object(0, 2, 0))

    def test_boxes_dict_should_have_one_box_with_one_object(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        solution.add_object(0, 3, 0)
        self.assertEqual(1, len(solution.boxes))
        self.assertEqual(1, len(solution.boxes[0]))
        self.assertEqual(0, solution.boxes[0][0])
        
    def test_boxes_dict_should_have_two_boxes_with_one_object_each(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        solution.boxes[1] = []
        solution.add_object(1, 3, 0)
        solution.add_object(0, 3, 1)
        self.assertEqual(2, len(solution.boxes))
        self.assertEqual(1, len(solution.boxes[0]))
        self.assertEqual(1, solution.boxes[0][0])        
        self.assertEqual(1, len(solution.boxes[1]))
        self.assertEqual(0, solution.boxes[1][0])        
        
    def test_boxes_dict_should_have_one_box_with_two_objects(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        solution.add_object(0, 3, 0)
        solution.add_object(1, 2, 0)
        self.assertEqual(1, len(solution.boxes))
        self.assertEqual(0, solution.boxes[0][0])
        self.assertEqual(2, len(solution.boxes[0]))
        self.assertEqual(1, solution.boxes[0][1])

    def test_weights_list_should_have_one_element_with_weight_3(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        solution.add_object(0, 3, 0)
        self.assertEqual(3, solution.weights[0])
        
    def test_weights_list_should_have_two_elements_with_weights_3_and_2(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        solution.boxes[1] = []
        solution.add_object(0, 3, 0)
        solution.add_object(1, 2, 0)
        self.assertEqual(3, solution.weights[0])
        self.assertEqual(2, solution.weights[1])
        
    def test_create_box_with_an_empty_solution_should_return_box_0(self):
        solution = Solution(5, 2)
        self.assertEqual(0, solution.create_box())
        self.assertEqual(1, len(solution.boxes))

    def test_create_box_with_an_solution__with_one_box_should_return_box_1(self):
        solution = Solution(5, 2)
        solution.boxes[0] = []
        self.assertEqual(1, solution.create_box())
        self.assertEqual(2, len(solution.boxes))       


class FirstFitConstructorTest(unittest.TestCase):
    def test_find_box_that_fits_5_with_empty_solution_should_return_box_0(self):
        instance =  Instance("inst_name", 20, [5, 10, 15, 20], 3)
        solution = Solution(10, 4)
        constructor = FirstFitConstructor(instance)
        self.assertEqual(0, constructor._find_box_that_fits(5, solution))
        
    def test_find_box_that_fits_20_with_one_full_box_should_return_box_1(self):
        instance =  Instance("inst_name", 20, [5, 10, 15, 20], 3)
        solution = Solution(10, 4)
        solution.boxes[0] = [0, 1, 2]
        solution.weights = [5, 10, 15, 20]
        constructor = FirstFitConstructor(instance)
        self.assertEqual(1, constructor._find_box_that_fits(5, solution))
        
    def test_generate_solution_valid_should_return_a_solution(self):
        instance =  Instance("inst_name", 10, [6, 10, 4, 5], 3)
        constructor = FirstFitConstructor(instance)
        solution = constructor.generate_solution()
        self.assertIsInstance(solution, Solution)
        self.assertEqual(3, len(solution.boxes))
        self.assertEqual([0, 2], solution.boxes[0])
        self.assertEqual([1], solution.boxes[1])
        self.assertEqual([3], solution.boxes[2])
        
    def test_generate_solution_with_weight_bigger_than_box_capacity_should_raise_error(self):
        instance =  Instance("inst_name", 5, [6, 10, 4, 5], 3)
        constructor = FirstFitConstructor(instance)
        with self.assertRaises(ValueError):
            solution = constructor.generate_solution()
