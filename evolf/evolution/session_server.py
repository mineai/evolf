import math

import numpy as np
from tqdm import trange

from evolf.elements.tree.tree import Tree
from evolf.fitnesseval.nn_fitness_evaluator import NNFitnessEvaluator
from evolf.populate.population import Population
from evolf.reproduction.crossover import Crossover
from evolf.reproduction.mutation import Mutation
from evolf.utils.tree_utils import TreeUtils
from evolf.utils.evolution_persistor import EvolutionPersistor


class SessionServer:

    def __init__(self, config, data_dict):
        # # Parse and initialize variables
        self.config = config
        self.evolution_specs = self.config.get("evolution_specs")
        self.visualization_specs = self.config.get("visualization_specs")
        self.domain_config = self.config.get("domain_config")
        self.evaluator_specs = self.domain_config.get("evaluator_specs")
        self.persistence_specs = self.config.get("persistence_specs")
        self.state_of_the_art_config = self.domain_config.get("state_of_the_art_config")

        self.initial_population_size = self.evolution_specs.get("initial_population_size")
        self.population_size = self.evolution_specs.get("population_size")
        self.mating_pool_multiplier = self.evolution_specs.get("mating_pool_multiplier")
        self.number_parents = self.evolution_specs.get("num_parents")
        self.weighted_function_mutation_rate = self.evolution_specs.get("weighted_function_mutation_rate")
        self.mutate_value_literal_nodes_rate = self.evolution_specs.get("mutate_value_literal_nodes_rate")
        self.mutate_leaf_node_rate = self.evolution_specs.get("mutate_leaf_node_rate")
        self.elitism = self.evolution_specs.get("elitism")
        self.num_of_generations = self.evolution_specs.get("num_of_generations")
        self.tree_min_height = self.evolution_specs.get("tree_min_height")
        self.tree_max_height = self.evolution_specs.get("tree_max_height")
        self.output_path = self.persistence_specs.get("output_path")
        self.state_of_the_art_loss = self.state_of_the_art_config.get("loss")
        self.evaluate_state_of_the_art_flag = self.state_of_the_art_config.get("evaluate")

        self.data_dict = data_dict

        self.state_of_the_art_testing_accuracy = None
        self.state_of_the_art_epoch_time = None

        self.persistor_obj = EvolutionPersistor(self.output_path)
        self.generation_number = 0
        self.current_tree = 1

    def evaluate_candidate(self, population, tree_idx):
        tree = population.working_trees[tree_idx]
        print(f" \n\n \t\t Loss Function: {tree.generate_printable_expression()} \n")

        if len(population.trainable_trees_fitness):
            print("Best Running in this Generation: ", np.max(population.trainable_trees_fitness))

        if tree_idx > self.population_size:
            # If it is an Elite, no need to train Again
            population.trainable_trees.append(tree)
            return

        print(f"State of the art Performance {self.state_of_the_art_testing_accuracy}")
        fitness_evaluator = NNFitnessEvaluator(tree, self.evaluator_specs, self.data_dict)

        if tree.working:
            fitness_evaluator.train()
            fitness_evaluator.evaluate()

            tree.fitness = fitness_evaluator.score[1]
            print("Tree Fitness", tree.fitness)

            tree.avg_epoch_time = np.mean(fitness_evaluator.times)
            print("Average Epoch Time: ", tree.avg_epoch_time,
                  "\n\n ###########################################################################")

            # Create tree_<index>_fitness folder at output_path
            self.persistor_obj.create_tree_folder(self.current_tree, tree, self.generation_number, tree.fitness)

            self.current_tree += 1
            # pickle the tree
            # put tree stats in a json file

            population.trainable_trees.append(tree)
            population.trainable_trees_fitness.append(tree.fitness)
        else:
            print("This tree failed while training",
                  "\n\n ###########################################################################")

        return population

    def evaluate_current_generation(self, population):
        print("############# Starting Evaluation ################## \n\n")
        self.persistor_obj.create_generation_folder(self.generation_number)

        for tree_idx in trange(len(population.working_trees)):
            self.evaluate_candidate(population, tree_idx)

        population.initialize_trainable_tree_fitness()
        return population

    def initialize_next_gen(self, population):
        next_gen_trees = []
        number_of_elites = math.ceil(len(population.trainable_trees) * self.elitism)
        sorted_parents = TreeUtils.sort_trees_by_fitness_desc(population.trainable_trees)
        elites = sorted_parents[:number_of_elites]
        print("############# Starting Reproduction ################## \n")
        population.generate_mating_pool()

        current_population = 0
        child_expressions = []
        while current_population < self.population_size:
            parents = population.natural_selection()
            parents = TreeUtils.sort_trees_by_fitness_desc(parents)
            child = Crossover.crossover(parents[0], parents[1])
            child = Mutation.weighted_function_mutation(child, self.weighted_function_mutation_rate)
            child = Mutation.mutate_leaf_node(child, self.mutate_leaf_node_rate)
            child = Mutation.mutate_value_literal_nodes(child, self.mutate_value_literal_nodes_rate)
            try:
                child.reset_tree()
            except:
                continue

            if not child.working:
                continue

            if child.symbolic_expression in child_expressions:
                continue

            next_gen_trees.append(child)
            child_expressions.append(child.symbolic_expression)
            current_population += 1
            print(f"Child {current_population} after reproduction Expression: {child.symbolic_expression}")

        next_gen_trees.extend(elites)
        print("\nElites from Previous Generation: ")
        [print(elite.generate_printable_expression()) for elite in elites]

        print("############# Initializing new Generation ################## \n\n\n\n")
        population = Population(None,
                                None,
                                self.population_size,
                                self.number_parents,
                                self.mating_pool_multiplier,
                                initial_population=next_gen_trees)
        population.get_working_trees()
        return population

    def evaluate_state_of_the_art(self):
        print("State of the Art Model: ")
        fitness_evaluator = NNFitnessEvaluator(None, self.state_of_the_art_config, self.data_dict)
        print(fitness_evaluator.model.summary())
        fitness_evaluator.train()
        fitness_evaluator.evaluate()

        self.state_of_the_art_testing_accuracy = fitness_evaluator.score[1]
        self.state_of_the_art_epoch_time = fitness_evaluator.times
        print("Testing Accuracy: ", self.state_of_the_art_testing_accuracy)
        avg_epoch_time = np.mean(self.state_of_the_art_epoch_time)
        print("Average Epoch Time: ", avg_epoch_time,
              "\n\n ###########################################################################")

    def evolve(self):
        import tensorflow as tf
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

        if self.evaluate_state_of_the_art_flag:
            print("###################### Evaluating State of the Art\n\n")
            self.evaluate_state_of_the_art()
            print("\n\n ###########################################################################")

        population = Population(self.tree_min_height,
                                self.tree_max_height,
                                self.initial_population_size,
                                self.number_parents,
                                self.mating_pool_multiplier)

        while not len(population.working_trees):
            population = Population(self.tree_min_height,
                                    self.tree_max_height,
                                    self.initial_population_size,
                                    self.number_parents,
                                    self.mating_pool_multiplier)

        for gen in range(self.num_of_generations):
            print(f"Starting Evolution for Generation {gen}")

            print("Evaluator NN: ")
            dummy_tree = Tree(2, 2)
            fitness_evaluator = NNFitnessEvaluator(dummy_tree, self.evaluator_specs, self.data_dict)
            print(fitness_evaluator.model.summary())
            del fitness_evaluator, dummy_tree

            population = self.evaluate_current_generation(population)
            try:
                best_candidate = population.get_best_fitness_candidate()
            except:
                best_candidate = False
            if best_candidate:
                print(f"\nBest Candidate for Generation {gen}: {best_candidate.symbolic_expression} \n \
                 Fitness: {best_candidate.fitness} \n \
                 Average Epoch Time: {best_candidate.avg_epoch_time}")
                print(f"\n\n Population Average Fitness: {np.mean(population.trainable_trees_fitness)}")
                print("\n #################################################################### ")

                self.persistor_obj.persist_best_candidate(best_candidate, self.generation_number)
            population = self.initialize_next_gen(population)

            self.generation_number += 1
