import sympy as sp
import numpy as np
import tensorflow as tf
import random


class FunctionLibrary:
    """
    
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees. 

    *For the time being, I am unable to properly import numpy so I put
    string representations of the Unary operators as a temporary fix
    to test the rest of the function library.

    """

    def __init__(self):
        self.tenorflow_functions = {
            "U": {
                "cos": tf.cos,
                "sin": tf.sin,
                "log": tf.log,
                "exp": tf.exp,
                "tan": tf.tan,
                "square": tf.square,
                "sqrt": tf.sqrt
            },
            "B": {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y,
                # ".": tf.
            },
            "L": {
                "y": "y_pred",
                "t": "y_true",
                "1": 1,
                "-1": -1
            },
            "R": {
                "reduce_mean": tf.reduce_mean,
                "reduce_sum": tf.reduce_sum,
                "reduce_max": tf.reduce_max,
                "reduce_min": tf.reduce_min
            }
        }

        self.expression_functions = {
            "U": {
                "cos": sp.cos,
                "sin": sp.sin,
                "log": sp.log,
                "exp": sp.exp,
                "tan": sp.tan,
                "square": np.square,
                "sqrt": lambda x: np.power(x, 0.5)
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
                "reduce_mean": np.mean,
                "reduce_sum": np.sum,
                "reduce_max": np.max,
                "reduce_min": np.min
            }

        }

    def sample(self, operator_type):
        assert operator_type.upper() in self.tenorflow_functions.keys(), "Function not available"
        functions_available = list(self.tenorflow_functions.get(operator_type).keys())
        sampled_function = functions_available[random.randint(0, len(functions_available) - 1)]

        return {
            operator_type.upper(): sampled_function
        }

    def get_tensorflow_handle(self, operator):
        function = None
        for function_type in self.tenorflow_functions.keys():
            if operator in self.tenorflow_functions[function_type].keys():
                function = self.tenorflow_functions[function_type][operator]
                break
        return function

    def get_symbolic_handle(self, operator):
        function = None
        for function_type in self.expression_functions.keys():
            if operator in self.expression_functions[function_type].keys():
                function = self.expression_functions[function_type][operator]
                break
        return function

    def get_function_type(self, function_str):
        for function_type in self.tenorflow_functions.keys():
            functions = self.tenorflow_functions[function_type]
            if function_str in functions:
                return function_type

    def get_token_types(self):
        return list(self.tenorflow_functions.keys())
