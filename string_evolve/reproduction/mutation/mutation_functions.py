class MutationFunctions():
	"""
	This class contains a library of functions for crossover.

	Newer functions can be added here.
	"""

	@staticmethod
	def mutate_list_with_ascii(candidate, mutation_rate, lower_ascii=0, upper_ascii=127):
		"""
		This function tweaks in the gene of the given DNA with some
		probability.

		:param candidate: String or List containing the candidate.
		:param mutation_rate: The probability with which to mutate neucleotide's of
		the candidate

		:returns candidate: The mutated candidate
		"""
		import random
		if isinstance(candidate, str):
			candidate = list(candidate)

		for neucleotide_idx, neucleotide in enumerate(candidate):
			if random.random() < mutation_rate:
				random_ascii = random.randint(lower_ascii,
								upper_ascii)
				random_char = chr(random_ascii)
				candidate[neucleotide_idx] = random_char

		return candidate
