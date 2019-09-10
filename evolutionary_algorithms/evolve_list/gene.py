import random

class Gene():
	"""
	This Class provides the
	basic random gene for a
	candidate of the population
	of the DNA. The gene is a character
	randomly generated.
	"""

	def generate_gene(self):
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
