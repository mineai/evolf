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

    def evolve(self):

        population = Population(self.tree_min_height,
                                self.tree_max_height,
                                self.population_size,
                                self.number_parents,
                                self.mating_pool_multiplier)

        for gen in range(self.num_of_generations):
            next_gen_trees = []
            print(f"Starting Evolution for Generation {gen}")
            print("############# Starting Evaluation ################## \n\n")
            for tree_idx in range(len(population.working_trees)):
                tree = population.working_trees[tree_idx]
                print(f" \n\n Expression = {tree.symbolic_expression} \n")
                fitness_evaluator = NNFitnessEvaluator(tree, self.evaluator_specs, self.data_dict)

                if tree.working:
                    fitness_evaluator.train()
                    fitness_evaluator.evaluate()

                    tree.fitness = fitness_evaluator.score[1]
                    print("Tree Fitness", tree.fitness)

                    tree.avg_epoch_time = np.mean(fitness_evaluator.times)
                    print("Average Epoch Time: ", tree.avg_epoch_time)

                    population.trainable_trees.append(tree)
                else:
                    print(" \n ########### NOTE: This Tree Failed ... \n")

            best_candidate = population.get_best_fitness_candidate()
            print(f"Best Candidate for Generation {gen}: {best_candidate.symbolic_expression} \n \
             Fitness: {best_candidate.fitness} \n \
             Average Epoch Time: {best_candidate.avg_epoch_time}")
            print("\n #################################################################### \
                                ################################################################")

            print("############# Starting Reproduction ################## \n")
            population.generate_mating_pool()
            for child_num in range(len(self.population_size)):
                parents = population.natural_selection()
                parents = TreeUtils.sort_trees_by_fitness_desc(parents)
                child = Crossover.crossover(parents[0], parents[1])
                child = Mutation.weighted_function_mutation(child, self.weighted_function_mutation_rate)
                child = Mutation.mutate_leaf_node(child, self.mutate_leaf_node_rate)
                child = Mutation.mutate_value_literal_nodes(child, self.mutate_value_literal_nodes_rate)
                child.reset_tree()

                next_gen_trees.append(child)

                print(f"Child {child_num} after reproduction Expression: {child.symbolic_expression}")

            print("############# Initializing new Generation ################## \n\n\n\n")
            population = Population(None,
                                    None,
                                    self.population_size,
                                    self.number_parents,
                                    self.mating_pool_multiplier,
                                    initial_population=next_gen_trees)





