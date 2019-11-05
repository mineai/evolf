from evolf.search_space.search_space import SearchSpace
from evolf.populate.population import Population
from evolf.reproduction.mutation import Mutation
from evolf.servicecommon.utils.visualize \
    import Visualize


class MutationTest:
    @staticmethod
    def run():
        import copy
        search_space_obj = SearchSpace()
        population = Population(3, 3, 1, search_space_obj=search_space_obj)
        # population.generate_population()
        # population.get_working_trees()

        print("number of nodes: ", population.trees[0].number_of_nodes)
        tree_to_mutate = copy.deepcopy(population.trees[0])
        child_function_mutation = Mutation.weighted_function_mutation(tree_to_mutate, 1, search_space_obj)
        # child_function_mutation.reset_tree()
        # tree_copy = copy.deepcopy(child_function_mutation)
        child_literal_mutation = Mutation.mutate_value_literal_nodes(child_function_mutation, 1)
        # child_literal_mutation.reset_tree()
        # tree_copy = copy.deepcopy(child_literal_mutation)
        child_leaf_mutation = Mutation.mutate_leaf_node(child_literal_mutation, 1, search_space_obj)
        # child_leaf_mutation.reset_tree()
        # tree_copy = copy.deepcopy(child_leaf_mutation)
        child_shrink_mutation = Mutation.shrink_mutation(child_leaf_mutation, 1, search_space_obj)
        # child_shrink_mutation.reset_tree()
        # tree_copy = copy.deepcopy(child_shrink_mutation)
        child_hoist_mutation = Mutation.hoist_mutation(child_shrink_mutation, 1)
        # child_hoist_mutation.reset_tree()
        trees_to_vis = []
        trees_to_vis.append(tree_to_mutate)
        trees_to_vis.append(child_function_mutation)
        trees_to_vis.append(child_literal_mutation)
        trees_to_vis.append(child_leaf_mutation)
        trees_to_vis.append(child_shrink_mutation)
        trees_to_vis.append(child_hoist_mutation)

        Visualize.visualize(trees_to_vis)


MutationTest().run()
