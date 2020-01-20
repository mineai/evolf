from flask import Flask, request
import pickle

from servicecommon.utils.cosntruct_class_from_path import ConstructClassFromPath

class EvaluatorServer:

    def __init__(self, evaluator_config, data_config, model_config):
        self.evaluator_config = evaluator_config
        self.data_config = data_config
        self.model_config = model_config

    def generate_data(self, DataGeneratorClass):
        """
        This function creates the data dictionary
        needed by EVOLF from the client provided script
        :param DataGeneratorClass: Class Defined by the user.
        :returns data_dict: Dictionary containing the train, test
        and validation sets
        """
        data_generator_object = DataGeneratorClass(self.data_config)
        predictors, labels = data_generator_object.get_data()
        data_dict = data_generator_object.process_data(predictors, labels)
        return data_dict

    def serialize_data_dict(self, data_dict):
        """
        This function serializes the data_dictionary.
        :param data_dict: Dictionary containing the train, test
        and validation sets
        :return serialize_data: Pickled version of the data
        """
        serialized_data = pickle.dumps(data_dict)
        return serialized_data

    def persist_data(self):
        data_generator_path = self.data_config("data_generator_class_path")
        data_generator_class = self.data_config("data_generator_class_name")
        DataGeneratorClass = ConstructClassFromPath.construct(data_generator_path,
                                                              data_generator_class)
        data_dict = self.generate_data(DataGeneratorClass)
        serialzied_data = pickle.dumps(data_dict)

    def restore_data(self):
        pass

    def persist_model(self):
        pass

    def load_model(self):
        pass


"""
Setup Gateway Microservice
"""
evaluator_service_app = Flask(__name__)

"""
Set Up Routes
"""

# 1) Setup Config
@evaluator_service_app.route("/initialize", methods=["POST"])
def setup_config():
    global evaluator_config
    global data_config
    global model_config

    pickled_data = request.data
    evaluator_config = pickle.loads(pickled_data)

    data_config = evaluator_config.get("data_config")
    model_config = evaluator_config.get("model_config")

    return 200

if __name__ == '__main__':

    evaluator_service_app.run(host="0.0.0.0",
                               port=2000,
                               debug=True)

# # From the arguments decode the Data generator
# # and the model generator package paths
# DataGeneratorClass = ConstructClassFromPath.construct(self.data_generator_class_path)
# DomainNetworkConstructionClass = ConstructClassFromPath.construct(self.model_generator_class_path)
#
# # Generate the data from the client provided script
# self.data_dict = self.generate_data(DataGeneratorClass)
#
# # Generate the Model for the network
# if self.model_config.get("generate_model"):
#     self.generate_model(DomainNetworkConstructionClass)




