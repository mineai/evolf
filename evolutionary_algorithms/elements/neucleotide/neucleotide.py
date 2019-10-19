from evolutionary_algorithms.servicecommon.parsers.function_parser \
        import FunctionParser

class Neucleotide():
	"""
	This Class provides the basic random neuclotide for a
	candidate of the population
	of the DNA. The neuclotide is the
	smallest element that forms the DNA
	"""
	def __init__(self, generation_function, generation_function_args=None):
		"""
		The Constructor of this class instantiates a class variable
		to store the neucleotide information.

		:param generation_function: The function that will be used
		to generate the neuclotide. This function should return the generated
		neucleotide.
		:param generation_function_args: Arguments to the generator function.
		"""
		self._neucleotide_information = None
		self._genotype = None
		self._generate_function = generation_function
		self._generation_function_args = generation_function_args

	def generate_neuclotide(self):
		"""
		This function acts as an entry point to generating a
		neucleotide using the function passed in to the
		constructor.

		:params none
		:returns neucleotide: The generated neucleotide
		"""
		if self._generate_function is None:
			raise NoGenerationFunction
		else:
			function_parser = FunctionParser(self._generate_function,
					    self._generation_function_args)
			neucleotide = function_parser.call_function()
			self._neucleotide_information = neucleotide
			return neucleotide

	def generate_genotype(self, binary_conversion_function=None):
		"""
		This function generates the genetype of the neucleotide
		and assigns it to the private variable _genotype.
		"""
		raise NotImplementedError

	def get_neucleotide(self):
		"""
		This function returns the private neucleotide variable.
		:params none
		:returns neucleotide: Generated Neucleotide if any
		"""
		neucleotide = self._neucleotide_information
		return neucleotide

	def set_neucleotide(self):
		"""
		This function sets the private neucleotide variable.
		:params neucleotide:
		:returns nothing
		"""
		self._neucleotide_information = neucleotide
