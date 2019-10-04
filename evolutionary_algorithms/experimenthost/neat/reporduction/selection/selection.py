import random


class Selection:

    @staticmethod
    def select_nodes(node_genes):
        """
        This function selects two nodes randomly from
        the node_genes list
        :param node_genes: A list containing objects of Node Gene Class
        :return selected_nodes: Two Randomly selected genes
        """
        node_1 = node_genes[random.randint(0, len(node_genes) - 1)]
        node_2 = node_genes[random.randint(0, len(node_genes) - 1)]

        while (node_1.get_type().name == "INPUT" and node_2.get_type().name == "INPUT") or \
                (node_1.get_type().name == "OUTPUT" and node_2.get_type().name == "OUTPUT") or \
                (node_1.get_id() == node_2.get_id()):
            node_2 = node_genes[random.randint(0, len(node_genes) - 1)]

        selected_nodes = [node_1, node_2]
        return selected_nodes

    @staticmethod
    def select_connection(connection_genes):
        """
        This function selects a connection gene randomly from
        the connection_genes list
        :param connection_genes: A list containing objects of Connection Gene Class
        :return connection: The randomly sampled connection
        """
        connection = connection_genes[random.randint(0, len(connection_genes) - 1)]
        return connection
