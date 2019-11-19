
from framework.domain.network_constructor import NetworkConstructor


class MnistNetworkConstructor(NetworkConstructor):

    def __init__(self, input_shape, data_generation_config):
        NetworkConstructor.__init__(self, input_shape, data_generation_config)

    def create_model(self):
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten
        from keras.layers import Conv2D, MaxPooling2D
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=self.input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        return model

