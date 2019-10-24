import math

import numpy as np
from tqdm import trange

from evolutionary_algorithms.experimenthost.glo.fitnesseval.nn_fitness_evaluator import NNFitnessEvaluator
from evolutionary_algorithms.experimenthost.glo.populate.population import Population
from evolutionary_algorithms.experimenthost.glo.reproduction.crossover import Crossover
from evolutionary_algorithms.experimenthost.glo.reproduction.mutation import Mutation
from evolutionary_algorithms.experimenthost.glo.utils.tree_utils import TreeUtils


class SessionServer:

    def __init__(self, config, data_dict):
        # # Parse and initialize variables
        self.config = config
        self.evolution_specs = self.config.get("evolution_specs")
        self.visualization_specs = self.config.get("visualization_specs")
        self.domain_config = self.config.get("domain_config")
        self.evaluator_specs = self.domain_config.get("evaluator_specs")

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

        self.data_dict = data_dict

    def evaluate_current_generation(self, population):
        print("############# Starting Evaluation ################## \n\n")
        for tree_idx in trange(len(population.working_trees)):
            tree = population.working_trees[tree_idx]
            print(f" \n\n \t\t {tree.generate_printable_expression()} \n")
            fitness_evaluator = NNFitnessEvaluator(tree, self.evaluator_specs, self.data_dict)

            if tree.working:
                fitness_evaluator.train()
                fitness_evaluator.evaluate()

                tree.fitness = fitness_evaluator.score[1]
                print("Tree Fitness", tree.fitness)

                tree.avg_epoch_time = np.mean(fitness_evaluator.times)
                print("Average Epoch Time: ", tree.avg_epoch_time, "\n\n ###########################################################################")

                population.trainable_trees.append(tree)

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

    def evolve(self):

        population = Population(self.tree_min_height,
                                self.tree_max_height,
                                self.population_size,
                                self.number_parents,
                                self.mating_pool_multiplier)

        for gen in range(self.num_of_generations):
            print(f"Starting Evolution for Generation {gen}")

            population = self.evaluate_current_generation(population)
            best_candidate = population.get_best_fitness_candidate()
            print(f"\nBest Candidate for Generation {gen}: {best_candidate.symbolic_expression} \n \
             Fitness: {best_candidate.fitness} \n \
             Average Epoch Time: {best_candidate.avg_epoch_time}")
            print(f"\n\n Population Average Fitness: {np.mean(population.trainable_trees_fitness)}")
            print("\n #################################################################### ")

            population = self.initialize_next_gen(population)


