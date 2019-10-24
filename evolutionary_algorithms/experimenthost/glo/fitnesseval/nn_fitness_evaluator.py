import time
import keras

from evolutionary_algorithms.experimenthost.glo.fitnesseval.initialize_keras_model import InitializeKerasModel


class TimeHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)


class NNFitnessEvaluator(InitializeKerasModel):

    def __init__(self, tree, evaluator_config, data_dict=None):
        InitializeKerasModel.__init__(self, tree, evaluator_config)
        self.epochs = evaluator_config.get("epochs", 1)
        self.verbose = evaluator_config.get("verbose", 1)
        self.batch_size = evaluator_config.get("batch_size", 32)

        if data_dict:
            self.x_train = data_dict.get("x_train")
            self.y_train = data_dict.get("y_train")
            self.x_test = data_dict.get("x_test")
            self.y_test = data_dict.get("y_test")

        self.score = None
        self.times = None

    def train(self):
        time_callback = TimeHistory()
        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(self.x_test, self.y_test),
                       callbacks=[time_callback])
        self.times = time_callback.times

    def evaluate(self):
        self.score = self.model.evaluate(self.x_test, self.y_test, verbose=self.verbose)
