import argparse
import os

import yaml

from servicecommon.parsers.hocon_parser import ParseHocon
from servicecommon.persistor.local.json.json_persistor import JsonPersistor


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

        return config
