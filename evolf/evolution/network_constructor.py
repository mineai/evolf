
class NetworkConstructor:

    def __init__(self, input_shape, model_generation_config):

        self.input_shape = input_shape
        self.num_classes = 10
        self.model = None
        self.model_generation_config = model_generation_config

    def create_model(self):
        """
        This function acts as an interface to the domains to
        create the model and the assign the model to self.model
        :return:
        """
        raise NotImplementedError

    def complie_model(self):
        assert self.model is not None, "Please Override the interface create_model in NetworkConstructo"
        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

    def save_model(self):
        import os
        self.model_json = self.model.to_json()

        model_file_name = self.model_generation_config.get("model_file_name")
        weight_file_name = self.model_generation_config.get("weight_file_name")

        path_to_write_model = self.model_generation_config.get("model_path")
        if not os.path.exists(path_to_write_model):
            os.makedirs(path_to_write_model)
        with open(f"{path_to_write_model}/{model_file_name}", "w") as json_file:
            json_file.write(self.model_json)
        self.model.save_weights(f"{path_to_write_model}/{weight_file_name}")



