
class ORLibraryInstanceReader(object):

	@classmethod
	def _get_instance_definition(cls, line):
		bin_capacity, number_of_itens, bins_in_best_sol = line.split()
		return int(bin_capacity), int(number_of_itens), int(bins_in_best_sol)
