
class ORLibraryInstanceReader(object):

    @classmethod
    def _get_instance_definition(cls, line):
        """It returns the bin capacity, number of itens in instance and the number of bins used 
        in the best known solution"""
        bin_capacity, number_of_itens, bins_in_best_sol = line.split()
        return int(bin_capacity), int(number_of_itens), int(bins_in_best_sol)

    @classmethod
    def _get_number_of_instances(cls, data):
        return int(data[0])
    
    @classmethod
    def _load_instance(cls, file):
        pass
    
    @classmethod
    def get_instances(cls, file):
        file_data = cls._read_file(file)
        number_of_instances = cls._get_number_of_instances(file_data)
        instance_name = file_data[1].strip()
        bin_cap, n_itens, best_sol = cls._get_instance_definition(file_data[2])
        
        objects = []
        for line in file_data[3:]:
            objects.append(int(line))
            
        return Instance(instance_name, bin_cap, n_itens, objects, best_sol)
    
    @classmethod
    def _read_file(cls, file):
        """Reads a file, returning a list with its contents"""
        input_file = open(file, 'r')
        data = list(input_file)
        input_file.close()
        return data

    
class Instance(object):
    def __init__(self, instance_name, bin_cap, n_itens, objects, best_sol):
        self.instance_name = instance_name
        self.bin_capacity = bin_cap
        self.n_itens = n_itens
        self.objects = objects
        self.best_known_sol = best_sol
