import unittest
from binp import *

class ORLibraryInstanceReaderTest(unittest.TestCase):

	def test_get_instance_definition_with_non_numeric_data_should_raise_valueerror(self):
		with self.assertRaises(ValueError):
			ORLibraryInstanceReader._get_instance_definition("10 AA 20")

	def test_get_instance_definition_with_invalid_data_should_raise_valueerror(self):
		with self.assertRaises(ValueError):
			ORLibraryInstanceReader._get_instance_definition("invalid line")

	def test_get_instance_definition_with_ivalid_data_should_return_1_10_20(self):
		cap, num, best = ORLibraryInstanceReader._get_instance_definition("1 10 20")
		self.assertEquals(1, cap)
		self.assertEquals(10, num)
		self.assertEquals(20, best)