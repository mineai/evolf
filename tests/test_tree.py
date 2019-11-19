from search_space.search_space import SearchSpace
from population.population import Population

fl = SearchSpace()
population = Population(3, 3, 10, search_space_obj=fl)

tree = population.working_trees[0]

print(f"{tree.binary_count}, {tree.unary_count}, {tree.literal_count}, {tree.height}")
print(tree.nodes[0].node_id)
print(tree.nodes[0].operator_type)
# print(f"{tree.nodes}")
tree.reset_tree()
# print(f"{tree.nodes}")
print(f"{tree.binary_count}, {tree.unary_count}, {tree.literal_count}, {tree.height}")
print(tree.nodes[0].node_id)
print(tree.nodes[0].operator_type)