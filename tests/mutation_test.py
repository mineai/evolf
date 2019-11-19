from framework.domain.get_default_config import GetDefaultConfig
from search_space.populate_search_space import PopulateSearchSpace
from search_space.search_space import SearchSpace
from population.population import Population
from reproduction.mutation import Mutation
from servicecommon.utils.visualize \
    import Visualize

class MutationTest:
    @staticmethod
    def run():
        import copy
        search_space_obj = SearchSpace()

        search_space = GetDefaultConfig.get_default_config().get("domain_config").get("search_space")

        PopulateSearchSpace.populate_search_space(search_space_obj, search_space)
        population = Population(5, 5, 1, search_space_obj=search_space_obj)

        tree_to_mutate = copy.deepcopy(population.trees[0])
        child_function_mutation = Mutation.weighted_function_mutation(tree_to_mutate, 1, search_space_obj)
        child_literal_mutation = Mutation.mutate_value_literal_nodes(child_function_mutation, 1)
        child_leaf_mutation = Mutation.mutate_leaf_node(child_literal_mutation, 1, search_space_obj)
        child_shrink_mutation = Mutation.shrink_mutation(child_leaf_mutation, 1, search_space_obj)
        child_hoist_mutation = Mutation.hoist_mutation(child_shrink_mutation, 1)
        child_literal_swap_mutation = Mutation.literal_swap_mutation(child_hoist_mutation, 1, search_space_obj)

        trees_to_vis = []
        trees_to_vis.append(tree_to_mutate)
        trees_to_vis.append(child_function_mutation)
        trees_to_vis.append(child_literal_mutation)
        trees_to_vis.append(child_leaf_mutation)
        trees_to_vis.append(child_shrink_mutation)
        trees_to_vis.append(child_hoist_mutation)
        trees_to_vis.append(child_literal_swap_mutation)

        Visualize.visualize(trees_to_vis)


MutationTest().run()
