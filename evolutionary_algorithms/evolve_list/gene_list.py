import random
from evolutionary_algorithms.gene import Gene
from evolutionary_algorithms.evolve_list.evolution_functions_lib_list import EvolutionFunctionLibList

class GeneList(Gene):
	"""
	This Class provides the
	basic random gene for a
	candidate of the population
	of the DNA. The gene is a character
	randomly generated.
	"""

	def __init__(self):
		print("GeneList")

	def generate_gene(self, **kwargs):
		"""
		This function generates
		a random character between
		the ASCII values 63 and 122.

		:params none
		:returns random_gene: A random character
		generated between ASCII 63 and 122
		"""
		evolution_functions = EvolutionFunctionLibList()
		if "generate_gene_function" in list(kwargs):
			generator_func = kwargs["generate_gene_function"]
		else:
			generator_func = evolution_functions.default_generate_gene

		gene = generator_func()
		return gene
