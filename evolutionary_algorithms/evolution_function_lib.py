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

	def default_fitness_function(self, dna, target):
		"""
		This is a simple fitness function that counts
		the characters at the correct indices.

		:param dna: String or List. The DNA who's
		fitness is required.
		:param target: String/List containing the target DNA.

		:returns fitness: Fitness of the DNA (Not Squished into probability)
		"""
		fitness = 0
		for gene_dna, gene_target in zip(dna, target):
			if gene_dna == gene_target:
				fitness += 1

		return fitness

	def cosine_fitness_function(dna, target):
		import nltk
		nltk.download('punkt')
		nltk.download('stopwords')
		# Program to measure similarity between
		# two sentences using cosine similarity.
		from nltk.corpus import stopwords
		from nltk.tokenize import word_tokenize

		if isinstance(dna, list):
			dna = ''.join(dna)
		if isinstance(target, list):
			target = ''.join(target)

		# tokenization
		X_list = word_tokenize(dna)
		Y_list = word_tokenize(target)

		# sw contains the list of stopwords
		sw = stopwords.words('english')
		l1 =[];l2 =[]

		# remove stop words from string
		X_set = {w for w in X_list if not w in sw}
		Y_set = {w for w in Y_list if not w in sw}

		# form a set containing keywords of both strings
		rvector = X_set.union(Y_set)
		for w in rvector:
		    if w in X_set: l1.append(1) # create a vector
		    else: l1.append(0)
		    if w in Y_set: l2.append(1)
		    else: l2.append(0)
		c = 0

		# cosine formula
		for i in range(len(rvector)):
			c+= l1[i]*l2[i]
		cosine = c / float((sum(l1)*sum(l2))**0.5)
		return cosine


	def fitness_function_words(self, dna, target):
		"""
		Another Fitness Function that counts correct words
		at different places, rather than characters.

		:param dna: String or List. The DNA who's
		fitness is required.
		:param target: String/List containing the target DNA.

		:returns fitness: Fitness of the DNA (Not Squished into probability)
		"""
		dna = "".join(dna)
		target = "".join(dna)

		dna = dna.split(" ")
		target = target.split(" ")

		fitness = 0
		for gene_dna, gene_target in zip(dna, target):
			if gene_dna == gene_target:
				fitness += 1

		return fitness
