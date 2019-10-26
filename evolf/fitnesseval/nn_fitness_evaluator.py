import time
from evolf.fitnesseval.initialize_keras_model import InitializeKerasModel


class NNFitnessEvaluator(InitializeKerasModel):

    def __init__(self, tree, evaluator_config, data_dict=None):
        if "loss" in evaluator_config.keys():
            loss = evaluator_config.get("loss")
        else:
            loss = None

        InitializeKerasModel.__init__(self, tree, evaluator_config, loss)
        self.epochs = evaluator_config.get("epochs", 1)
        self.verbose = evaluator_config.get("verbose", 1)
        self.batch_size = evaluator_config.get("batch_size", 32)
        if data_dict:
            self.x_train = data_dict.get("x_train")
            self.y_train = data_dict.get("y_train")
            self.x_test = data_dict.get("x_test")
            self.y_test = data_dict.get("y_test")
            self.x_validation = data_dict.get("x_validation")
            self.y_validation = data_dict.get("y_validation")

        self.score = None
        self.times = None

    def train(self):
        import keras

        class TimeHistory(keras.callbacks.Callback):
            def on_train_begin(self, logs={}):
                self.times = []

            def on_epoch_begin(self, batch, logs={}):
                self.epoch_time_start = time.time()

            def on_epoch_end(self, batch, logs={}):
                self.times.append(time.time() - self.epoch_time_start)

        time_callback = TimeHistory()
        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=self.verbose,
                       validation_data=(self.x_validation, self.y_validation),
                       callbacks=[time_callback])
        self.times = time_callback.times

    def evaluate(self):
        self.score = self.model.evaluate(self.x_test, self.y_test, verbose=self.verbose)
