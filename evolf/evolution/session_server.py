import argparse
from evolf.evolution.evolve import Evolve
from evolf.evolution.get_default_config import GetDefaultConfig
from evolf.search_space.populate_search_space import PopulateSearchSpace
from evolf.search_space.search_space import SearchSpace
from evolf.servicecommon.utils.overlayer import Overlayer
from string_evolve.servicecommon.parsers.parse_hocon import ParseHocon


class SessionServer(Evolve):

    def __init__(self, DomainNetworkConstructionClass, DataGeneratorClass):
        parser = argparse.ArgumentParser(description="This server is used to evolve a loss function")
        # The model name should not have .json
        parser.add_argument("--config",
                            help="The Hocon Config file location")
        args = parser.parse_args()
        # Read the Config File
        self.conf = ParseHocon().parse(args.config)

        default_config = GetDefaultConfig.get_default_config()
        self.conf = Overlayer.overlay_configs(default_config, self.conf)

        self.domain_config = self.conf.get("domain_config")
        self.domain_name = self.domain_config.get("domain")

        self.search_space = self.domain_config.get("search_space")

        print(f"################################# Evolf is currently Running on {self.domain_name}")
        self.data_config = self.domain_config.get("data_config")

        self.model_generation_config = self.domain_config.get("model_generation")

        data_generator_object = DataGeneratorClass(self.data_config)
        predictors, labels = data_generator_object.get_data()
        self.data_dict = data_generator_object.process_data(predictors, labels)

        generate_model = self.model_generation_config.get("generate_model")
        if generate_model:
            network_constructor = DomainNetworkConstructionClass(self.data_dict.get("input_shape"),
                                                                 self.model_generation_config)
            network_constructor.model = network_constructor.create_model()
            network_constructor.compile_model()
            network_constructor.save_model()

        self.search_space_obj = SearchSpace()
        self.search_space_obj = PopulateSearchSpace.populate_search_space(self.search_space_obj,
                                                                          self.search_space)
        print(self.search_space_obj.search_space)
        super().__init__(self.conf, self.data_dict, self.search_space_obj)

    def run(self):
        self.evolve()
