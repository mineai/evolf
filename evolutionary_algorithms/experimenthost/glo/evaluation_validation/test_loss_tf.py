from sympy import *
import tensorflow as tf
from keras.layers import Dense, Input
import keras.backend as K

# Build a Symbolic Function
y_pred, y_true = Symbol("y_pred"), Symbol("y_true")
expression = tf.reduce_mean(tf.square(y_pred) - y_true)

print(expression)


def loss(y_pred, y_true):

    stack = []
