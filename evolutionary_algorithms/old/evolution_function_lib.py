import math
import random
import numpy as np

from evolutionary_algorithms.evolution_utils import EvolutionUtils
class EvolutionFunctionLib():

	"""
	This class provides as a base class that
	can be inherited and build upon the library of additional
	functions required for evolution. This includes different
	techniques for fitness, crossover and mutation.

	Fitness functions, Crossover functions, Gene Generation
	and Mutation functions can all be overriden or externally
	supplied.

	"""
	def __init(self):
		pass

	def generate_mating_pool(self, population, fitness_prob,
				mating_pool_mutiplier):
		"""
		This function generates the mating pool from the population
		based on their fitness.
		:param population: A list caontaining all the candidates of the
		population
		:param fitness_prob: A list containing the fitness of the candidates
		of the populaiton
		:param mating_pool_mutiplier: This scales the mating pool size
		:returns mating_pool: List contiaing all the candidates chosen for
		mating.
		"""
		# Scale the fitness probabilites
		fitness_prob = [fitness_of_candidate*mating_pool_mutiplier \
				for fitness_of_candidate in fitness_prob]
		# Generate mating pool by copying elements
		mating_pool = self.utils.copy_elements(population, fitness_prob)
		# if mating pool is empty, which might be
		# in the earlier generations
		if not len(mating_pool):
			  # Assign the mating pool to the original population
		      mating_pool = population
		# Return the Mating Pool
		return mating_pool

	def default_crossover_function(self, target, parents):
		"""
		This function implements a default crossover algorithm for
		lists. This function takes the target as an argument to evaluate
		the fitness. Then uses the parents to equally sample from them
		starting at indices that end last.

		For Eg:
		The child of UNICORN, POPCORN and SANDRAN would be: UNPCRAN

		:param target: String containing the target to be achieved
		:param parents: A list containing the Parent DNA's

		:returns child: The DNA created after crossover
		"""
		max_length = len(parents[0])
		num_parents = len(parents)

		fitness_array = [self.default_fitness_function(parent, target)
						for parent in parents]

		child = []
		idx = 0

		evolution_utils = EvolutionUtils()
		fitness_array = evolution_utils.softmax(fitness_array)

		for parent_num, parent in enumerate(parents):
			parent_length = len(parent)
			parent_fitness = fitness_array[parent_num]

			end_idx = idx + math.ceil( parent_length * parent_fitness )

			genes_from_parent = list(parent[idx:end_idx])
			[child.append(gene) for gene in genes_from_parent]
			idx = end_idx

		if len(child) > max_length:
			child = child[:max_length]

		assert len(child) == max_length, "DNA Size Mismatch " + str(len(child))
		return child

	def default_mutation_function(self, dna, mutation_rate, gene_generator):
		"""
		This function tweaks in the gene of the given DNA with some
		probability.

		:param dna: String or List containing the DNA.
		:param mutation_rate: The probability with which to mutate gene's of
		the DNA
		:param gene_generator: Object of the class Gene so that it can
		generate a new gene.

		:returns dna: The mutated DNA
		"""
		if isinstance(dna, str):
			dna = list(dna)

		for gene_idx, gene in enumerate(dna):
			if random.random() < mutation_rate:
				dna[gene_idx] = gene_generator.generate_gene()

		return dna
