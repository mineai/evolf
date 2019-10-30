import sympy as sp
import numpy as np

import random

from evolutionary_algorithms.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary

class FunctionLibrary:
    """
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees.
    """

    @staticmethod
    def get_tensorflow_expression():
        import keras.backend as K
        import tensorflow as tf

        tensorflow_functions = {
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
                "- y * log(x)":  [lambda x, y: -y * K.log(x), 3],
                "(1 - y) * log(1 - x)": [lambda x, y: (1 - y) * K.log(1 - x), 3],
                # "crossentropy": [lambda x, y: -y * K.log(x) + (1 - y) * K.log(1 - x), 1],
                # "squared_differnece": [lambda x, y: K.square(x - y), 1]
            },
            "L": {
                "y": ["y_pred", 1],
                "t": ["y_true", 1],
                "pos_scalar": [1, 1],
                "neg_scalar": [-1, 1]
            },
            "R": {
                "mean": [tf.reduce_mean, 1],
                # "sum": tf.reduce_sum,
                # "max": tf.reduce_max,
                # "min": tf.reduce_min
            }
        }
        return tensorflow_functions

    @staticmethod
    def get_symbolic_expression():
        expression_functions = {
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
                "squared_differnece": lambda x, y: (x - y)**2
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

        }
        return expression_functions

    @classmethod
    def sample(cls, operator_type):
        """
        Put your fucking comments here god damn it!

        :param operator_type:
        :return operator_type.upper(): sampled_function:

        """
        assert operator_type.upper() in cls.get_tensorflow_expression().keys(), "Function not available"
        functions_available = list(cls.get_tensorflow_expression().get(operator_type).keys())

        functions = []
        fitness = []

        for function in functions_available:
            functions.append(function)
            fitness.append(cls.get_tensorflow_expression().get(operator_type)[function][1])

        mating_pool = SelectionFunctionsLibrary.default_mating_pool(functions, fitness, 100)
        sampled_function = SelectionFunctionsLibrary.natural_selection(mating_pool, 1)[0]
        return sampled_function

    @classmethod
    def get_tensorflow_handle(cls, operator):
        """
            Put your fucking comments here god damn it!

            :param operator:
            :return function:

        """
        function = None
        for function_type in cls.get_tensorflow_expression().keys():
            if operator in cls.get_tensorflow_expression()[function_type].keys():
                function = cls.get_tensorflow_expression()[function_type][operator]
                break
        return function[0]

    @classmethod
    def get_symbolic_handle(cls, operator):
        """
            Put your fucking comments here god damn it!

            :param operator:
            :return function:

        """
        function = None
        for function_type in cls.get_symbolic_expression().keys():
            if operator in cls.get_symbolic_expression()[function_type].keys():
                function = cls.get_symbolic_expression()[function_type][operator]
                break
        return function

    @classmethod
    def get_function_type(cls, function_str):
        """
            Put your fucking comments here god damn it!

            :param function_str:
            :return function_type:

        """
        for function_type in cls.get_tensorflow_expression().keys():
            functions = cls.get_tensorflow_expression()[function_type]
            if function_str in functions:
                return function_type

    @classmethod
    def get_token_types(cls):
        """
        This function returns all the availaible node types.
        That is: "U", "B" etc
        :return list: that contains the node types possible.
        """
        return list(cls.get_tensorflow_expression().keys())
