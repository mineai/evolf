import random

class Gene():
	"""
	This Class provides the
	basic random gene for a
	candidate of the population
	of the DNA. The gene is the
    smallest element that forms the DNA
	"""

	def generate_gene(self, **kwargs):
		"""
		This Function can be overriden based
        on the requirements of the gene
        :params none
        returns: A randomly generated gene
		"""
		pass
