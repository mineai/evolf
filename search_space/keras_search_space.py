import keras.backend as K
#import tensorflow as tf

class KerasSearchSpace:



    # This gives the range of possible keras functions usable
    keras_search_space = {
        "cos": K.cos,
        "sin": K.sin,
        "log": K.log,
        "exp": K.exp,
#        "tan": tf.tan,
        "square": K.square,
        "sqrt": K.sqrt,
#        "cosh": tf.math.cosh,
#        "sinh": tf.math.sinh,
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "y": "y_pred",
        "t": "y_true",
        "pos_scalar": 1,
        "neg_scalar": -1,
        "mean": K.mean,
        "sum": K.sum,
#        "max": tf.reduce_max,
#        "min": tf.reduce_min,
#        "acosh": tf.math.acosh,
#        "asinh": tf.math.asinh
    }



