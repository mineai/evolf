import sympy as sp
import numpy as np
from collections import OrderedDict

from evolutionary_algorithms.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary

class FunctionLibrary:
    """
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees.
    """

    def __init__(self):
        import keras.backend as K
        import tensorflow as tf
        self.tokens = OrderedDict({
            "L": 3,
            "U": 3,
            "B": 1,
            "BBL": 1,
            "R": None
        })
        self.tensorflow_functions = OrderedDict({
            "U": {
                # "cos": K.cos,
                # "sin": K.sin,
                "log": [K.log, 10],
                "exp": [K.exp, 1],
                "tan": [tf.tan, 1],
                "square": [K.square, 2],
                "sqrt": [K.sqrt, 2],
                "cosh": [tf.math.cosh, 1],
                "sinh": [tf.math.sinh, 1]
            },
            "B": {
                "+": [lambda x, y: tf.add(x, y), 10],
                "-": [lambda x, y: tf.subtract(x, y), 10],
                "*": [lambda x, y: tf.multiply(x, y), 3],
                "/": [lambda x, y: tf.divide(x, y), 1]
            },
            "BBL": {
                "- y * log(x)":  [lambda x, y: -y * K.log(x), 1],
                "(1 - y) * log(1 - x)": [lambda x, y: (1 - y) * K.log(1 - x), 1],
                # "crossentropy": [lambda x, y: -y * K.log(x) + (1 - y) * K.log(1 - x), 1],
                # "squared_differnece": [lambda x, y: K.square(x - y), 1]
            },
            "L": {
                "y": ["y_pred", 3],
                "t": ["y_true", 3],
                "pos_scalar": [1, 1],
                "neg_scalar": [-1, 1]
            },
            "R": {
                "mean": [tf.reduce_mean, 1],
                # "sum": tf.reduce_sum,
                # "max": tf.reduce_max,
                # "min": tf.reduce_min
            }
        })

        self.expression_functions = OrderedDict({
            "U": {
                "cos": sp.cos,
                "sin": sp.sin,
                "log": sp.log,
                "exp": sp.exp,
                "tan": sp.tan,
                "square": np.square,
                "sqrt": sp.sqrt,
                "cosh": sp.cosh,
                "sinh": sp.sinh
            },
            "B": {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y
            },
            "BBL": {
                "- y * log(x)": lambda x, y: -y * sp.log(x),
                "(1 - y) * log(1 - x)": lambda x, y: (1 - y) * sp.log(1 - x),
                "crossentropy": lambda x, y: -y * sp.log(x) + (1 - y) * sp.log(1 - x),
                "squared_differnece": lambda x, y: (x - y) ** 2
            },
            "L": {
                "y": sp.Symbol("y_pred"),
                "t": sp.Symbol("y_true"),
                "pos_scalar": 1,
                "neg_scalar": -1
            },
            "R": {
                "mean": np.mean,
                "sum": np.sum,
                "max": np.max,
                "min": np.min
            }

        })

    def get_tensorflow_expression(self):
        return self.tensorflow_functions

    def get_symbolic_expression(self):
        return self.expression_functions

    def sample(self, operator_type):
        """
        Put your fucking comments here god damn it!

        :param operator_type:
        :return operator_type.upper(): sampled_function:

        """
        assert operator_type.upper() in self.get_tensorflow_expression().keys(), "Function not available"
        functions_available = list(self.get_tensorflow_expression().get(operator_type).keys())

        functions = []
        fitness = []

        for function in functions_available:
            functions.append(function)
            fitness.append(self.get_tensorflow_expression().get(operator_type)[function][1])

        mating_pool = SelectionFunctionsLibrary.default_mating_pool(functions, fitness, 100)
        sampled_function = SelectionFunctionsLibrary.natural_selection(mating_pool, 1)[0]
        return sampled_function

    def get_tensorflow_handle(self, operator):
        """
            Put your fucking comments here god damn it!

            :param operator:
            :return function:

        """
        function = None
        for function_type in self.get_tensorflow_expression().keys():
            if operator in self.get_tensorflow_expression()[function_type].keys():
                function = self.get_tensorflow_expression()[function_type][operator]
                break
        return function[0]

    def get_symbolic_handle(self, operator):
        """
            Put your fucking comments here god damn it!

            :param operator:
            :return function:

        """
        function = None
        for function_type in self.get_symbolic_expression().keys():
            if operator in self.get_symbolic_expression()[function_type].keys():
                function = self.get_symbolic_expression()[function_type][operator]
                break
        return function

    def get_function_type(self, function_str):
        """
            Put your fucking comments here god damn it!

            :param function_str:
            :return function_type:

        """
        for function_type in self.get_tensorflow_expression().keys():
            functions = self.get_tensorflow_expression()[function_type]
            if function_str in functions:
                return function_type

    def get_token_types(self):
        """
        This function returns all the availaible node types.
        That is: "U", "B" etc
        :return list: that contains the node types possible.
        """
        return list(self.get_tensorflow_expression().keys())
