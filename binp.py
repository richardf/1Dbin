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
        for x in range(0, number_of_instances):
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
        solution = Solution(self.instance.bin_capacity, len(self.instance.objects))
        for obj, weight in enumerate(self.instance.objects):
            box_number = self._find_box_that_fits(weight, solution)
            isAdded = solution.add_object(obj, weight, box_number)
            if not isAdded:
                raise ValueError("Impossible to add object to box.")
            
        return solution
    
    def _find_box_that_fits(self, weight, solution):
        """Return a box that have enough space to hold the given weight. 
        If none, it opens a new box."""
        for box_number, box in enumerate(solution.boxes):
            if solution.has_space_box(box_number, weight):
                return box_number
            
        return solution.create_box()


class Solution(object):
    """A solution for the bin packing problem."""
    
    def __init__(self, box_size, size=1):
        if size <= 0:
            raise ValueError("The solution size should be greater than zero.")
            
        self.weights = [0] * size
        self.box_size = box_size
        self.boxes = {}

    def add_object(self, obj, weight, box):
        """Adds an object obj with a weight in a given box, if possible.
        Returns true if added, false otherwise."""
        self._validate(obj, weight, box)
        
        if self.has_space_box(box, weight):
            if not box in self.boxes:
                return False
                
            self.boxes[box].append(obj)
            self.weights[obj] = weight
            return True
        return False
    
    def create_box(self):
        """Create a new box, returning its box number"""
        next_box_number = len(self.boxes)
        self.boxes[next_box_number] = []
        return next_box_number

    def has_space_box(self, box, weight):
        """True if the box can hold a given weight"""
        used_weight = 0
        
        if box in self.boxes:
            for obj in self.boxes[box]:
                used_weight = used_weight + self.weights[obj]
        
        free_weight = self.box_size - used_weight
        if free_weight >= weight:
            return True
        return False
        
    def _validate(self, obj, weight, box):
        """Validate the object, weight and box parameters"""
        if obj < 0 or weight <=0 or box < 0:
            raise ValueError("Invalid data passed as argument.")
