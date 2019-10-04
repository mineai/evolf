class CrossoverFunctions():
	"""
	This class contains a library of functions for crossover.

	Newer functions can be added here.
	"""

	@staticmethod
	def crossover_function_lists(parents):
		"""
		This function implements a default crossover algorithm for
		lists. This function takes the target as an argument to evaluate
		the fitness. Then uses the parents to equally sample from them
		starting at indices that end last.

		For Eg:
		The child of UNICORN, POPCORN and SANDRAN would be: UNPCRAN

		:param parents: A list containing the Parent DNA's

		:returns child: The DNA created after crossover
		"""
		import math
		max_length = len(parents[0])
		num_parents = len(parents)

		child = []
		idx = 0

		fitness_array = [max_length / num_parents]*num_parents
		for parent_num, parent in enumerate(parents):
			parent_length = len(parent)
			parent_fitness = fitness_array[parent_num]
			end_idx = idx + math.ceil( parent_length * parent_fitness )

			genes_from_parent = list(parent[idx:end_idx])
			[child.append(gene) for gene in genes_from_parent]
			idx = end_idx

		if len(child) > max_length:
			child = child[:max_length]

		assert len(child) == max_length, "Candidate Size Mismatch " + str(len(child))
		return child
