from string_evolve.elements.candidate.candidate \
    import Candidate

from string_evolve.elements.neucleotide.neucleotide \
    import Neucleotide

import copy

class CandidateList(Candidate):
    """
    This class generates a candidate of a list struct

    """

    def __init__(self, length_of_candidate,
                neucleotide_generation_function, neucleotide_generation_function_args=None):
        """
        The constructors calls the constructor of the base class.

        :param length_of_candidate: Lenght of the candidate
        :param neucleotide_generation_function: Function to
        generate the neucleotide
        :param neucleotide_generation_function_args: Args to
        neucleotide_generation_function_args
        """
        super().__init__(length_of_candidate,
                    neucleotide_generation_function, neucleotide_generation_function_args)

    def generate_candidate(self):
        """
        This Function Generates a candidate of list struct using
        neucleotides of the desired length.

        :params none
        :returns self: The object itself but with the gene information
        created.
        """
        self = copy.copy(self)
        gene_encoded = []
        gene_decoded = []
        for neucleotide_num in range(self.length_of_candidate):
            neucleotide = Neucleotide(self.neucleotide_generation_function,
                            self.neucleotide_generation_function_args)
            neucleotide.generate_neuclotide()
            gene_encoded.append(neucleotide)
            gene_decoded.append(neucleotide.get_neucleotide())

        self._gene_information_encoded = gene_encoded
        self._gene_information_decoded = gene_decoded

        return self
