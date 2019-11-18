from evolf.framework.domain.get_default_config import GetDefaultConfig
from evolf.population.population \
    import Population
from evolf.reproduction.crossover import Crossover
from evolf.search_space.populate_search_space import PopulateSearchSpace
from evolf.search_space.search_space import SearchSpace
from evolf.servicecommon.utils.visualize import Visualize


search_space_obj = SearchSpace()
search_space = GetDefaultConfig.get_default_config().get("domain_config").get("search_space")
PopulateSearchSpace.populate_search_space(search_space_obj, search_space)
pop1 = Population(5, 5, 5, search_space_obj=search_space_obj)
tree1 = pop1.working_trees[0]
tree2 = pop1.working_trees[1]

tree_list = []

for tree in pop1.working_trees:
    tree_list.append(tree)

# new_tree1, new_tree2 = Crossover().crossover(tree1, tree2)
new_tree3 = Crossover.crossover_n_trees(tree_list)

tree_list.append(new_tree3)
# new_tree1.reset_tree()
# new_tree2.reset_tree()
Visualize.visualize(tree_list)
