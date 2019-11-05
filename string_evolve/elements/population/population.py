from string_evolve.elements.candidate.candidate \
    import Candidate

class Population():
    """
    This class acts as interface that can be inherited to generate the population.
    """

    def __init__(self, population_size, candidate_obj):
        """
        The constructor initializes the population
        size.
        :param population_size: Size of the population
        :param candidate_class: The class of the candidate
        :returns nothing
        """
        self.population_size = population_size
        self.candidate_obj = candidate_obj
        self._population_encoded = None
        self._population_decoded = None

    def generate_population(self):
        """
        Override this function to initialize the population.
        Each member of the populaiton should be contained in a
        list and should be an object of the Candidate class.
        """
        population_encoded = []
        population_decoded = []
        for population_idx in range(self.population_size):
            population_encoded.append(self.candidate_obj.generate_candidate())
            population_decoded.append(population_encoded[population_idx]. \
                                    get_candidate_gene_decoded())

        self._population_encoded = population_encoded
        self._population_decoded = population_decoded


    def get_population_encoded(self):
        return self._population_encoded

    def get_population_decoded(self):
        return self._population_decoded
