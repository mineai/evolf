import math

from evolf.servicecommon.utils.tree_utils import TreeUtils
from evolf.populate.population import Population
from evolf.reproduction.crossover import Crossover
from evolf.reproduction.mutation import Mutation


class InitializeNextGen:

    def __init__(self, evolution_specs):
        self.evolution_specs = evolution_specs
        self.weighted_function_mutation_rate = self.evolution_specs.get("weighted_function_mutation_rate")
        self.mutate_value_literal_nodes_rate = self.evolution_specs.get("mutate_value_literal_nodes_rate")
        self.mutate_leaf_node_rate = self.evolution_specs.get("mutate_leaf_node_rate")
        self.shrink_mutation_rate = self.evolution_specs.get("shrink_mutation_rate")
        self.hoist_mutation_rate = self.evolution_specs.get("hoist_mutation_rate")
        self.literal_swap_mutation_rate = self.evolution_specs.get("literal_swap_mutation_rate")
        self.elitism = self.evolution_specs.get("elitism")

    def initialize_next_gen(self, population):
        next_gen_trees = []
        sorted_parents = TreeUtils.sort_trees_by_fitness_desc(population.trees)

        number_of_elites = math.ceil(len(population.trees) * self.elitism)
        elites = sorted_parents[:number_of_elites]

        population.generate_mating_pool()

        current_population = 0
        child_expressions = []
        while current_population < self.population_size:
            parents = population.natural_selection()
            parents = TreeUtils.sort_trees_by_fitness_desc(parents)
            children = Crossover.crossover(parents[0], parents[1])

            for child in children:
                child = Mutation.weighted_function_mutation(child, self.weighted_function_mutation_rate,
                                                            self.search_space_obj)
                child = Mutation.mutate_leaf_node(child, self.mutate_leaf_node_rate, self.search_space_obj)
                child = Mutation.mutate_value_literal_nodes(child, self.mutate_value_literal_nodes_rate)
                child = Mutation.shrink_mutation(child, self.shrink_mutation_rate, self.search_space_obj)
                child = Mutation.hoist_mutation(child, self.hoist_mutation_rate)

                if not child.working:
                    continue

                if child.symbolic_expression in child_expressions:
                    continue

                next_gen_trees.append(child)
                child_expressions.append(child.symbolic_expression)
                current_population += 1
                print(f"Child {current_population}: {child.symbolic_expression}")

        next_gen_trees.extend(elites)
        print("\nElites from Previous Generation: ")
        [print(elite.generate_printable_expression()) for elite in elites]

        population = Population(None,
                                None,
                                self.population_size,
                                self.number_parents,
                                self.mating_pool_multiplier,
                                initial_population=next_gen_trees,
                                search_space_obj=self.search_space_obj)
        return population
