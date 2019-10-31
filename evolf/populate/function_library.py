import sympy as sp
import numpy as np
import keras.backend as K
import tensorflow as tf
import random


class FunctionLibrary:
    """
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees.
    """

    def __init__(self):
        self.tensorflow_functions = {}
        self.expression_functions = {}

    def get_tensorflow_expression(self):

        return self.tensorflow_functions

    def get_symbolic_expression(self):

        return self.expression_functions

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
