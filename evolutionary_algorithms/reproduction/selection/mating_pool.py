from evolutionary_algorithms.servicecommon.parsers.function_parser \
    import FunctionParser


class MatingPool():
    """
	This class is the entrypoint to generate a mating pool.
	This class provides a default mating function, which can
	be overridden during the initialization.
	"""

    def __init__(self, mating_pool_generator=None,
                 mating_pool_generator_args=None):
        """
		The constructor initializes the mating pool generator function,
		if any.

		:param mating_pool_generator: The function to generate mating
		pool. The first two argument passed will be the
        population and fitness, so don't pass it in explicitly. So, program accordingly.
		:param mating_pool_generator_args: The argumets to this function passed
		as a list
		:returns nothing.
		"""
        self._mating_pool_generator = mating_pool_generator
        self._mating_pool_generator_args = mating_pool_generator_args

    def generate_mating_pool(self, population, fitness):
        """
		This function generates the mating pool from the population
		based on their fitness values.
		"""
        if self._mating_pool_generator is None:
            raise NoGenerationFunction
        else:
            args = [population, fitness]
            if isinstance(self._mating_pool_generator_args, list):
                for arg in self._mating_pool_generator_args:
                    args.append(arg)
            else:
                args.append(self._mating_pool_generator_args)

                function_parser = FunctionParser(self._mating_pool_generator,
                                                 args)
                mating_pool = function_parser.call_function()
                return mating_pool
