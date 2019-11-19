import argparse
import os

import yaml

from evolf.servicecommon.persistor.local.json.json_persistor import JsonPersistor
from string_evolve.servicecommon.parsers.parse_hocon import ParseHocon


class ArgumentParser:

    @staticmethod
    def add_parser():
        parser = argparse.ArgumentParser(description="This server is used to evolve a loss function")
        # The model name should not have .json
        parser.add_argument("--config",
                            help="The Hocon Config file location")
        args = parser.parse_args()
        # Read the Config File
        config = ParseHocon().parse(args.config)
        studio_conf = config.get("studio_config")

        temp_folder_path = os.path.join(os.getcwd(), "temp/")
        studio_yaml_path = os.path.join(temp_folder_path, "studio/")
        if not os.path.exists(studio_yaml_path):
            os.makedirs(studio_yaml_path)
        yaml_file = os.path.join(studio_yaml_path, "studio_config.yaml")
        config_json_path = os.path.join(temp_folder_path, "config/")

        studio_config_file = open(yaml_file, 'w')
        studio_conf = yaml.dump(studio_conf, studio_config_file, default_flow_style=False)
        studio_config_file.close()

        json_persistor = JsonPersistor(base_file_name='config', folder=config_json_path)
        json_persistor.persist(config)

