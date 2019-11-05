import keras.backend as K
import tensorflow as tf


class KerasSearchSpace:

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



