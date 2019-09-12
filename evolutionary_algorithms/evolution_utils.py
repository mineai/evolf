import math
import numpy as np

class EvolutionUtils():
	"""
	This class provides as an interface for
	othe evolution utilities that can be derived
	from this base class.
	"""

	def get_dna_string_from_list(self, dna):
		"""
		This string converts a list dna to
		a string.
		:param dna: A list which represents the dna
		:returns dna_string: String representation of
		the dna
		"""
		dna_string = ''.join(dna)
		return dna_string


	def softmax(self, x):
		"""
		Converts a list of elements into probability values
		using softmax

		:param x: List containing values
		:returns softmax_x: Softmax(x)
		"""
		e_x = np.exp(x - np.max(x))
		softmax_x = e_x / e_x.sum()
		return softmax_x

	def copy_elements(self, elements, copies):
		"""
		This function makes multiple copies of
		elements in a list.
		:param elements: List containing the information to be copied
		:copies: List specifying number of copies of each element in elements
		list
		:returns final_list: List containing each element copied number of times
		specified by the copies list.
		"""
		final_list = []
		for idx, element in enumerate(elements):
		    [final_list.append(element) for times in range(math.floor(copies[idx]))]

		return final_list
