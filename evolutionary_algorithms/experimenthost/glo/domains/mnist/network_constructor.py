import keras
import os

class NetworkConstructor:

    def __init__(self, input_shape, data_generation_config):
        self.input_shape = input_shape
        self.num_classes = 10

        # Save Large Model Locally
        self.model_medium = self.create_conv_model_medium(self.input_shape)
        self.model_medium.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        self.model_json = self.model_medium.to_json()

        model_file_name = data_generation_config.get("model_file_name")
        weight_file_name = data_generation_config.get("weight_file_name")

        path_to_write_model = data_generation_config.get("medium_model_path")
        if not os.path.exists(path_to_write_model):
            os.makedirs(path_to_write_model)
        with open(f"{path_to_write_model}/{model_file_name}", "w") as json_file:
            json_file.write(self.model_json)
        self.model_medium.save_weights(f"{path_to_write_model}/{weight_file_name}")

        # Save Small Model Locally
        self.model_small = self.create_conv_model_small(self.input_shape)
        self.model_small.compile(optimizer='rmsprop', loss='categorical_crossentropy')
        self.model_json = self.model_small.to_json()

        path_to_write_model = data_generation_config.get("small_model_path")
        if not os.path.exists(path_to_write_model):
            os.makedirs(path_to_write_model)
        with open(f"{path_to_write_model}/{model_file_name}", "w") as json_file:
            json_file.write(self.model_json)
        self.model_small.save_weights(f"{path_to_write_model}/{weight_file_name}")

    def create_conv_model_medium(self, input_shape):
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten
        from keras.layers import Conv2D, MaxPooling2D
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

    def create_conv_model_small(self, input_shape):
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten
        from keras.layers import Conv2D, MaxPooling2D
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        return model

    def clone_model(self):
        model_copy = keras.models.clone_model(self.model_medium)
        model_copy.build(self.input_shape)  # replace 10 with number of variables in input layer
        return model_copy
