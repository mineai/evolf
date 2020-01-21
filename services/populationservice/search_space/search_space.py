import sympy as sp
import numpy as np

from servicecommon.utils.evolution_util import EvolutionUtils

class SearchSpace:
    """
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees.
    """

    def __init__(self):
        self.search_space = {}

    def collect_by_type(self, operator_type):
        operator_type_search_space = {}
        for function in list(self.search_space.keys()):
            function_type = self.get_function_type(function)
            if function_type == operator_type:
                operator_type_search_space.update({
                        function: self.search_space[function]
                    })

        return operator_type_search_space

    def generate_sample_space(self, operators):
        sample_space = []
        for operator in operators:
            operator_sample_space = self.collect_by_type(operator)

            probabilities = []
            functions = list(operator_sample_space.keys())
            for function in functions:
                probabilities.append(operator_sample_space[function]["probability"])

            operator_sample_space = EvolutionUtils.default_mating_pool(functions,
                                                                                  probabilities,
                                                                                  100)
            sample_space.extend(operator_sample_space)
        import random
        random.shuffle(sample_space)
        return sample_space

    def sample(self, operator_types):
        if not isinstance(operator_types, list):
            operator_types = [operator_types]
        sample_space = self.generate_sample_space(operator_types)
        sampled_function = EvolutionUtils.natural_selection(sample_space,
                                                                       1)[0]
        return sampled_function

    def get_tensorflow_handle(self, function):
        function_dict = self.search_space[function]["tensorflow_handle"]
        return function_dict

    def get_symbolic_handle(self, function):
        function_dict = self.search_space[function]["symbolic_handle"]
        return function_dict

    def get_function_type(self, function):
        return self.search_space[function]["type"]

