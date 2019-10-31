class NeucleotideGenerationLibrary():
    """
    This class contains some basic functions that can be used as
    the basic neucleotide for evolution.
    """

    @staticmethod
    def ascii_neucleotide(lower_ascii=0, upper_ascii=127):
    	"""
    	This function generates a random character between
    	the ASCII values specified.

    	:param lower_ascii: Lower limit for ASCII. Default is 0.
            :param upper_ascii: Upper limit for ASCII. Default is 127.

    	:returns random_gene: A random character
    	generated between ASCII limits specified.
    	"""
    	import random
    	random_ascii = random.randint(lower_ascii,
    					upper_ascii)
    	random_char = chr(random_ascii)
    	return random_char
