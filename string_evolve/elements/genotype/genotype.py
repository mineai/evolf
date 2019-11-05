
class Genotype():
    """
    This class is the binary representation of a
    the Neucleotide.
    """

    def __init__(self, neucleotide_obj):
        self._neucleotide_obj = neucleotide_obj

    def produce_genotype(self):
        """
        This function can be overriden to produce the binary
        representation of the Neucleotide.
        """

        raise NotImplementedError
