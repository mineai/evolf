from evolf.populate.population \
    import Population
from evolf.reproduction.crossover import Crossover
from evolf.utils.visualize import Visualize


pop = Population(2, 3, 100)
tree1 = pop.working_trees[0]
tree2 = pop.working_trees[1]

new_tree1, new_tree2 = Crossover().crossover(tree1, tree2)
new_tree1.reset_tree()
new_tree2.reset_tree()
Visualize.visualize([tree1, tree2, new_tree1, new_tree2])