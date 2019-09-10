# Import Other Classes
from evolutionary_algorithms.evolve_list.gene_list import GeneList
from evolutionary_algorithms.dna import DNA
from evolutionary_algorithms.evolve_list.evolution_functions_lib_list \
import EvolutionFunctionLibList

class DNAList(DNA):
	"""
	This class provides an interface
	to generate the Dna (A list) using
	the elemnts from the Gene class (A character).
	This function also provides methods to
	fetch, evaluate, reproduce and mutate the Dna.
	"""

	DEFAULT = "default"

	def __init__(self, length_of_dna, mutation_rate, **kwargs):

		self.length_of_dna = length_of_dna
		self.gene_generator = GeneList()
		super().__init__(length_of_dna, mutation_rate, **kwargs)

		evolution_functions = EvolutionFunctionLibList()

		self.fitness_function = self.initializer.initialize_fitness_function(kwargs,
		 										evolution_functions.default_fitness_function)
		self.crosover_function = self.initializer.initialize_crossover_function(kwargs,
												evolution_functions.default_crossover_function)
		self.mutation_function = self.initializer.initialize_mutation_function(kwargs,
												evolution_functions.default_mutation_function)


	def generate_dna(self, length_of_dna, gene_generator):
		dna = []
		for index in range(length_of_dna):
			gene = gene_generator.generate_gene()
			# print(gene)
			dna.append(gene)
		return dna

	def get_fitness(self, dna, target):
		if isinstance(target, str):
			target = list(target)
		return self.fitness_function(dna, target)
