import random
import numpy as np
import math
from evolutionary_algorithms.evolution_function_lib import EvolutionFunctionLib

class EvolutionFunctionLibList(EvolutionFunctionLib):

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
		lower_ascii = 32
		upper_ascii = 127
		# Generate the Random Ascii Value
		random_ascii = random.randint(lower_ascii,
						 upper_ascii)

		# If Ascii is 127
		if random_ascii == 127:
			# Convert it into a new line
			random_ascii = 10
		# # If Ascii is 64
		# elif random_ascii == 64:
		# 	# Convert it into a ".""
		# 	random_ascii = 46

		# Convert Ascii to character
		random_gene = chr(random_ascii)

		# Return the character
		return random_gene
