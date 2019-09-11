import argparse
from pyhocon import ConfigFactory
from multiprocessing import Process, current_process, Manager, Pool

from evolutionary_algorithms.evolve_list.evolution_functions_lib_list \
import EvolutionFunctionLibList

from evolutionary_algorithms.evolve_list.evolve_list_server \
import EvolveListServer

class StringEvolutionServer():

    def __init__(self, config_path, target_file_path):
        conf = self.read_config_file(config_path)
        self.target_string = self.read_target(target_file_path)[0].rstrip()

        self.targets = self.block_target(conf, self.target_string)
        evolution_specs = conf.get("evolution_specs")
        self.population_size = evolution_specs.get("population_size")
        self.mutation_rate = evolution_specs.get("mutation_rate")
        self.num_of_generations = evolution_specs.get("num_of_generations")
        self.num_parents = evolution_specs.get("num_parents")
        self.elitism = evolution_specs.get("elitism")
        self.mating_pool_mutiplier = evolution_specs.get("mating_pool_mutiplier")

    def read_config_file(self, file_path):
        # Read Config File
        conf = ConfigFactory.parse_file(file_path)
        return conf

    def read_target(self, target_path):
        with open (target_path, "r") as target_string:
            target = target_string.readlines()
        return target

    def block_target(self, conf, target):
        target_specs = conf.get("target_specs")
        paralellize = target_specs.get("paralellize")

        max_string_length = target_specs.get("max_string_length")
        bits_of_strings = []

        if paralellize:
            length_of_string = len(target)
            number_of_bits = int(length_of_string / max_string_length)
            start_idx = 0
            for bit in range(number_of_bits+1):
                end_idx = start_idx + max_string_length
                if end_idx > length_of_string:
                    end_idx = length_of_string

                bit = target[start_idx:end_idx]
                bits_of_strings.append(bit)
                start_idx = end_idx
        else:
            bits_of_strings = target

        return bits_of_strings

    def evolve_string(self, target):
        # Setup Evolution
        efl = EvolutionFunctionLibList()
        kwargs = {"fitness_function_not": efl.fitness_function_words}

        evserver = EvolveListServer(self.population_size, self.mutation_rate,
                                self.num_of_generations,
                                target, self.num_parents, **kwargs)

        best_candidate = evserver.serve(target, self.num_of_generations, self.population_size,
                        evserver.gene_length,
                        evserver.population_obj, evserver.num_parents,
                        evserver.mutation_rate, self.mating_pool_mutiplier, self.elitism)


        return best_candidate

if __name__ == "__main__":
    # Use command :
    # python -m domains.string_evolution.string_evolution_server

    # Setup Parser
    PARSER = argparse.ArgumentParser(description='Evolve a String')
    # The model name should not have .json
    PARSER.add_argument("config_file_location", help="Location of Config file")
    PARSER.add_argument("target_file", help="Location of Target Text file")
    ARGS = PARSER.parse_args()

    # Initialize the Server
    evolution_server = StringEvolutionServer(ARGS.config_file_location,
                                            ARGS.target_file)
    print("\n ########## Stating Evolvution for ", evolution_server.num_of_generations, " generations.....")
    print("\n Evolution target: ", evolution_server.target_string)

    # Start Multicore Processing
    pool = Pool()
    evolved_chunks = pool.map(evolution_server.evolve_string, evolution_server.targets)
    pool.close()

    # Recombine the Chunks
    for iter, evolved_chunk in enumerate(evolved_chunks):
        evolved_chunks[iter] = "".join(evolved_chunk)

    evolved_candidate = "".join(evolved_chunks)
    print("Final Evolved Canidate:", evolved_candidate)
