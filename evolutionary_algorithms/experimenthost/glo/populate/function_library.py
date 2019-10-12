import sympy as sp
import numpy as np
import tensorflow as tf
import random

import keras.backend as K

class FunctionLibrary:
    """
    
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees. 

    *For the time being, I am unable to properly import numpy so I put
    string representations of the Unary operators as a temporary fix
    to test the rest of the function library.

    """

    tenorflow_functions = {
        "U": {
            # "cos": K.cos,
            # "sin": K.sin,
            "log": K.log,
            "exp": K.exp,
            # "tan": tf.tan,
            "square": K.square,
            "sqrt": K.sqrt,
            # "cosh": tf.math.cosh,
            # "sinh": tf.math.sinh
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
            "1": 1,
            "-1": -1
        },
        "R": {
            "mean": tf.reduce_mean,
            "sum": tf.reduce_sum,
            "max": tf.reduce_max,
            "min": tf.reduce_min
        }
    }

    expression_functions = {
        "U": {
            "cos": sp.cos,
            "sin": sp.sin,
            "log": sp.log,
            "exp": sp.exp,
            "tan": sp.tan,
            "square": np.square,
            "sqrt": lambda x: np.power(x, 0.5),
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
            "1": 1,
            "-1": -1
        },
        "R": {
            "mean": np.mean,
            "sum": np.sum,
            "max": np.max,
            "min": np.min
        }

    }

    @classmethod
    def sample(cls, operator_type):
        """
        Put your fucking comments here god damn it!

        :param operator_type:
        :return operator_type.upper(): sampled_function:

        """
        assert operator_type.upper() in cls.tenorflow_functions.keys(), "Function not available"
        functions_available = list(cls.tenorflow_functions.get(operator_type).keys())
        sampled_function = functions_available[random.randint(0, len(functions_available) - 1)]

        return {
            operator_type.upper(): sampled_function
        }

    @classmethod
    def get_tensorflow_handle(cls, operator):
        """
            Put your fucking comments here god damn it!

            :param operator:
            :return function:

        """
        function = None
        for function_type in cls.tenorflow_functions.keys():
            if operator in cls.tenorflow_functions[function_type].keys():
                function = cls.tenorflow_functions[function_type][operator]
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
        for function_type in cls.expression_functions.keys():
            if operator in cls.expression_functions[function_type].keys():
                function = cls.expression_functions[function_type][operator]
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
        for function_type in cls.tenorflow_functions.keys():
            functions = cls.tenorflow_functions[function_type]
            if function_str in functions:
                return function_type

    @classmethod
    def get_token_types(cls):
        return list(cls.tenorflow_functions.keys())
