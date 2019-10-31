from evolf.populate.function_library import FunctionLibrary
from evolf.populate.population import Population
from evolf.utils.visualize import Visualize

fl = FunctionLibrary()
population = Population(3, 3, 10, search_space_obj=fl)
Visualize.visualize(population.working_trees)
