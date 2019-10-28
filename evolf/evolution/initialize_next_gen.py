import math

from evolf.utils.tree_utils import TreeUtils
from evolf.populate.population import Population
from evolf.reproduction.crossover import Crossover
from evolf.reproduction.mutation import Mutation


class InitializeNextGen:

    def initialize_next_gen(self, population):
        next_gen_trees = []
        sorted_parents = TreeUtils.sort_trees_by_fitness_desc(population.trainable_trees)

        number_of_elites = math.ceil(len(population.trainable_trees) * self.elitism)
        elites = sorted_parents[:number_of_elites]

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

        population = Population(None,
                                None,
                                self.population_size,
                                self.number_parents,
                                self.mating_pool_multiplier,
                                initial_population=next_gen_trees)
        population.get_working_trees()
        return population
