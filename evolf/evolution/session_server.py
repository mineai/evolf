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
        self.persist_status = self.persistence_specs.get("persist")
        self.visualize_tree_status = self.visualization_specs.get("visualize_tree")
        self.visualize_function_status = self.visualization_specs.get("visualize_function")
        self.visualize_avg_fitness = self.visualization_specs.get("visualize_avg_fitness")
        self.visualize_best_fitness = self.visualization_specs.get("visualize_best_fitness")
        self.state_of_the_art_loss = self.state_of_the_art_config.get("loss")
        self.evaluate_state_of_the_art_flag = self.state_of_the_art_config.get("evaluate")

        self.data_dict = data_dict

        self.state_of_the_art_testing_accuracy = None
        self.state_of_the_art_epoch_time = None

        self.persistor_obj = EvolutionPersistor(self.output_path)
        self.generation_number = 0
        self.current_tree = 1

        self.avg_fitness_list = []
        self.best_fitness_list = []

    def evaluate_candidate(self, population, tree_idx, eval_all=False):
        tree = population.working_trees[tree_idx]
        print(f" \n\n \t\t Loss Function: {tree.generate_printable_expression()} \n")

        if len(population.trainable_trees_fitness):
            print("Best Running in this Generation: ", np.max(population.trainable_trees_fitness))

        if not eval_all:
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
            self.persistor_obj.create_tree_folder(self.current_tree, tree, self.generation_number, tree.fitness, self.persist_status, self.visualize_tree_status, self.visualize_function_status)


            self.current_tree += 1
            # pickle the tree
            # put tree stats in a json file

            population.trainable_trees.append(tree)
            population.trainable_trees_fitness.append(tree.fitness)
        else:
            print("This tree failed while training",
                  "\n\n ###########################################################################")

        return population

    def evaluate_current_generation(self, population, eval_all=False):
        print("############# Starting Evaluation ################## \n\n")
        self.persistor_obj.create_generation_folder(self.generation_number)
        population.get_working_trees()
        for tree_idx in trange(len(population.working_trees)):
            self.evaluate_candidate(population, tree_idx, eval_all)

        population.initialize_trainable_tree_fitness()
        return population

    def initialize_next_gen(self, population):
        next_gen_trees = []
        sorted_parents = TreeUtils.sort_trees_by_fitness_desc(population.trainable_trees)

        number_of_elites = math.ceil(len(population.trainable_trees) * self.elitism)
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

            child.reset_tree()

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

    def get_best_candidate(self, population, gen):
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

            # Update the lists of average fitness and best fitness for each generation
            self.avg_fitness_list.append(np.mean(population.trainable_trees_fitness))
            self.best_fitness_list.append(best_candidate.fitness)

            self.persistor_obj.persist_best_candidate(best_candidate, self.generation_number, self.persist_status, self.visualize_tree_status, self.visualize_function_status)
            if self.visualize_avg_fitness:
                plot_file_name = "Average_Fitness_Plot.png"
                plot_title = f"Average Fitness Over {self.generation_number+1} Generations"
                x_label = "Generations"
                y_label = "Average Fitness"
                self.persistor_obj.create_fitness_plot(self.avg_fitness_list, self.generation_number, self.num_of_generations, plot_file_name, plot_title, x_label, y_label)

            if self.visualize_best_fitness:
                plot_file_name = "Best_Fitness_Plot.png"
                plot_title = f"Best Fitness Over {self.generation_number+1} Generations"
                x_label = "Generations"
                y_label = "Best Fitness"
                self.persistor_obj.create_fitness_plot(self.best_fitness_list, self.generation_number, self.num_of_generations, plot_file_name, plot_title, x_label, y_label)

        return best_candidate

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

            if gen == 0:
                eval_all = True
            else:
                eval_all = False
            population = self.evaluate_current_generation(population, eval_all)

            self.get_best_candidate(population, gen)

            population = self.initialize_next_gen(population)

            self.generation_number += 1
            self.current_tree = 1
