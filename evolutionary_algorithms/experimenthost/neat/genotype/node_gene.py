# Import Libraries
from enum import Enum


class TYPE(Enum):
    """
    Describe an ENUM to inform the
    service what operator_type of node it is.
    """
    INPUT = 0
    HIDDEN = 1
    OUTPUT = 2


class NodeGene:
    """
    This class serves as the Node Geneotype described
    in the NEAT paper.
    """
    def __init__(self, layer_type, id, activation="relu"):
        """

        :param operator_type:
        :param id:
        """
        self._type = TYPE[layer_type]
        self._id = id
        self._activation = activation

    def get_type(self):
        """
        This function returns the private variable operator_type
        """
        return self._type

    def get_id(self):
        """
        This function returns the private variable node_id
        """
        return self._id

    def clone_gene(self):
        """
        This function clones the gene and returns a new object.
        :return:
        """
        return NodeGene(self._type.name, self._id, self._activation)
