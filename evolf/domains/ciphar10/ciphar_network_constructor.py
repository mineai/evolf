from evolf.evolution.network_constructor import NetworkConstructor


class CipharNetworkConstructor(NetworkConstructor):

    def __init__(self, input_shape, data_generation_config):
        NetworkConstructor.__init__(self, input_shape, data_generation_config)

    def create_model(self):
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten, Activation
        from keras.layers import Conv2D, MaxPooling2D

        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same',
                         input_shape=self.input_shape))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes))
        model.add(Activation('softmax'))

        return model
