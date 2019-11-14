class OriginalNetwork:

    @staticmethod
    def get_orignal_network(input_shape, num_classes):
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten, Activation
        from keras.layers import Conv2D, MaxPooling2D

        model = Sequential()

        model.add(Conv2D(64, (3, 3),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(64, (3, 3),
                         input_shape=input_shape, activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(128, (3, 3),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(128, (3, 3),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(128, (3, 3),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(128, (3, 3),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(1280, (3, 3),
                         input_shape=input_shape, activation='relu'))

        model.add(Conv2D(64, (1, 1),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(64, (1, 1),
                         input_shape=input_shape, activation='relu'))
        model.add(Conv2D(64, (3, 3),
                         input_shape=input_shape, activation='relu'))

        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(num_classes, activation='softmax'))

        return model