from evolf.populate.population import Population
from evolf.reproduction.mutation import Mutation
from evolf.utils.visualize \
    import Visualize


class MutationTest:
    @staticmethod
    def run():
        population = Population(3, 3, 1)
        population.generate_population()
        population.get_working_trees()

        print("number of nodes: ", population.trees[0].number_of_nodes)

        child_function_mutation = Mutation.weighted_function_mutation(population.trees[0], 0.75)
        child_literal_mutation = Mutation.mutate_value_literal_nodes(child_function_mutation, 0.5)
        child_leaf_mutation = Mutation.mutate_leaf_node(child_literal_mutation, 0.5)
        trees_to_vis = []
        trees_to_vis.extend(population.trees)
        trees_to_vis.append(child_function_mutation)
        trees_to_vis.append(child_literal_mutation)
        trees_to_vis.append(child_leaf_mutation)

        Visualize.visualize(trees_to_vis)


MutationTest().run()
