class FitnessLibrary():
	"""
	This class implements all the fitness objectives availaible.
	More functions can be added to this class to build up a library of
	the fitness functions.

	The requirement to add more fitness functions is:
		* That a fitness value should be returned.
		* The function should be able to handle only a candidate
		(And not a populaton)
	"""


	@staticmethod
	def character_matching_fitness_function(dna, target):
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

	@staticmethod
	def cosine_fitness_function(dna, target):
		"""
   		This function comuptes the cosine distance between
    	dna and target.

    	:param dna: String or List. The DNA who's
		fitness is required.
		:param target: String/List containing the target DNA.

		:returns fitness: Fitness of the DNA (Not Squished into probability)
   		"""
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

	@staticmethod
	def fitness_function_words(dna, target):
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

	@staticmethod
	def get_best_fitness_candidate(population, fitness_prob):
		"""
		This function returns the best candidate of the population.
		:param population: A list containing the population.
		:param fitness_prob: A list containing the fitness of the population

		:returns best_candidate: The candidate with the highest fitness
		"""
		import numpy as np
		fitness_probs = np.array(fitness_prob)
		max_fitness_element = np.argmax(fitness_probs)

		best_candidate = {fitness_prob[max_fitness_element]: population[max_fitness_element]}
		return best_candidate
