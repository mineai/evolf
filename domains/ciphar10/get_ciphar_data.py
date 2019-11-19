from framework.domain.generate_data_dict import GenerateDataDict


class GetCipharDataDict(GenerateDataDict):

    def __init__(self, data_config):
        GenerateDataDict.__init__(self, data_config)

    def get_data(self):
        import keras
        from keras.datasets import cifar10
        import numpy as np

        num_classes = 10

        # the function_str, split between train and test sets
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        x = np.concatenate((x_train, x_test))
        y = np.concatenate((y_train, y_test))

        # convert class vectors to binary class matrices
        predictors = x.astype('float32')
        labels = keras.utils.to_categorical(y, num_classes)

        return predictors, labels
