from string_evolve.servicecommon.parsers.function_parser \
        import FunctionParser

class FitnessObjectives():
    """
    This class serves as the entry point to
    optimimizing fitness objectives and returnning a recombination
    of those scores.

    Note: This is usually done using a Pareto front, but the
    default function here returns a weighted score.
    """

    def __init__(self, objectives, args, maximize=True):
        """
        :param objectives: List of function objects of fitness functions.
        The objectives should act on a population not just a single canidate.
        :param args: An immutable tuple containing (candidate, target)
        Each list of arguments corresponds to each fitness functions
        :returns nothing
        """
        self._objectives = objectives
        self._args = args
        self._maximize = maximize

    @staticmethod
    def get_objective_fitness(objective, args):
        """
        This function calculates the Fitness using the
        provided objective function.

        :param objective: The function Object to be used
        :param args: A list of arguments that the objective
        function provided will use.

        :returns fitness: Return value of the objective function.
        """
        function_parser = FunctionParser(objective, args)
        fitness = function_parser.call_function()

        return fitness

    @classmethod
    def execute_all_fitness(self, objectives, args):
        """
        This function calculates the fitness from all the objective
        functions and returns return values as a list. Each index of
        the list corresponds to each fitness value.

        :param objectives: A list containing the function Object to be used
        :params args: A List containing tuples containing arguments to the objective functions.
        Arguments should be grouped up in a list. Each index of the tuple
        corresponds to arguments of the fintess function at that index.

        :returns fitness_from_objectives: A list containing the return values
        of all the objectives provided.
        """
        fitness_from_objectives = []
        function_parser = None

        if callable(objectives):
            function_parser = FunctionParser(objectives, args)
            fitness = function_parser.call_function()
            fitness_from_objectives = fitness
        else:
            for objective in objectives:
                function_parser = FunctionParser(objective, args)
                fitness = function_parser.call_function()
                fitness_from_objectives.append(fitness)

        return fitness_from_objectives

    def average_fitness(self, fitness_from_objectives):
        """
        This function serves as the default to recombine the fitness from
        all the objective functions. This function
        returns the average of all the fitness functions.
        :param weights: The weights used to recombine.
        """
        import numpy as np
        from collections.abc import Iterable
        if isinstance(fitness_from_objectives[0], Iterable):
            recombined_fitness = np.mean([fitness_values], axis=0)
        else:
            recombined_fitness = fitness_from_objectives
        return recombined_fitness


    def get_recombined_fitness(self, recombination_method=None):
        """
        This function serves as the entrypoint to this file. It calculates
        all the objective functions and recombines them to return the recombined
        fitness.

        :param recombination_method: A function object that should be passed
        to use an external recombination method.
        This external function should be research such that the fitness list
        is passed to it and it can operate on it
        Eg: The function call would be made as follows:
        recombination_method([fitness])

        :returns recombined_fitness: The recombined fitness value

        Note: If recombination_method is not provided, a default weighted
        recombination strategy is used.
        """
        recombined_fitness = None
        fitness_values = self.execute_all_fitness(self._objectives,
                                                self._args)
        if recombination_method is None:
            recombined_fitness = self.average_fitness(fitness_values)
        else:
            function_parser = FunctionParser(recombination_method,
                                            [fitness_values])
            recombined_fitness = function_parser.call_function()

        return recombined_fitness
