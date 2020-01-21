
from framework.serialize.population.population_serializer import PopulationSerializer
from servicecommon.persistor.local.text.json import TextJsonPersistor


class PopulationCheckpoint:

    def __init__(self, population_obj=None, search_space_obj=None, folder=".", filename="population_checkpoint"):
        self.population_obj = population_obj
        self.search_space_obj = search_space_obj
        self.folder = folder
        self.filename = filename

    def create_checkpoint(self, object=None, folder=None, filename=None):
        object = self.population_obj if object is None else object
        folder = self.folder if folder is None else folder
        filename = self.filename if filename is None else filename

        population_serializer = PopulationSerializer(object, self.search_space_obj)
        serialized_population = population_serializer.serialize()

        checkpoint_persistor = TextJsonPersistor(serialized_population, folder, filename)
        checkpoint_persistor.persist()

    def restore_checkpoint(self, folder=None, filename=None):
        folder = self.folder if folder is None else folder
        filename = self.filename if filename is None else filename

        checkpoint_restorer = TextJsonPersistor(None, folder, filename)
        deserialized_population = checkpoint_restorer.restore()

        population_deserializer = PopulationSerializer(deserialized_population, self.search_space_obj)
        checkpoint_population_object = population_deserializer.deserialize()

        return checkpoint_population_object
