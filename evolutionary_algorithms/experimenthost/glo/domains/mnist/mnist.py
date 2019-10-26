import argparse

from evolutionary_algorithms.experimenthost.glo.domains.mnist.generate_mnist_data import GenerateMnistData
from evolutionary_algorithms.experimenthost.glo.domains.mnist.network_constructor import NetworkConstructor
from evolutionary_algorithms.experimenthost.glo.evolution.session_server import SessionServer
from evolutionary_algorithms.servicecommon.parsers.parse_hocon import ParseHocon

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This server is used to evolve a loss function for the MNIST Dataset")
    # The model name should not have .json
    parser.add_argument("--config",
                        help="The Hocon Config file location")
    args = parser.parse_args()
    # Read the Config File
    conf = ParseHocon().parse(args.config)
    domain_config = conf.get("domain_config")
    data_config = domain_config.get("data_config")

    data_dict = GenerateMnistData.get_data(data_config)

    model_generation_config = domain_config.get("model_generation")
    generate_data = model_generation_config.get("generate_data")

    if generate_data:
        NetworkConstructor(data_dict.get("input_shape"), model_generation_config)
    session_server = SessionServer(conf, data_dict)
    session_server.evolve()
