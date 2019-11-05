import sympy as sp
import numpy as np

from string_evolve.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary


class SearchSpace:
    """
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees.
    """

    def __init__(self):
        import keras.backend as K
        import tensorflow as tf
        self.search_space = {
            "log": {
                "tensorflow_handle": K.log,
                "symbolic_handle": sp.log,
                "probability": 4,
                "type": "U"
            },
            "exp": {
                "tensorflow_handle": K.exp,
                "symbolic_handle": sp.exp,
                "probability": 1,
                "type": "U"
            },
            # "tan": {
            #     "tensorflow_handle": tf.tan,
            #     "symbolic_handle": sp.tan,
            #     "probability": 1,
            #     "type": "Y"
            # },
            "square": {
                "tensorflow_handle": K.square,
                "symbolic_handle": np.square,
                "probability": 1,
                "type": "U"
            },
            "sqrt": {
                "tensorflow_handle": K.sqrt,
                "symbolic_handle": sp.sqrt,
                "probability": 2,
                "type": "U"
            },
            "cosh": {
                "tensorflow_handle": tf.math.cosh,
                "symbolic_handle": sp.cosh,
                "probability": 1,
                "type": "U"
            },
            "sinh": {
                "tensorflow_handle": tf.math.sinh,
                "symbolic_handle": sp.sinh,
                "probability": 1,
                "type": "U"
            },
            "acosh": {
                "tensorflow_handle": tf.math.cosh,
                "symbolic_handle": sp.cosh,
                "probability": 1,
                "type": "U"
            },
            "asinh": {
                "tensorflow_handle": tf.math.sinh,
                "symbolic_handle": sp.sinh,
                "probability": 1,
                "type": "U"
            },
            "+": {
                "tensorflow_handle": lambda x, y: tf.add(x, y),
                "symbolic_handle": lambda x, y: x + y,
                "probability": 1,
                "type": "B"
            },
            "-": {
                "tensorflow_handle": lambda x, y: tf.subtract(x, y),
                "symbolic_handle": lambda x, y: x - y,
                "probability": 1,
                "type": "B"
            },
            "*": {
                "tensorflow_handle": lambda x, y: tf.multiply(x, y),
                "symbolic_handle": lambda x, y: x * y,
                "probability": 1,
                "type": "B"
            },
            "/": {
                "tensorflow_handle": lambda x, y: tf.divide(x, y),
                "symbolic_handle": lambda x, y: x / y,
                "probability": 1,
                "type": "B"
            },
            "mean": {
                "tensorflow_handle": tf.reduce_mean,
                "symbolic_handle": np.mean,
                "probability": 1,
                "type": "R"
            },
            "y": {
                "tensorflow_handle": "y_pred",
                "symbolic_handle": sp.Symbol("y_pred"),
                "probability": 3,
                "type": "L"
            },
            "t": {
                "tensorflow_handle": "y_true",
                "symbolic_handle": sp.Symbol("y_true"),
                "probability": 3,
                "type": "L"
            },
            "pos_scalar": {
                "tensorflow_handle": 1,
                "symbolic_handle": 1,
                "probability": 1,
                "type": "L"
            },
            "neg_scalar": {
                "tensorflow_handle": -1,
                "symbolic_handle": -1,
                "probability": 1,
                "type": "L"
            }
        }

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

            operator_sample_space = SelectionFunctionsLibrary.default_mating_pool(functions,
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
        sampled_function = SelectionFunctionsLibrary.natural_selection(sample_space,
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

