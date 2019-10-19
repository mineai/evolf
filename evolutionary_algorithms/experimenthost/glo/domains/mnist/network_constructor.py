from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import keras

class NetworkConstructor:

    def __init__(self, input_shape):
        self.input_shape = input_shape
        self.num_classes = 10
        self.initial_model = self.create_conv_model(self.input_shape)
        self.initial_model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        self.initial_model_weights = self.initial_model.get_weights()

    def create_conv_model(self, input_shape):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=input_shape))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        return model

    def clone_model(self):
        model_copy = keras.models.clone_model(self.initial_model)
        model_copy.build(self.input_shape)  # replace 10 with number of variables in input layer
        return model_copy
