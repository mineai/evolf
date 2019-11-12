from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D, concatenate
import keras

from tqdm import trange

class NetworkConstructor:

    def __init__(self, number_of_models, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.number_of_models = number_of_models
        self.models_cut, self.models_complete = [], []
        for model_num in range(number_of_models):
            model_cut, model_complete = self.create_base_model(input_shape,
                                                      num_classes,
                                                      f"split_model_{model_num}")
            self.models_cut.append(model_cut)
            self.models_complete.append(model_complete)

        self.models_complete[0].summary()

        for model in self.models_complete:
            model.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adadelta(),
                          metrics=['accuracy'])

        self.comination_model = self.create_combination(self.models_cut,
                                                        self.num_classes)


    def train_split_models(self, train_x_sets, train_t_sets, validation_set, epochs=25):
        for model_num in trange(len(self.models_complete)):
            model = self.models_complete[model_num]

            train_x_set = train_x_sets[model_num]
            train_t_set = train_t_sets[model_num]

            model.fit(train_x_set, train_t_set,
                      batch_size=32,
                      epochs=epochs,
                      verbose=True)
            scores = model.evaluate(validation_set[0], validation_set[1])
            print("Validation Accuracy: ", scores[1])

    def freeze_combination_model_layers(self):
        for layer in self.comination_model.layers[:-1]:
            class_name = layer.__class__.__name__
            if class_name == 'Model':
                for nested_layer in layer.layers[1:]:
                    nested_layer.trainable = False

    def compile_and_train_combination_model(self, train_x, train_t, test_set, epochs=50):
        self.comination_model.compile(loss='categorical_crossentropy',
                            optimizer=keras.optimizers.Adadelta(),
                            metrics=['accuracy'])

        full_training_data_x = [train_x] * self.number_of_models
        full_test_data_x = [test_set[0]] * self.number_of_models

        self.comination_model.summary()

        self.comination_model.fit(full_training_data_x,
                        train_t,
                        batch_size=32,
                        epochs=epochs,
                        verbose=True)

        scores = self.comination_model.evaluate(full_test_data_x, test_set[1])
        print("Validation Accuracy: ", scores[1])

    @staticmethod
    def create_base_model(input_shape, num_classes, name):
        input_layer = Input(shape=input_shape)
        conv = Conv2D(64, kernel_size=(3, 3),
                      activation='relu')(input_layer)
        conv = Conv2D(64, kernel_size=(3, 3),
                      activation='relu')(conv)
        max_pool_1 = MaxPooling2D(pool_size=(2, 2))(conv)

        conv = Conv2D(128, kernel_size=(3, 3),
                      activation='relu')(max_pool_1)
        conv = Conv2D(128, kernel_size=(3, 3),
                      activation='relu')(conv)
        conv = Conv2D(128, kernel_size=(3, 3),
                      activation='relu')(conv)
        conv = Conv2D(128, kernel_size=(3, 3),
                      activation='relu')(conv)
        max_pool_1 = MaxPooling2D(pool_size=(2, 2))(conv)
        conv2 = Conv2D(10, kernel_size=(3, 3),
                      activation='relu')(max_pool_1)
        dropout_1 = Dropout(0.25)(conv2)

        flatten = Flatten()(dropout_1)
        dense = Dense(2, activation='relu')(flatten)
        dropout_2 = Dropout(0.5)(dense)
        output = Dense(num_classes, activation='softmax')(dropout_2)

        model_cut = Model(inputs=[input_layer], outputs=[conv], name=f"{name}_cut")
        model_complete = Model(inputs=[input_layer], outputs=[output], name=f"{name}_full")

        return model_cut, model_complete

    @staticmethod
    def create_combination_model(input_shape, num_classes):
        input_layer = Input(shape=input_shape[1:])
        conv = Conv2D(64, kernel_size=(1, 1),
                      activation='relu')(input_layer)
        conv = Conv2D(64, kernel_size=(1, 1),
                      activation='relu')(conv)
        conv = Conv2D(64, kernel_size=(3, 3),
                      activation='relu')(conv)
        flatten = Flatten()(conv)
        dense = Dense(512, activation='relu')(flatten)
        output = Dense(num_classes, activation='softmax')(dense)

        model = Model(inputs=[input_layer],
                      outputs=[output])
        return model

    @staticmethod
    def collect_input_tensors(models):
        input_tensors = []
        for model in models:
            input_tensors.append(model.input)

        return input_tensors

    @staticmethod
    def create_combination(models, num_classes):
        input_tensors = NetworkConstructor.collect_input_tensors(models)

        # Collect the Real Models
        real_models = []
        for model in models:
            model_dense_x = model(model.input)
            real_models.append(model_dense_x)

        # Concatenate
        combination_layer = concatenate(real_models, axis=-1)

        # Define Combination model
        input_shape = combination_layer._shape_tuple()
        combination_model = NetworkConstructor.create_combination_model(input_shape,
                                                                        num_classes)
        combination_model_init = combination_model(combination_layer)

        model = Model(input_tensors, combination_model_init)

        return model