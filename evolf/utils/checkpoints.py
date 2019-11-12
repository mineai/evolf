class Checkpoint:
    SavedPopulation = ''

    @classmethod
    def checkpoint(cls, population):
        cls.SavedPopulation = population
