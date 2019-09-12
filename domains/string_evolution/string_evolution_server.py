import argparse
from pyhocon import ConfigFactory
import time
from tqdm import tqdm
from colorama import Fore
from multiprocessing import Process, current_process, Manager, Pool

from evolutionary_algorithms.evolve_list.evolution_functions_lib_list \
import EvolutionFunctionLibList

from evolutionary_algorithms.evolve_list.evolve_list_server \
import EvolveListServer

class StringEvolutionServer():

    def __init__(self, config_path, target_file_path):
        conf = self.read_config_file(config_path)
        self.target_string = self.read_target(target_file_path)
        self.target_string = "".join(self.target_string)
        # self.target_string = self.target_string.replace('\n', " ")

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

    def evolve_string(self, args):
        """
        param args: This contains (target, queue)
        """
        target, queue = args
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

        queue.put(target)

        return best_candidate

if __name__ == "__main__":
    # Use command :
    # python -m domains.string_evolution.string_evolution_server domains/string_evolution/config.hocon domains/string_evolution/target_wiki.txt

    # Setup Parser
    PARSER = argparse.ArgumentParser(description='Evolve a String')
    # The model name should not have .json
    PARSER.add_argument("config_file_location", help="Location of Config file")
    PARSER.add_argument("target_file", help="Location of Target Text file")
    ARGS = PARSER.parse_args()

    # Initialize the Server
    evolution_server = StringEvolutionServer(ARGS.config_file_location,
                                            ARGS.target_file)
    print("\n ########## Stating Evolution for ", evolution_server.num_of_generations,
                " generations.....")
    evolution_target = evolution_server.target_string
    target_dna_size = len(evolution_target)
    print("\n Evolution target: ", evolution_target)
    print("Target Size:", target_dna_size)



    start_time = time.time()

    # Start Multicore Processing
    pool = Pool()
    manager = Manager()
    queue = manager.Queue()

    # Generate args such that there is a queue for each target
    args = [(target, queue) for target in evolution_server.targets]
    # Asynchronously map the function and the args to the pool
    evolved_chunks = pool.map_async(evolution_server.evolve_string, args)
    # Close the pool
    pool.close()

    # Check On Progress
    TOTAL_TASKS = len(evolution_server.targets)
    jobs_left_last = evolved_chunks._number_left
    jobs_left_currently = jobs_left_last

    colors = Fore.__dict__

    pbar = tqdm(total=TOTAL_TASKS, desc="JOBS", initial=1)
    while not evolved_chunks.ready():
        jobs_left_currently = evolved_chunks._number_left
        jobs_finished_since_last = jobs_left_last - jobs_left_currently
        pbar.update(jobs_finished_since_last)
        if jobs_left_currently < jobs_left_last:
            jobs_left_last = jobs_left_currently


    pbar.close()

    # Once All jobs have finished, get the result
    evolved_chunks = evolved_chunks.get()

    # Tet the time taken for evolution
    elapsed_time = time.time() - start_time


    # Recombine the Chunks
    if isinstance(evolved_chunks[0], list):
        for chunk_idx, chunk in enumerate(evolved_chunks):
            evolved_chunks[chunk_idx] = "".join(chunk)

    evolved_candidate = "".join(evolved_chunks)

    print("Final Evolved Canidate:", evolved_candidate)
    print("Time Taken to evolve: ", elapsed_time/60, " mins" )
