import keras

import numpy as np

class Data:
    @staticmethod
    def get_data_ciphar():
        from keras.datasets import cifar10
        num_classes = 10
        # the function_str, split between train and test sets
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        x = np.concatenate((x_train, x_test))
        y = np.concatenate((y_train, y_test))

        # convert class vectors to binary class matrices
        predictors = x.astype('float32')
        labels = keras.utils.to_categorical(y, num_classes)

        print(predictors.shape)

        return predictors, labels

    @staticmethod
    def divide_data(x, t, num_sets):
        train_x_sets = np.split(x, num_sets)
        train_t_sets = np.split(t, num_sets)

        return train_x_sets, train_t_sets

    @staticmethod
    def process_data(predictors, labels, train_percentage, validation_percentage):
        num_samples = len(predictors)
        num_train_samples = int(num_samples * train_percentage)
        num_validation_samples = int(num_samples * validation_percentage)

        x_train, y_train = predictors[:num_train_samples], labels[:num_train_samples]
        x_validation, y_validation = predictors[num_train_samples:num_train_samples + num_validation_samples], \
                                     labels[num_train_samples:num_train_samples + num_validation_samples]
        x_test, y_test = predictors[num_train_samples + num_validation_samples:], \
                         labels[num_train_samples + num_validation_samples:]

        input_shape = x_train.shape[1:]
        data_dict = {
            "x_train": x_train,
            "x_test": x_test,
            "y_train": y_train,
            "y_test": y_test,
            "x_validation": x_validation,
            "y_validation": y_validation,
            "input_shape": input_shape
        }

        return data_dict