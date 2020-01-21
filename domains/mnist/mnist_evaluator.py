from framework.domain.evaluator.domain_evaluator import DomainEvaluator


class MnistEvaluator(DomainEvaluator):
    """
    This class overrides DomainEvaluator and its functions override
    the required functions required by EVOLF to evolve a loss function.
    This serves as an example domain to demonstrate the power of EVOLF.
    """

    def get_data_config(self):
        """
        Not an override !!!!
        This function is used by the domain to generate the train-test split.
        :return data_config: Dictionary containing the training and validation
        percentages
        """

        data_config = {
            "train_percentage": 0.75,
            "validation_percentage": 0.1
        }
        return data_config

    def process_data(self, predictors, labels):
        """
        Not an Override !!!!!
        This function is used to generate the data_dict required to
        override the load_data function.
        :param predictors: The X values to be passed to the evaluator
        :param labels: The targets to be passed th the evaluator
        :return data_dict: Dictionary containing the train, test and validation sets.
        """
        data_config = self.get_data_config()
        train_percentage = data_config.get("train_percentage")
        validation_percentage = data_config.get("validation_percentage")
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

    def load_data(self):
        """
        This function overrides the base load_data function
        and returns the data_dict.
        :return data_dict: Dictionary containing the train, test and validation sets.
        """
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

        data_dict = self.process_data(predictors, labels)

        return data_dict

    def build_evaluator_model(self):
        """
        This function overrides the base interface function of DomainEvaluator, specifically
        of NetworkConstructor to build a simple Keras model that serves as the evaluator.
        :return model: Evaluator Model to be used
        """
        data_dict = self.load_data()
        num_classes = 10
        from keras.models import Sequential
        from keras.layers import Dense, Dropout, Flatten
        from keras.layers import Conv2D, MaxPooling2D
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=data_dict.get("input_shape")))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))

        return model

    def get_evaluator_config(self):
        """
        Not an Override !!!!
        This function is not an override but used
        within the functions of this class.
        :return evaluator_config: Config for training
        """
        evaluator_config = {
            "epochs": 10,
            "verbose": True,
            "batch_size": 500
        }

        return evaluator_config

    def compile_model(self, model, loss):
        """
        Not an Override !!!!!
        Thus function compiles the evaluator, in this
        case a keras model
        :param model: Keras model to be evaluated
        :param loss: Loss that will be used to evaluate performance
        :return model: Compiled Keras Model
        """
        import keras
        model.compile(loss=loss,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])

        return model

    def initialize_data(self, data_dict):
        """
        Not an Override !!!!
        This function reads in the data_dict
        and returns the train, test and validation variables.
        :param data_dict: Dictionary containing the data splits
        :return:
        """
        x_train = data_dict.get("x_train")
        y_train = data_dict.get("y_train")
        x_test = data_dict.get("x_test")
        y_test = data_dict.get("y_test")
        x_validation = data_dict.get("x_validation")
        y_validation = data_dict.get("y_validation")

        return x_train, y_train, \
               x_test, y_test, \
               x_validation, y_validation

    def evaluate_loss(self, evaluator_model, data_dict, loss,
                      loss_evaluator_config={}):
        """
        This function overrides the base function to evaluate the loss
        function with the model we created.

        NOTE: This domain uses a Keras NN to evaluate the network and thus we
        do not override the handles in the search space.

        :param loss_evaluator_config: Config of the evaluator
        :param evaluator_model: The model that needs to be evaluated
        :param data_dict: The Data splits
        :param loss: The loss function generated by EVOLF
        :return metrics: A dictionary containing the metrics to optimize for
        """
        # Compile the evaluator
        compiled_evaluator_model = self.compile_model(evaluator_model, loss)

        # Set up early stopping
        from keras.callbacks import EarlyStopping
        early_stopping_callback = EarlyStopping(monitor="val_acc",
                                                mode="max",
                                                verbose=True,
                                                patience=4,
                                                min_delta=2)

        # Get Data
        x_train, y_train, \
        x_test, y_test, \
        x_validation, y_validation = self.initialize_data(data_dict)

        # Get the Config for training if no config provided. Does
        # not need to be here but just a safety check.
        if not loss_evaluator_config:
            loss_evaluator_config = self.get_evaluator_config()

        # Get the params from the config
        batch_size = loss_evaluator_config.get("batch_size", 32)
        epochs = loss_evaluator_config.get("epochs", 1)
        verbose = loss_evaluator_config.get("verbose", 1)

        # Train the model
        compiled_evaluator_model.fit(x_train, y_train,
                                     batch_size=batch_size,
                                     epochs=epochs,
                                     verbose=verbose,
                                     validation_data=(x_validation, y_validation),
                                     callbacks=[early_stopping_callback])

        # Get the Test Accuracy and Loss
        scores = compiled_evaluator_model.evaluate(x_test,
                                                     y_test,
                                                     verbose=True)
        loss = scores[0]
        test_acc = scores[1]

        metrics = {
            "test_acc": test_acc,
            # "loss": loss
        }

        return metrics
