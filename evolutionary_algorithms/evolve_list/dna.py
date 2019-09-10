# Import Other Classes
from gene import Gene
from external_function_intitializer import ExternalFunctionInitializer

class DNA():
	"""
	This class provides an interface
	to generate the Dna (A list) using
	the elemnts from the Gene class (A character).
	This function also provides methods to
	fetch, evaluate, reproduce and mutate the Dna.
	"""

	DEFAULT = "default"

	def __init__(self, length_of_dna, mutation_rate, **kwargs):

		self.gene_generator = Gene()
		self.initializer = ExternalFunctionInitializer()

		self.length_of_dna = length_of_dna
		self.mutation_rate = mutation_rate
		self.fitness_function = self.initializer.initialize_fitness_function(kwargs)
		self.crosover_function = self.initializer.initialize_crossover_function(kwargs)
		self.mutation_function = self.initializer.initialize_mutation_function(kwargs)



	def generate_dna(self, length_of_dna, gene_generator):
		dna = []
		for index in range(length_of_dna):
			dna.append(gene_generator.generate_gene())
		return dna


	def get_fitness(self, dna, target):
		if isinstance(target, str):
			target = list(target)
		return self.fitness_function(dna, target)




# target = "I want to drink black coffee tonight."
# mutation_rate = 0.1
#
# k = {"fitness_function": cosine_fitness_function}
# Dna = DNA(len(target), mutation_rate, **k)
# dna = Dna.intitialize_dna(Dna.length_of_dna, Dna.gene_generator)
# print("\n")
# print("Target: ", target)
# print("Dna: ", Dna.get_dna_string(dna))
# print("Dna Fitness: ", Dna.get_fitness(dna, target))
#
# print("\n\n### Default Function ")
# Dna = DNA(len(target), mutation_rate)
# dna = Dna.intitialize_dna(Dna.length_of_dna, Dna.gene_generator)
# print("\n")
# print("Target: ", target)
# print("Dna: ", Dna.get_dna_string(dna))
# print("Dna Fitness: ", Dna.get_fitness(dna, target))
#
#
#
# print("\n\n\n\n")
# Dna.default_crossover_function("Unicorn", "Popcorn", ["Unijorn", "Uniform"])
#
#
# print("\n\n\n\n")
# print(Dna.default_mutation_function(list("Uniform"), Dna.mutation_rate, Dna.gene_generator))
