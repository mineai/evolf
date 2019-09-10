# Import Other Classes
from evolutionary_algorithms.gene import Gene
from evolutionary_algorithms.external_function_intitializer import ExternalFunctionInitializer

class DNA():
	"""
	This class provides an interface
	to generate the Dna (a list) using
	the elemnts from the Gene class (a character).
	This function also provides methods to
	fetch, evaluate, reproduce and mutate the Dna.
	"""

	DEFAULT = "default"

	def __init__(self, dna_dimensions, mutation_rate, **kwargs):
		"""
		This Constructor provdes an interface to iniitialize
		the derived DNA class.
		:param dna_dimensions: Dimensions of the DNA. This has
		to be initialized in the derived class.
		:param mutation_rate: This is the mutation rate.
		:param kwargs: This argument is a dictionary that can
		contain aditinal parameters if required.
		The three parameters of interest would be the fitness function,
		crossover function and mutation function which should be passed an is
		fitness_function, crosover_function, mutation_function.

		:returns nothing
		"""

		self.initializer = ExternalFunctionInitializer()

		self.mutation_rate = mutation_rate

		# !!!!!!!!!! Remember to override these
		# self.gene_generator = Gene()
		# self.fitness_function = None
		# self.crosover_function = None
		# self.mutation_function = None

	def generate_dna(self, dna_dimensions, gene_generator):
		"""
		This function uses a gene generator to generate a dna.
		This function should be overriden in the derived class.
		:param dna_dimensions: Dimensions of the DNA
		:param gene_generator: Function that generates new genes
		for the DNA.

		:returns dna: The generated DNA
		"""
		pass

	def get_fitness(self, dna, target):
		"""
		This function provides an interface to be overriden
		to evaluate the fitness of a candidate of the population.
		:param dna: Candidate of the population
		:param target: Candidate to compare to

		:returns fitness: Fitness score of the dna
		"""
		pass
