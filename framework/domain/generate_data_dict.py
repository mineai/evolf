class GenerateDataDict:

    def __init__(self, data_config):
        self.data_config = data_config

    def get_data(self):
        """
        This Function is overriden
        to generate the data and must
        return the predictors and the labels
        :return:
        """
        raise NotImplementedError

    def process_data(self, predictors, labels):
        train_percentage = self.data_config.get("train_percentage")
        validation_percentage = self.data_config.get("validation_percentage")
        test_percentage = self.data_config.get("test_percentage")
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