from evolutionary_algorithms.servicecommon.parsers.function_parser \
        import FunctionParser

class Mutation():
    """
    This class acts as the entrypoint to mutation of
    a neucleotide.
    """

    def __init__(self, neucleotide, mutation_method=None, mutation_function_args=None):
        """
        This constructor initializes the variables
        and the crossover function.

        :param neucleotide: Neucleotide to be mutated.
        :mutation_function: Function that will mutate. The first argument passed will be the
        neucleotide passed in, so don't pass it in accordingly. So, program accordingly.
        :mutation_function_args: Args for the mutation function
        """
        self._neucleotide = neucleotide
        self._mutation_method = mutation_method
        self._mutation_function_args = mutation_function_args

        self._neucleotide_mutated = None

    def mutate(self):
        """
        This function acts as the entry point to
        generating a new child from the parents
        using the crossover function supplied.

        :params none
        :returns mutated_neucleotide: The neucleotide mutated
        """
        if self._mutation_method is None:
            raise NoGenerationFunction
        else:
            args = [self._neucleotide]
            if isinstance(self._mutation_function_args, list):
                for ext_arg in self._mutation_function_args:
                    args.append(ext_arg)
            else:
                args.append(self._mutation_function_args)
            # Note here the arguments passed to the function will be
            # unpacked
            function_parser = FunctionParser(self._mutation_method,
                                            args)
            mutated_neucleotide = function_parser.call_function()
            self._neucleotide_mutated = mutated_neucleotide
            return mutated_neucleotide
