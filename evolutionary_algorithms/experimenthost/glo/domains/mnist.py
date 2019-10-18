from __future__ import print_function

import calendar
import os, sys
import time

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from tqdm import trange

from evolutionary_algorithms.experimenthost.glo.evaluation_validation.loss_funciton_constructor import \
    LossFunctionConstructor
from evolutionary_algorithms.experimenthost.glo.populate.population import Population

from evolutionary_algorithms.experimenthost.glo.utils.statistics import Statistics
from evolutionary_algorithms.servicecommon.persistor.local.json.json_persistor import JsonPersistor

import numpy as np

def get_data():
    num_classes = 10
    # input image dimensions
    img_rows, img_cols = 28, 28

    # the function_str, split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return x_train, x_test, y_train, y_test, input_shape


class TimeHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)


class GloMnist:

    def __init__(self, tree, data, batch_size=128, epochs=3):
        self.x_train, self.x_test, \
        self.y_train, self.y_test, self.input_shape = data
        self.num_classes = 10
        self.model = self.create_conv_model()
        self.tree = tree
        self.loss = LossFunctionConstructor.construct_loss(self.tree)
        self.batch_size = batch_size
        self.epochs = epochs
        self.score = []
        self.times = []

    def create_conv_model(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=self.input_shape))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        return model

    def compile_model(self):
        self.model.compile(loss=self.loss,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])

    def train(self):
        time_callback = TimeHistory()
        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(self.x_test, self.y_test))
        self.times = time_callback.times

    def evaluate(self):
        self.score = self.model.evaluate(self.x_test, self.y_test, verbose=0)


class GLO:

    def __init__(self, min_height=2, max_height=5, pop_size=100):
        self.population = Population(min_height, max_height, pop_size)
        self.population.generate_population()
        self.population.get_working_trees()

        self.data = get_data()
        self.experiment_id = calendar.timegm(time.gmtime())

    def persist(self, tree, tree_idx, base_dir=None):

        if base_dir is None:
            base_dir = f"{os.getcwd()}/results/mnist/glo_mnist_{self.experiment_id}/candidates"

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        candidate_path = f"{base_dir}/tree_{tree_idx}"
        os.makedirs(candidate_path)
        stats = Statistics.statistics(tree)

        json_persistor = JsonPersistor("stats", candidate_path)
        json_persistor.persist(stats)

        # pickle_persistor = PicklePersistor("tree", candidate_path)
        # pickle_persistor.persist(tree)

    def persist_best_candidate(self, best_candidate):
        base_dir = f"{os.getcwd()}/results/mnist/glo_mnist_{self.experiment_id}/"
        stats = Statistics.statistics(best_candidate)

        json_persistor = JsonPersistor("stats", base_dir)
        json_persistor.persist(stats)

    def run(self):
        print(f"To refer to this test Experiment, the ID is: {self.experiment_id}")
        for tree_idx in trange(len(self.population.working_trees)):
            tree = self.population.working_trees[tree_idx]
            glo_mnist_NN = GloMnist(tree, self.data, epochs=1)

            print(" \n\n ######################################################## \n\n ")
            tree.generate_printable_expression()
            print("\n\n")

            try:
                glo_mnist_NN.compile_model()
                glo_mnist_NN.train()
                glo_mnist_NN.evaluate()
            except:
                print("\n\n This tree failed while training \n\n")

            self.persist(tree, tree_idx)

            if len(glo_mnist_NN.score):
                tree.fitness = glo_mnist_NN.score[1]
            tree.avg_epoch_time = np.mean(glo_mnist_NN.times)
            print(f"Fitness: {tree.fitness}")
            print(f"Avg_time: {tree.avg_epoch_time}")
            print(" \n\n ######################################################## \n\n ")

        print(f"To refer to this test Experiment, the ID is: {self.experiment_id}")


glo_obj = GLO()
glo_obj.run()

fitness = []
[fitness.append(x.fitness) for x in glo_obj.population.working_trees]

if len(fitness):
    best_fitness_candidate = np.argmax(filter(lambda x: x != None, fitness))
    print("\n\n Best fitness was of Candidate: ", best_fitness_candidate)
else:
    print("All trees failed")
