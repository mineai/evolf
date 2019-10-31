import sympy as sp
import numpy as np
from evolf.populate.function_library import FunctionLibrary
from evolutionary_algorithms.servicecommon.parsers.parse_hocon import ParseHocon


class SymbolicSearchSpace:
    full_search_space = {}

    # This gives the range of possible symbolic functions usable
    symbolic_search_space = {
            "cos": sp.cos,
            "sin": sp.sin,
            "log": sp.log,
            "exp": sp.exp,
            "tan": sp.tan,
            "square": np.square,
            "sqrt": lambda x: np.power(x, 0.5),
            "cosh": sp.cosh,
            "sinh": sp.sinh,
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "y": sp.Symbol("y_pred"),
            "t": sp.Symbol("y_true"),
            "pos_scalar": 1,
            "neg_scalar": -1,
            "mean": np.mean,
            "sum": np.sum,
            "max": np.max,
            "min": np.min
    }
    @classmethod
    def get_search_space(cls, hocon_config):
        ''' Get Search Space:
            This works on parsing the search space information from the hocon
            configuration file. This works based on user input into the hocon
        '''
        conf = ParseHocon().parse(hocon_config)
        domain_config = conf.get("domain_config")
        search_space = domain_config.get("search_space")
        cls.full_search_space = search_space

    @classmethod
    def populate_function_library(cls, function_library):
        ''' Populate Function Library:
            This allows one to set the usable functions in a single function
            library for a set population. This is set based on user input
            from the hocon. For now the hocon loaction is hardcoded
        '''
        cls.get_search_space("evolf/domains/mnist/config.hocon")
        b = cls.full_search_space.get('binary')
        u = cls.full_search_space.get('unary')
        unary = {}
        binary = {}
        for k in u:
            unary[k] = [cls.symbolic_search_space[k], u.get(k)]
        for k in b:
            try:
                binary[k[1]] = [cls.symbolic_search_space[k[1]], b.get(k)]
            except:
                binary[k] = [cls.symbolic_search_space[k], b.get(k)]
        function_library.expression_functions['unary'] = unary
        function_library.expression_functions['binary'] = binary

