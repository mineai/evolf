class CheckPoints:
    population_at_cp = None

    @classmethod
    def save_population(cls, treeset):
        cls.population_at_cp = treeset
