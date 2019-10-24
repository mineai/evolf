import argparse

from evolutionary_algorithms.experimenthost.glo.domains.mnist.generate_mnist_data import GenerateMnistData
from evolutionary_algorithms.experimenthost.glo.evolution.session_server import SessionServer
from evolutionary_algorithms.servicecommon.parsers.parse_hocon import ParseHocon

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This server is used to evolve strings")
    # The model name should not have .json
    parser.add_argument("--config",
                        help="The Hocon Config file location")
    args = parser.parse_args()
    # Read the Config File
    conf = ParseHocon().parse(args.config)
    data_dict = GenerateMnistData.get_data()
    session_server = SessionServer(conf, data_dict)
    session_server.evolve()