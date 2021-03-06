import os

class LoadKerasEvaluator:

    def __init__(self, evaluator_config):
        self.model_path = evaluator_config.get("model_path")
        self.model_file_name = evaluator_config.get("model_file_name")
        self.weight_file_name = evaluator_config.get("weight_file_name")
        self.model = self.initialize_model()

    def initialize_model(self):
        from keras.models import model_from_json
        if not len(self.model_path.strip()):
            path = f"{self.model_file_name}"
            weight_path = self.weight_file_name
        else:
            path = f'{self.model_path}/{self.model_file_name}'
            weight_path = os.path.join(self.model_path, self.weight_file_name)
        json_file = open(path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()

        model = model_from_json(loaded_model_json)
        
        try:
            model.load_weights(weight_path)
        except:
            print("Failed to Load Weights")

        return model


