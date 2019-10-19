from evolutionary_algorithms.servicecommon.parsers.function_parser \
        import FunctionParser


class Selection():
	"""
	This class acts as an interface for Natural Selection
	methods.
	"""
	def __init__(self, mating_pool,
		selection_function=None,
		selection_function_args=None):
		"""
		The constructor of this class initializes the mating pool
		and the selection_function.

		:params population: A list containing the candidate objects
		that will be used for mating.
		:params selection_function: The function that will be used
		to select parents. The first argument passed will be the
        mating pool, so don't pass it in explicitly. So, program accordingly.
		:params selection_function_args: The arguments to that function
		passed as a list.
		"""
		self._mating_pool = mating_pool
		self._selection_function = selection_function
		self._selection_function_args = selection_function_args

	def select_parents(self):
		"""
		This function selects the parents from the mating pool
		and returns them.
		:params None
		:returns parents: List containing the parents
		"""
		if self._selection_function is None:
			raise NoGenerationFunction
		else:
			args = [self._mating_pool]
			if isinstance(self._selection_function_args, list):
				for ext_arg in self._selection_function_args:
					args.append(ext_arg)
			else:
				args.append(self._selection_function_args)
			# Note here the arguments passed to the function will be
			# unpacked.
			function_parser = FunctionParser(self._selection_function,
						args)
			parents = function_parser.call_function()
			return parents
