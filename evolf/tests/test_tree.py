import random
import os

from evolf.elements.tree.tree import Tree
from evolf.populate.population import Population
from evolf.utils.visualize import Visualize

population = Population(3, 3, 10)

Visualize.visualize(population.working_trees)
