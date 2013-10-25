class ORLibraryInstanceReader(object):
    """Class that knows how to load the ORLibrary instances for the 1-D bin
    packing instances"""

    @classmethod
    def get_instances(cls, file):
        """Returns a list of Instance objects with the instances found in file param"""
        file_data = cls._read_file(file)
        number_of_instances = cls._get_number_of_instances(file_data)
        
        instances = []
        idx = 1
        for x in xrange(0, number_of_instances):
            instance_name = file_data[idx].strip()
            bin_cap, n_itens, best_sol = cls._get_instance_definition(file_data[idx+1])
            
            objects = []
            for line in file_data[idx+2:idx+2+n_itens]:
                objects.append(int(line))
            
            inst = Instance(instance_name, bin_cap, objects, best_sol)
            instances.append(inst)
            idx = idx+n_itens+2
        
        return instances

    @classmethod
    def _get_instance_definition(cls, line):
        """It returns the bin capacity, number of itens in instance and the number of bins used 
        in the best known solution"""
        bin_capacity, number_of_itens, bins_in_best_sol = line.split()
        return int(bin_capacity), int(number_of_itens), int(bins_in_best_sol)

    @classmethod
    def _get_number_of_instances(cls, data):
        """Returns the number of instances in the data file"""
        return int(data[0])

    @classmethod
    def _read_file(cls, file):
        """Reads a file, returning a list with its contents"""
        input_file = open(file, 'r')
        data = list(input_file)
        input_file.close()
        return data


class Instance(object):
    """Class that represents an 1-D bin packing problem instance"""
    
    def __init__(self, instance_name, bin_cap, objects, best_sol):
        self.instance_name = instance_name
        self.bin_capacity = bin_cap
        self.objects = objects
        self.best_known_sol = best_sol


class Constructor(object):
    """Base class of constructive algorithms"""
    
    def __init__(self, instance):
        self.instance = instance


class FirstFitConstructor(Constructor):
    
    def generate_solution(self):
        solution = Solution(len(instance.objects))
        for obj, weight in enumerate(instance.objects):
            box_number = self._find_box_that_fits(weight)
            solution.add_object(obj, weight, box_number)
            
        return solution


class Solution(object):
    """A solution for the bin packing problem."""
    
    def __init__(self, size=1):
        if size <= 0:
            raise ValueError("The solution size should be greater than zero.")
            
        self.sol = [0] * size
        self.boxes = {}

    def add_object(obj, weight, box):
        pass
