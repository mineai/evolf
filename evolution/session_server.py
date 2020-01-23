from searchspace.search_space import SearchSpace
from searchspace.populate_search_space import PopulateSearchSpace
from framework.serialize.population.population_serializer import PopulationSerializer
from servicecommon.parsers.argumentparsers.domain_arg_parser import DomainArgParser
from servicecommon.filer.experiment_filer import ExperimentFiler
from evolution.config_handler import ConfigHandler
import pickle
import requests
import os
# os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"


SERVICE_ENDPOINTS = {

    "population_service": {
        "initialize_search_space": "http://127.0.0.1:5000/initialize",  # POST
        "initial_population": "http://127.0.0.1:5000/request_inital_population"  # POST
    },
    "evaluation_service": {
        "initialize_config": "http://127.0.0.1:2000/initialize",  # POST
    }

}


class SessionServer():
    """""
    This class serves as the entry point to Evolf.
    """""

    def __init__(self):
        """""
        The Constructor Initializes the Domain with the
        config and carries out the model building and
        the data generation
        :param DomainNetworkConstructionClass: Client supplied class to generate Network
        :param DataGeneratorClass: Client supplied class to generate Data
        """""
        # Add the Parser to read the config from the
        # command line and initialize configs
        self.domain_arg_parser = DomainArgParser()
        self.config, self.experiment_id = self.domain_arg_parser.add_parser()

        # Initialize Config Handler
        self.config_handler = ConfigHandler(self.config)
        self.config = self.config_handler.overlay_config()

        # Absorb the Args
        self.backend, self.domain_config, self.domain_name, self.data_generator_class_path, \
            self.model_generator_class_path, \
            self.data_config, self.evaluator_config, self.search_space, \
            self.state_of_the_art_config, self.evolution_config, \
            self.visualization_config, self.persistence_config, \
            self.studio_config = self.domain_arg_parser.absorb_args()

        # Get the search space
        self.search_space_obj = SearchSpace()
        self.search_space_obj = PopulateSearchSpace.populate_search_space(self.search_space_obj,
                                                                          self.search_space)

        self.experiment_filer = ExperimentFiler(self.experiment_id)
        self.experiment_id = self.experiment_filer.get_experiment_id()

    def generate_model(self, DomainNetworkConstructionClass):
        """""
        This function creates the NN model
        needed by EVOLF from the client provided script
        """""
        network_constructor = DomainNetworkConstructionClass(self.data_dict.get("input_shape"),
                                                             self.model_config)
        network_constructor.model = network_constructor.create_model()
        network_constructor.compile_model()
        network_constructor.save_model()

    def setup_population_service(self):
        """
        This function calls the population micro-service
        and sets up the searchspace.
        :return:
        """
        pickled_search_space = pickle.dumps(self.search_space)

        # Initialize Search Space
        search_space_endpoint = SERVICE_ENDPOINTS.get("population_service"). \
            get("initialize_search_space")
        _ = requests.post(url=search_space_endpoint,
                          data=pickled_search_space)

    def setup_evaluation_service(self):
        """
        This function calls the population micro-service
        and sets up the searchspace.
        :return:
        """
        pickled_config = pickle.dumps(self.evaluator_config)

        # Initialize Search Space
        initialize_config_endpoint = SERVICE_ENDPOINTS.get("evaluation_service"). \
            get("initialize_config")
        _ = requests.post(url=initialize_config_endpoint,
                          data=pickled_config)

    def request_initial_population(self):
        # Initialze population Endpoint
        init_population_endpoint = SERVICE_ENDPOINTS.get("population_service"). \
            get("initial_population")

        # evolution_config = pickle.dumps(self.evolution_config)
        # response = requests.post(
        #     url=init_population_endpoint, data=evolution_config)

        # create a dictionary to hold relevant job info
        job_info = {}

        # add the evolution and visualization configs to job_info
        job_info['evolution_config'] = self.evolution_config
        job_info['visualization_config'] = self.visualization_config

        response = requests.post(
            url=init_population_endpoint, json=job_info)
        # population_bytes = response._content
        # serialized_population = pickle.loads(population_bytes)
        serialized_population = response.body

        return serialized_population

    def process_serialized_population(self, serialized_population):
        population_deserializer = PopulationSerializer(serialized_population,
                                                       self.search_space_obj)
        population_obj = population_deserializer.deserialize()
        return population_obj

    def run(self):
        print(f""" ################################# 
                Evolf is currently Running on {self.domain_name} \n
                Experiment ID: {self.experiment_id} 
                ################################# """)

        # Setup Population Service
        self.setup_population_service()

        # Request Initial population
        serialized_initial_population = self.request_initial_population()

        # Deserialize Initial Population
        initial_population = self.process_serialized_population(
            serialized_initial_population)

        [print(tree.symbolic_expression) for tree in initial_population.trees]

        # Construct Evaluator Config
        # self.evaluator_config = self.config_handler.generate_evaluator_config(self.domain_config,
        #                                                                       self.evaluator_config)
        # self.setup_evaluation_service()


if __name__ == "__main__":
    session_server = SessionServer()
    session_server.run()
