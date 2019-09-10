import math
import numpy as np

class EvolutionUtils():
	def get_dna_string_from_list(self, dna):
		return ''.join(dna)

	def softmax(self, x):
		e_x = np.exp(x - np.max(x))
		return e_x / e_x.sum()

	def copy_elements(self, elements, copies):
		final_list = []
		for idx, element in enumerate(elements):
		    [final_list.append(element) for times in range(math.floor(copies[idx]))]

		return final_list


	 # def copy_elements(self, elements, copies):
		# final_list = []
		# for idx, element in enemurate(elements):
		#     [final_list.append(element) for times in range(copies[idx])]
     #
		# return final_list
