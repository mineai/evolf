
import copy

class Candidate():
    """
	This Class provides the construction of a
	candidate of the population. Each Candidate object will
    contain a collection of neucleotides objects in some structure.

    Use this class more like an interface.
	"""

    def __init__(self, length_of_candidate,
                neucleotide_generation_function,
                neucleotide_generation_function_args):
        """
        The constructor of the class initializes the structure
        function and the _gene_information as none.
        _gene_information_encoded: The genetic information
        of the candidate in form of a list containing
        nucleotide objects.
        _gene_information_decoded: The genetic information
        of the candidate in form of the _neucleotide_information
        of the Neucleotide object
        """
        self.length_of_candidate = length_of_candidate
        self.neucleotide_generation_function = neucleotide_generation_function
        self.neucleotide_generation_function_args = neucleotide_generation_function_args
        self._gene_information_encoded = None
        self._gene_information_decoded = None

    def generate_candidate(self):
        """
		This function uses a neucleotide generator to generate a dna.
		This function should be overriden in the derived class.

		:returns nothing: It should assign the generated gene to
        the class variable _gene_information. The generated genes
        should be a collection of neucleotide objects that are
        assigned to __gene_information_encoded and the
        neucleotide objects _neucleotide_information should
        be assigned to __gene_information_decoded
		"""
        raise NotImplementedError

    def get_candidate_gene_encoded(self):
        """
        This function returns the private __gene_information_encoded variable
        which contains the Neucleotide objects
		:params none
		:returns encoded_gene: Generated gene encoded if any
        """
        encoded_gene = self._gene_information_encoded
        return encoded_gene

    def get_candidate_gene_decoded(self):
        """
        This function returns the private __gene_information_encoded variable
        which contains the neuclotide information of the Neucleotide objects
		:params none
		:returns decoded_gene: Generated gene encoded if any
        """
        decoded_gene = self._gene_information_decoded
        return decoded_gene
