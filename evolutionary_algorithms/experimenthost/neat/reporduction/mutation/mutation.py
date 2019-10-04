from evolutionary_algorithms.experimenthost.neat.reporduction.selection.selection import Selection
from evolutionary_algorithms.experimenthost.neat.utils.neat_utils import NeatUtils
from evolutionary_algorithms.experimenthost.neat.genotype.connection_gene \
    import ConnectionGene
from evolutionary_algorithms.experimenthost.neat.genotype.node_gene \
    import NodeGene
import random


class Mutation():

    def __init__(self, latest_innovation_number=1):
        """
        :param latest_innovation_number: The next innovation number to be used.
        """
        self.latest_innovation_number = latest_innovation_number

    def update_innovation(self):
        """
        This function updates the innovation number.
        """
        self.latest_innovation_number += 1

    def mutate_weight_value(self, nodes, connection_genes, uniform_perturbed_probability):
        """
        This function depending on the uniform_perturbed_probability either changes the
        weight randomly or assigns a new random weight.
        :param nodes:
        :param connection_genes:
        :param uniform_perturbed_probability:
        :return:
        """
        for connection in connection_genes:
            if random.random() < uniform_perturbed_probability:
                new_weight = connection.get_weight() + random.uniform(-2, 2)
            else:
                new_weight = random.uniform(-2, 2)
            connection.set_weight(new_weight)

    def mutate_connections(self, nodes, connection_genes, connection_specs={}):
        """
        This function takes in two nodes and mutates the tree by creating a new connection
        :param nodes:
        :param connection_genes:
        :param connection_specs: A dictionary containing information required to
        add the mutation
        :return nothing:
        """
        node_1, node_2 = Selection().select_nodes(nodes)
        # Fix the sequence of the nodes.
        node_incoming, node_outgoing = NeatUtils().validate_node_sequence(node_1,
                                                                          node_2)
        connection_exists = NeatUtils().validate_existing_connection(node_incoming, node_outgoing,
                                                                     connection_genes)

        if not connection_exists:
            lower_weight_range = connection_specs.get("lower_weight_range", -1)
            higher_weight_range = connection_specs.get("higher_weight_range", 1)
            new_weight = random.uniform(lower_weight_range, higher_weight_range)
            expressed = connection_specs.get("is_expressed", True)
            new_connection = ConnectionGene(node_incoming.get_id(), node_outgoing.get_id(),
                                            new_weight, expressed, self.latest_innovation_number)
            self.update_innovation()
            connection_genes.append(new_connection)

        return connection_genes

    def mutate_node(self, nodes, connection_genes):
        """
        This function adds a node between two nodes.
        The old_in_node -> new node = Receives a weight of 1 and a new innovation number
        The new_node -> old_out_node = Receives the old weight and the old innovation number
        :return nothing:
        """
        # Select an existing connection at random
        connection = Selection().select_connection(connection_genes)

        in_node_id, out_node_id = connection.get_in_node(), connection.get_out_node()
        in_node, out_node = None, None

        for node in nodes:
            if node.get_id() == in_node_id:
                in_node = node
            elif node.get_id() == out_node_id:
                out_node = node

        connection.disable()

        # Create a new Node
        new_node = NodeGene("HIDDEN", len(nodes) + 1)

        # Create Connection from in_node to new_node
        new_in_connection = ConnectionGene(in_node.get_id(), new_node.get_id(), 1.00, True,
                                           self.latest_innovation_number)
        self.update_innovation()

        # Create Connection from new_node to out_node
        new_out_connection = ConnectionGene(new_node.get_id(), out_node.get_id(), connection.get_weight(), True,
                                            self.latest_innovation_number)
        self.update_innovation()

        nodes.append(new_node)
        connection_genes.append(new_in_connection)
        connection_genes.append(new_out_connection)

        return [nodes, connection_genes]
