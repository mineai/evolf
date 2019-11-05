from string_evolve.servicecommon.parsers.function_parser \
        import FunctionParser

class Crossover():
    """
    This class acts as interface to implement crossover
    methods.
    """

    def __init__(self, parents, crossover_function=None, crossover_function_args=None):
        """
        This constructor initializes the variables
        and the crossover function.

        :param parents: A List containing the parents over which
        crossover has to happen. The list can contain
        objects of Candidate class or the Candidate's
        genetic information.
        :param crossover_function: The crossover function object that
        will operate on the parents to generate a child. The function should
        return just one child. The first argument passed will be the
        parents, so dont pass it explicitly. So, program accordingly.
        :param crossover_function_args: Arguments to the function

        :returns nothing
        """
        self._parents = parents
        self._crossover_function = crossover_function
        self._crossover_function_args = crossover_function_args

        self._child = None

    def crossover(self):
        """
        This function acts as the entry point to
        generating a new child from the parents
        using the crossover function supplied.

        :params none
        :returns child: The child produced after the crossover function is
        applied.
        """
        if self._crossover_function is None:
            raise NoGenerationFunction
        else:
            args = [self._parents]
            if isinstance(self._crossover_function_args, list):
                for ext_arg in self._crossover_function_args:
                    args.append(ext_arg)
            else:
                if self._crossover_function_args is not None:
                    args.append(self._crossover_function_args)
            # Note here the arguments passed to the function will be
            # unpacked

            function_parser = FunctionParser(self._crossover_function,
                                            args)
            child = function_parser.call_function()
            self.child = child
            return child
