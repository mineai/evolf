import argparse

from evolf.domains.ciphar10.ciphar_network_constructor import CipharNetworkConstructor
from evolf.domains.ciphar10.generate_ciphar_data import GenerateCipharData
from evolf.evolution.session_server import SessionServer
from evolutionary_algorithms.servicecommon.parsers.parse_hocon import ParseHocon

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This server is used to evolve a loss function for the Ciphar Dataset")
    # The model name should not have .json
    parser.add_argument("--config",
                        help="The Hocon Config file location")
    args = parser.parse_args()
    # Read the Config File
    conf = ParseHocon().parse(args.config)
    domain_config = conf.get("domain_config")
    domain_name = domain_config.get("domain")

    print(f"################################# Evolf is currently Running on {domain_name}")
    data_config = domain_config.get("data_config")

    data_dict = GenerateCipharData.get_data(data_config)

    model_generation_config = domain_config.get("model_generation")
    generate_model = model_generation_config.get("generate_model")

    if generate_model:
        network_constructor = CipharNetworkConstructor(data_dict.get("input_shape"), model_generation_config)
        network_constructor.create_model()
        network_constructor.complie_model()
        network_constructor.save_model()

    session_server = SessionServer(conf, data_dict)
    session_server.evolve()
