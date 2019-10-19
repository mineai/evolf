import keras
import time
from evolutionary_algorithms.experimenthost.glo.evaluation_validation.loss_funciton_constructor import \
    LossFunctionConstructor


class TimeHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)


class NetworkInitializer:

    def __init__(self, tree, data, network_constructor_obj, batch_size=128, epochs=3):
        self.x_train, self.x_test, \
        self.y_train, self.y_test, self.input_shape = data
        self.num_classes = 10
        self.tree = tree
        self.loss = LossFunctionConstructor.construct_loss(self.tree)
        self.batch_size = batch_size
        self.epochs = epochs
        self.score = []
        self.times = []

        self.model = network_constructor_obj.clone_model()
        self.model.set_weights(network_constructor_obj.initial_model_weights)

    def compile_model(self):
        try:
            self.model.compile(loss=self.loss,
                          optimizer=keras.optimizers.Adadelta(),
                          metrics=['accuracy'])
            return True
        except:
            # print("\n\n This tree failed while training \n\n")
            self.tree.working = False
            return False

    def train(self):
        time_callback = TimeHistory()
        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(self.x_test, self.y_test), callbacks=[time_callback])
        self.times = time_callback.times

    def evaluate(self):
        self.score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
