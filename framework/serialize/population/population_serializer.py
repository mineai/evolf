
from framework.interfaces.serialize.serialize import Serialize
from framework.population.population import Population
from framework.serialize.tree.tree_serializer import TreeSerializer


class PopulationSerializer(Serialize):

    def __init__(self, population_obj=None, search_space_obj=None):
        self.population_obj = population_obj
        self.search_space_obj = search_space_obj

    def serialize(self):
        serialized_population = TreeSerializer(self.population_obj.trees,
                                          self.search_space_obj).serialize()
        return serialized_population


    def deserialize(self):
        deserialized_population = TreeSerializer(self.population_obj,
                                               self.search_space_obj).deserialize()
        population_object = Population(initial_population=deserialized_population,
                                       search_space_obj=self.search_space_obj)

        return population_object


