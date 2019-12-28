import argparse

from framework.interfaces.parser.argument_parser import ArgumentParser
from servicecommon.parsers.hocon_parser import ParseHocon


class DomainArgParser(ArgumentParser):
    """
    This class adds the command line argument
    supplier to the Session Server.

    NOTE: This argument parser is very specific to the
    SessionServer to EVOLF !!!
    """

    def __init__(self):
        self.config, self.experiment_id = self.add_parser()

    def add_parser(self):
        """""
        This function adds the argument parser
        to take in inputs from the CLI
        :return config: A dictionary parsed from the supplied Hocon
        """""
        parser = argparse.ArgumentParser(description="This server is used to evolve a loss function")
        parser.add_argument("--config",
                            help="The Hocon Config file location")
        parser.add_argument("--experiment_id",
                            help="Experiment Id for this run", default=None)
        args = parser.parse_args()
        # Read the Config File
        config = ParseHocon().parse(args.config)
        experiment_id = args.experiment_id
        return config, experiment_id


    def absorb_args(self):
        """""
        This function extracts the necessary parameters from the supplied
        config and initializes them as class variables.
        """""
        # Get the backend to use
        backend = self.config.get("backend")

        # Get the domain Config
        domain_config = self.config.get("domain_config")
        domain_name = domain_config.get("domain")
        data_generator_class_path = domain_config.get("data_generator_class_path")
        model_generator_class_path = domain_config.get('model_generator_class_path')
        data_config = domain_config.get("data_config")

        evolution_config = self.config.get("evolution_config")
        search_space = self.config.get("search_space")
        state_of_the_art_config = self.config.get("state_of_the_art_config")
        evaluator_config = self.config.get("evaluator_config")
        visualization_config = self.config.get("visualization_config")
        persistence_config = self.config.get("persistence_config")
        studio_config = self.config.get("studio_config")

        return backend, domain_config, domain_name, data_generator_class_path, \
               model_generator_class_path, data_config, evaluator_config, \
               search_space, state_of_the_art_config, evolution_config, visualization_config, \
               persistence_config, studio_config
