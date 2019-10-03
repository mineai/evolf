
class Genome:
    """
    This class wraps around the Connection Gene and Node Gene
    to build the basic block for a candidate.
    """

    def __init__(self):
        """
        The constructor initializes the default value for
        the instance variables.
        """
        self._nodes = {}
        self._connection_genes = {}

    """
    Setters and Getters
    """
    def add_node(self, node):
        self._nodes[node.get_id()] = node

    def add_connection_gene(self, connection):
        self._connection_genes[connection.get_innovation_number()] = connection

    def get_connection_genes(self):
        return self._connection_genes

    def get_nodes(self):
        return self._nodes

    def set_connection_genes_from_dict(self, value):
        assert isinstance(value, dict), "Connection Genes should be a dictionary"
        self._connection_genes = value

    def set_nodes_from_dict(self, value):
        assert isinstance(value, dict), "Nodes should be a dictionary"
        self._nodes = value

    def set_connection_genes_from_list(self, connection_genes):
        connection_genes_dict = {}
        for connection in connection_genes:
            connection_genes_dict[connection.get_innovation_number()] = connection

        self._connection_genes = connection_genes_dict

    def set_nodes_from_list(self, nodes):
        nodes_dict = {}
        for node in nodes:
            nodes_dict[node.get_id()] = node

        self._nodes = nodes_dict
