import math
import random

class EvolutionFunctionLib():

	def default_crossover_function(self, target, dna, partners):
		max_length = len(dna)

		partners.append(dna)
		parents = partners

		fitness_array = [self.get_fitness(parent, target) for parent in parents]

		parents = [x for _, x in sorted(zip(fitness_array, parents))][::-1]
		fitness_array = sorted(fitness_array)[::-1]

		child = []
		idx = 0

		fitness_array = self.softmax(fitness_array)

		for parent_num, parent in enumerate(parents):
			parent_length = len(parent)
			parent_fitness = fitness_array[parent_num]
			end_idx = idx + math.floor( parent_length * parent_fitness )

			genes_from_parent = list(parent[idx:end_idx])
			[child.append(gene) for gene in genes_from_parent]
			idx = end_idx

		return child

	def default_mutation_function(self, dna, mutation_rate, gene_generator):
		
		if isinstance(dna, str):
			dna = list(dna)
            
		for gene_idx, gene in enumerate(dna):
			if random.random() < mutation_rate:
				dna[gene_idx] = gene_generator.generate_gene()

		return dna

	def default_fitness_function(self, dna, target):
		fitness = 0
		assert len(dna) == len(target), "DNA Size mismatch"
		for gene_dna, gene_target in zip(dna, target):
			if gene_dna == gene_target:
				fitness += 1

		return fitness / len(target)

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
