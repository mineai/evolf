from evolf.framework.domain.generate_data_dict import GenerateDataDict


class GetMnistData(GenerateDataDict):

    def __init__(self, data_config):
        GenerateDataDict.__init__(self, data_config)

    def get_data(self):
        import keras
        from keras.datasets import mnist
        import numpy as np

        num_classes = 10
        # the function_str, split between train and test sets
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x = np.concatenate((x_train, x_test))
        y = np.concatenate((y_train, y_test))

        # convert class vectors to binary class matrices
        predictors = x.astype('float32')
        labels = keras.utils.to_categorical(y, num_classes)

        predictors = predictors.reshape([x.shape[0], x.shape[1], x.shape[2], 1])
        print(predictors.shape)

        return predictors, labels
