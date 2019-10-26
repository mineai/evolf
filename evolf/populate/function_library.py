import sympy as sp
import numpy as np

import random


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
                "log": K.log,
                "exp": K.exp,
                "tan": tf.tan,
                "square": K.square,
                "sqrt": K.sqrt,
                "cosh": tf.math.cosh,
                "sinh": tf.math.sinh
            },
            "B": {
                "+": lambda x, y: tf.add(x, y),
                "-": lambda x, y: tf.subtract(x, y),
                "*": lambda x, y: tf.multiply(x, y),
                "/": lambda x, y: tf.divide(x, y)
                # ".": tf.
            },
            "L": {
                "y": "y_pred",
                "t": "y_true",
                "pos_scalar": 1,
                "neg_scalar": -1
            },
            "R": {
                "mean": tf.reduce_mean,
                "sum": tf.reduce_sum,
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
                "/": lambda x, y: x / y,
                # ".": tf.
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
        sampled_function = functions_available[random.randint(0, len(functions_available) - 1)]

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
        return function

    @classmethod
    def get_symbolic_handle(cls, operator):
        """
            Put your fucking comments here god damn it!

            :param operator:
            :return function:

        """
        function = None
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
        function = None
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
