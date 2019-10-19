from evolutionary_algorithms.experimenthost.glo.populate.population \
    import Population
from evolutionary_algorithms.experimenthost.glo.reproduction.crossover import Crossover
from evolutionary_algorithms.experimenthost.glo.utils.visualize import Visualize


pop = Population(2, 3, 100)
pop.generate_population()
tree1 = pop.working_trees[0]
tree2 = pop.working_trees[1]

new_tree = Crossover().crossover(tree1, tree2)
while not new_tree.working:
    new_tree = Crossover().crossover(tree1, tree2)
Visualize.visualize([tree1, tree2, new_tree])
print('New Tree Height: ', new_tree.height)