from evolf.populate.search_space import SearchSpace
from evolf.populate.population import Population
from evolf.utils.visualize import Visualize

fl = SearchSpace()
population = Population(3, 3, 10, search_space_obj=fl)
Visualize.visualize(population.working_trees)
