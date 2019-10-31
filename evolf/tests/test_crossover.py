from evolf.populate.population \
    import Population
from evolf.reproduction.crossover import Crossover
from evolf.utils.visualize import Visualize
import copy

pop = Population(5, 5, 3)
pop.generate_population()
pop.trees[0].fitness = 7
pop.trees[1].fitness = 2
pop.trees[2].fitness = 3
trees = copy.deepcopy(pop.trees)
trees.append(copy.deepcopy(Crossover.crossover_n_trees(trees)))
Visualize.visualize(trees)