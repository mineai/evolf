import os

class LoadKerasEvaluator:
    """""
    This class loads a Keras model from given paths
    """""

    def __init__(self, model_path, model_file_name, weight_file_name=None):
        self.model_path = model_path
        self.model_file_name = model_file_name
        self.weight_file_name = weight_file_name

    def construct_path(self, model_folder, model_file_name, weight_file_name=None):
        """""
        This function constructs the path to load the model and the weights
        file.
        """""
        if not len(model_folder.strip()):
            model_path = f"{model_file_name}"
            weights_path = weight_file_name
        else:
            model_path = f'{model_folder}/{model_file_name}'
            weights_path = os.path.join(model_folder, weight_file_name)

        return model_path, weights_path

    def initialize_model(self):
        """
        Thuis function loads the model and its weights.
        :param model_path: The folder where the model is located
        :param model_file_name: The filename of the JSON model
        :param weight_file_name: The filename of the H5 weights
        :return model: Keras Model
        """
        from keras.models import model_from_json

        # Construct the path
        model_path, weights_path = self.construct_path(self.model_path,
                                                       self.model_file_name,
                                                       self.weight_file_name)

        # Initialize the model
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)

        # Load the weights
        model.load_weights(weights_path)

        return model

    def compile_model(self, model, loss):
        import keras
        model.compile(loss=loss,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])

        return model



