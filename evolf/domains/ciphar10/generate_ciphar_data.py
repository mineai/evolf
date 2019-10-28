
class GenerateCipharData:

    @staticmethod
    def get_data(data_config):

        import keras
        from keras.datasets import cifar10
        import numpy as np

        num_classes = 10

        # the function_str, split between train and test sets
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        x = np.concatenate((x_train, x_test))
        y = np.concatenate((y_train, y_test))

        train_percentage = data_config.get("train_percentage")
        validation_percentage = data_config.get("validation_percentage")
        test_percentage = data_config.get("test_percentage")

        # convert class vectors to binary class matrices
        x = x.astype('float32')
        y = keras.utils.to_categorical(y, num_classes)

        num_samples = len(x)
        num_train_samples = int( num_samples * train_percentage )
        num_validation_samples = int(num_samples * validation_percentage)
        num_test_samples = int(num_samples * test_percentage)

        x_train, y_train = x[:num_train_samples], y[:num_train_samples]
        x_validation, y_validation = x[num_train_samples:num_train_samples +num_validation_samples], \
                                     y[num_train_samples:num_train_samples +num_validation_samples]
        x_test, y_test = x[num_train_samples +num_validation_samples:], \
                                     y[num_train_samples +num_validation_samples:]

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
