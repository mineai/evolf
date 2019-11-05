from neat.genotype.node_gene \
    import TYPE


class NeatUtils():

    @staticmethod
    def validate_node_sequence(node_1, node_2):
        """
        This function takes in two nodes and verifies if they
        are in the correct order.
        Eg: node_1 => INPUT, node_2 => HIDDEN is a valid sequence.
        However, node_1 => HIDDEN, node_2 => INPUT is an invalid sequence.
        :param node_1: Object of NodeGene class
        :param node_2: Object of NodeGene class
        :return nodes: List containing the input nodes in the correct order
        """
        if (node_1.get_type() == TYPE["HIDDEN"] and \
            node_2.get_type() == TYPE["INPUT"]) or \
                (node_1.get_type() == TYPE["OUTPUT"] and
                 node_2.get_type() == TYPE["HIDDEN"]) or \
                (node_1.get_type() == TYPE["OUTPUT"] and
                 node_2.get_type() == TYPE["INPUT"]):
            nodes = [node_2, node_1]
        else:
            nodes = [node_1, node_2]

        return nodes

    @classmethod
    def validate_existing_connection(self, node_1, node_2, connection_genes):
        """
        This Function checks if a connection between two nodes exists or not.
        :param node_1: Object of Node Gene class
        :param node_2: Object of Node Gene class
        :param connection_genes: List Containing the connection gene objects
        :return _connection_exists: A boolean value that describes if the connection
                exists
        """
        node_inc, node_out = self.validate_node_sequence(node_1, node_2)

        _connection_exists = False
        for connection_gene in connection_genes:
            if connection_gene.get_in_node() == node_inc.get_id() and \
                    connection_gene.get_out_node() == node_out.get_id():
                _connection_exists = True
                break

        return _connection_exists