
class GenerateMnistData:

    def __init__(self):
        pass

    @staticmethod
    def get_data(data_config):

        import keras
        import keras.backend as K
        from keras.datasets import mnist
        import numpy as np

        num_classes = 10
        # input image dimensions
        img_rows, img_cols = 28, 28

        # the function_str, split between train and test sets
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x = np.concatenate((x_train, x_test))
        y = np.concatenate((y_train, y_test))

        train_percentage = data_config.get("train_percentage")
        validation_percentage = data_config.get("validation_percentage")
        test_percentage = data_config.get("test_percentage")

        if K.image_data_format() == 'channels_first':
            x = x.reshape(x.shape[0], 1, img_rows, img_cols)
            input_shape = (1, img_rows, img_cols)
        else:
            x = x.reshape(x.shape[0], img_rows, img_cols, 1)
            input_shape = (img_rows, img_cols, 1)

        x = x.astype('float32')
        x /= 255

        # convert class vectors to binary class matrices
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



        print(x.shape)

        print(x_train.shape)
        print(x_validation.shape)
        print(x_test.shape)

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
