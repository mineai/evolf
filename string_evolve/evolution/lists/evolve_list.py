# Import Libs
from string_evolve.evolution.lists.candidate_list \
            import CandidateList
from string_evolve.elements.population.population \
            import Population
from string_evolve.evaluation.fitness.fitness_objectives \
            import FitnessObjectives
from string_evolve.reproduction.selection.selection import Selection
from string_evolve.reproduction.selection.mating_pool \
            import MatingPool
from string_evolve.reproduction.crossover.crossover \
            import Crossover
from string_evolve.reproduction.mutation.mutation \
            import Mutation

from string_evolve.evaluation.fitness.fitness_library \
            import FitnessLibrary
from string_evolve.servicecommon.utils.list_utils \
            import ListUtils

from string_evolve.servicecommon.persistor.local.json.json_persistor \
            import JsonPersistor

import math
from tqdm import trange
from multiprocessing import Process, current_process, Manager, Pool
import os
import time
import calendar

class EvolveList():
    def __init__(self, target,
                        initial_population=None,
                        population_size=10,
                        num_of_generations=10000,
                        elitism=0.1,
                        neucleotide_generator_function_and_args=None,
                        fitness_functions=None,
                        mating_pool_function_and_args=None,
                        selection_function_and_args=None,
                        crossover_function_and_args=None, mutation_function_and_args=None,
                        fitness_recombination_method=None,
                        domain="experiment"):


        self.initial_population = initial_population
        self.population_size = population_size
        self.num_of_generations = num_of_generations
        self.target = target
        self.elitism = elitism
        self.best_candidate = None

        self.candidate_length = len(self.target)
        self.neucleotide_generator_function = neucleotide_generator_function_and_args[0]
        self.neucleotide_generator_function_args = neucleotide_generator_function_and_args[1]
        self.fitness_functions = fitness_functions
        self.mating_pool_function = mating_pool_function_and_args[0]
        self.mating_pool_function_args = mating_pool_function_and_args[1]
        self.selection_function = selection_function_and_args[0]
        self.selection_function_args = selection_function_and_args[1]
        self.crossover_function = crossover_function_and_args[0]
        self.crossover_function_and_args = crossover_function_and_args[1]
        self.mutation_function = mutation_function_and_args[0]
        self.mutation_function_and_args = mutation_function_and_args[1]
        self.fitness_recombination_method = fitness_recombination_method


        self.experiment_id = calendar.timegm(time.gmtime())
        self.file_directory = f"{os.getcwd()}/results/{domain}_{self.experiment_id}"
        os.makedirs(self.file_directory)

        print("Refer to this Experiment:", f"{domain}_{self.experiment_id}")



    def initialize_functions(self, neucleotide_generator_function_and_args=None,
                            fitness_functions_and_args=None,
                            mating_pool_function_and_args=None,
                            selection_function_and_args=None,
                            crossover_function_and_args=None,
                            mutation_function_and_args=None,
                            fitness_recombination_method=None):
        self.neucleotide_generator_function,
        self.neucleotide_generator_function_args = neucleotide_generator_function_and_args
        self.fitness_functions = fitness_functions
        self.mating_pool_function, self.mating_pool_function_args = mating_pool_function_and_args
        self.selection_function, self.selection_function_args = selection_function_and_args
        self.crossover_function, self.crossover_function_and_args = crossover_function_and_args
        self.mutation_function, self.mutation_function_and_args = mutation_function_and_args
        self.fitness_recombination_method = fitness_recombination_method

    def evolve(self, target):

        # Generate A candidate Object
        candidate_list_obj = CandidateList(self.candidate_length, self.neucleotide_generator_function)
        # Create a Population
        if not self.initial_population:
            p = Population(self.population_size, candidate_list_obj)
            p.generate_population()
            population = p.get_population_decoded()
        else:
            population = self.initial_population

        best_fitness_candidate_extractor = FitnessLibrary.get_best_fitness_candidate

        elites = []
        elites_to_keep = math.floor(self.population_size * self.elitism)



        # For all the generations
        for generation in trange(self.num_of_generations):

            # Retain elites
            population[:elites_to_keep] = elites

            # Evaluate Fintess objectives
            fitness_objectives_object = FitnessObjectives(self.fitness_functions,
                                    [population, target])
            fitness_from_objectives = fitness_objectives_object.execute_all_fitness( \
                                        self.fitness_functions,
                                        [population, target])

            fitness = fitness_objectives_object.get_recombined_fitness(self.fitness_recombination_method)

            best_candidate_info = best_fitness_candidate_extractor(population, fitness)

            # Print Stats
            print("Genration ", generation)

            best_candidate = best_candidate_info[list(best_candidate_info)[0]]
            best_candidate_fitness = list(best_candidate_info)[0]
            print("Best Candidate: ", "".join(best_candidate))
            self.best_candidate = best_candidate
            # Persist Population
            population_dict = {}
            gen_folder = self.file_directory + f"/gen{generation}"
            os.makedirs(gen_folder)
            json_persistor_obj = JsonPersistor("popuation", gen_folder)
            for candidate, candidate_fitness in zip(population, fitness):
                candidate_info = self.generate_dict_obj(candidate,
                                                    candidate_fitness)
                population_dict.update(candidate_info)
            json_persistor_obj.persist(population_dict)

            # Persist Best Candidate
            best_candidate_dict = self.generate_dict_obj(best_candidate,
                                                best_candidate_fitness)
            json_persistor_obj.base_file_name = "best_candidate"
            json_persistor_obj.persist(best_candidate_dict)



            # Sort the values in descending order
            population_desc = ListUtils().sort_lists(population, fitness)
            elites = population_desc[:elites_to_keep]

            # Generate Mating Pool
            mating_pool_obj = MatingPool(self.mating_pool_function, self.mating_pool_function_args)
            mating_pool = mating_pool_obj.generate_mating_pool(population,
                                                            fitness)

            children = []
            # Select Parents
            for parent_idx in range(self.population_size):
                selection = Selection(mating_pool, self.selection_function,
                                                self.selection_function_args)
                parents = selection.select_parents()
                crossover_obj = Crossover(parents,
                                            self.crossover_function,
                                            self.crossover_function_and_args)


                child = crossover_obj.crossover()
                mutation = Mutation(child, self.mutation_function,
                                    self.mutation_function_and_args)
                mutated_child = mutation.mutate()
                children.append(child)

            population = children

            if target == best_candidate:
                break

        return best_candidate

    def evolve_parallel_using_single(self, args):
        target, queue = args
        best_candidate = self.evolve(target)
        queue.put(target)

        return best_candidate

    def generate_dict_obj(self, candidate, fitness):
        dict = {
            str(candidate): fitness
        }
        return dict

    def evolve_parallel(self, max_chunk_size):
        start_time = time.time()
        target_chunks = ListUtils().block_list(self.target, max_chunk_size)
        print(target_chunks)

        # Start Multicore Processing
        pool = Pool()
        manager = Manager()
        queue = manager.Queue()

        # Generate args such that there is a queue for each target
        args = [(target, queue) for target in target_chunks]

        # Asynchronously map the function and the args to the pool
        evolved_chunks = pool.map_async(self.evolve_parallel_using_single, args)
        # Close the pool
        pool.close()

        while not evolved_chunks.ready():
            pass

        # Once All jobs have finished, get the result
        evolved_chunks = evolved_chunks.get()

        # Tet the time taken for evolution
        elapsed_time = time.time() - start_time

        #Recombine the Chunks
        if isinstance(evolved_chunks[0], list):
            for chunk_idx, chunk in enumerate(evolved_chunks):
                evolved_chunks[chunk_idx] = "".join(chunk)

        evolved_candidate = "".join(evolved_chunks)

        print("Final Evolved Canidate:", evolved_candidate)
        print("Time Taken to evolve: ", elapsed_time/60, " mins" )

        print("Refer to this Experiment:", f"{domain}_{self.experiment_id}")
