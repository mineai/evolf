import random
import numpy as np

from evolutionary_algorithms.evolve_list.dna_list import DNAList
from evolutionary_algorithms.evolve_list.evolution_list_utils import EvolutionListUtils
from evolutionary_algorithms.population import Population


class PopulationList(Population):

    def __init__(self, pop_size, mutation_rate, target, **kwargs):
        super().__init__(pop_size, mutation_rate, target, **kwargs)
        self.dna = DNAList(self.dna_dimensions, self.mutation_rate,
                    **self.external_functions)

        self.utils = EvolutionListUtils()
