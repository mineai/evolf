import argparse

from framework.interfaces.parser.argument_parser import ArgumentParser

class TreeNNAccArgumentParser(ArgumentParser):

    def add_parser(self):
        parser = argparse.ArgumentParser(description="This server is used train the NN for the tree")
        parser.add_argument("--evaluator_config",
                            help="The Hocon Config file location")
        parser.add_argument("--tree_location",
                            help="Location of the un-serialized Tree")
        args = parser.parse_args()

        return args

    def absorb_args(self):
        pass
