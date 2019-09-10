import random
import numpy as np
import math
from evolutionary_algorithms.evolution_function_lib import EvolutionFunctionLib

class EvolutionFunctionLibList(EvolutionFunctionLib):



	def default_crossover_function(self, target, parents):

		max_length = len(parents[0])
		num_parents = len(parents)

		fitness_array = [self.default_fitness_function(parent, target)
						for parent in parents]

		child = []
		idx = 0

		fitness_array = self.softmax(fitness_array)

		for parent_num, parent in enumerate(parents):
			parent_length = len(parent)
			parent_fitness = fitness_array[parent_num]

			end_idx = idx + math.ceil( parent_length * parent_fitness )

			genes_from_parent = list(parent[idx:end_idx])
			[child.append(gene) for gene in genes_from_parent]
			idx = end_idx

		return child


		if len(child) > max_length:
			child = child[:max_length]

		assert len(child) == max_length, "DNA Size Mismatch " + str(len(child))
		return child

	def default_mutation_function(self, dna, mutation_rate, gene_generator):
		for gene_idx, gene in enumerate(dna):
			if random.random() < mutation_rate:
				dna[gene_idx] = gene_generator.generate_gene()

		return dna

	def default_fitness_function(self, dna, target):
		fitness = 0
		# assert len(dna) == len(target), "DNA Size mismatch"
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

	def softmax(self, x):
		e_x = np.exp(x - np.max(x))
		return e_x / e_x.sum()

	def fitness_function_words(self, dna, target):
		dna = "".join(dna)
		target = "".join(dna)

		dna = dna.split(" ")
		target = target.split(" ")

		fitness = 0
		for gene_dna, gene_target in zip(dna, target):
			if gene_dna == gene_target:
				fitness += 1

		return fitness

	def default_generate_gene(self):
		"""
		This function generates
		a random character between
		the ASCII values 63 and 122.

		:params none
		:returns random_gene: A random character
		generated between ASCII 63 and 122
		"""
		# Specify the ASCII limits
		lower_ascii = 63
		upper_ascii = 122
		# Generate the Random Ascii Value
		random_ascii = random.randint(lower_ascii,
						 upper_ascii)

		# If Ascii is 63
		if random_ascii == 63:
			# Convert it into a Space
			random_ascii = 32
		# If Ascii is 64
		elif random_ascii == 64:
			# Convert it into a ".""
			random_ascii = 46

		# Convert Ascii to character
		random_gene = chr(random_ascii)

		# Return the character
		return random_gene
