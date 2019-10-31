import keras.backend as K
import tensorflow as tf
from evolutionary_algorithms.servicecommon.parsers.parse_hocon import ParseHocon
from evolf.populate.function_library import FunctionLibrary


class KerasSearchSpace:
    full_search_space = {}

    # This gives the range of possible keras functions usable
    keras_search_space = {
        "cos": K.cos,
        "sin": K.sin,
        "log": K.log,
        "exp": K.exp,
        "tan": tf.tan,
        "square": K.square,
        "sqrt": K.sqrt,
        "cosh": tf.math.cosh,
        "sinh": tf.math.sinh,
        "+": lambda x, y: tf.add(x, y),
        "-": lambda x, y: tf.subtract(x, y),
        "*": lambda x, y: tf.multiply(x, y),
        "/": lambda x, y: tf.divide(x, y),
        "y": "y_pred",
        "t": "y_true",
        "pos_scalar": 1,
        "neg_scalar": -1,
        "mean": tf.reduce_mean,
        "sum": tf.reduce_sum,
        "max": tf.reduce_max,
        "min": tf.reduce_min
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
            unary[k] = [cls.keras_search_space[k], u.get(k)]
        for k in b:
            try:
                binary[k[1]] = [cls.keras_search_space[k[1]], b.get(k)]
            except:
                binary[k] = [cls.keras_search_space[k], b.get(k)]
        function_library.tensorflow_functions['unary'] = unary
        function_library.tensorflow_functions['binary'] = binary




