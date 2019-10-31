from neat.genotype.connection_gene \
    import ConnectionGene
from neat.genotype.node_gene \
    import NodeGene
import random


class NetworkConstructor():

    @classmethod
    def construct_network(cls, num_inputs, num_outputs, method="sparsely_connected"):
        """
        This method serves as the entry point to connect an initial network
        :param num_inputs: The number of input Neurons
        :param num_outputs: The number of output Neurons
        :param method: String describing which method to use to generate the
        initial NN.
        :returns: A list connected the added nodes, conneciton_genes and the next innovation number
        to be used
        """
        if method == "fully_connected":
            nodes, connection_genes, innovation_number = cls.construct_fully_connected_network(num_inputs, num_outputs)
        else:
            nodes, connection_genes, innovation_number = cls.construct_sparsely_connected_network(num_inputs,
                                                                                                  num_outputs)

        return [nodes, connection_genes, innovation_number]

    @classmethod
    def construct_sparsely_connected_network(self, num_inputs, num_outputs):
        """
        This function creates a sparsely connected network with atleast one connection
        for all nodes.
        :param num_inputs: The number of input Neurons
        :param num_outputs: The number of output Neurons
        :returns: A list connected the added nodes, conneciton_genes and the next innovation number
        to be used
        """
        connection_genes = []
        nodes, input_nodes, output_nodes = self.add_initial_nodes_to_network(num_inputs, num_outputs)

        innovation_number = 1
        if num_inputs > num_outputs:
            for out_node_num, out_node in enumerate(output_nodes):
                in_node = input_nodes[out_node_num]
                connection = ConnectionGene(in_node.get_id(),
                                            out_node.get_id(),
                                            random.uniform(-1, 1),
                                            True, innovation_number)
                innovation_number += 1
                connection_genes.append(connection)

            for in_node in input_nodes[len(output_nodes):]:
                random_output = output_nodes[random.randint(0, len(output_nodes) - 1)]
                connection = ConnectionGene(in_node.get_id(),
                                            random_output.get_id(),
                                            random.uniform(-1, 1),
                                            True, innovation_number)
                innovation_number += 1
                connection_genes.append(connection)
        else:
            for in_node_num, in_node in enumerate(input_nodes):
                out_node = output_nodes[in_node_num]
                connection = ConnectionGene(in_node.get_id(),
                                            out_node.get_id(),
                                            random.uniform(-1, 1),
                                            True, innovation_number)
                innovation_number += 1
                connection_genes.append(connection)

            for out_node in output_nodes[len(input_nodes):]:
                random_input = input_nodes[random.randint(0, len(input_nodes) - 1)]
                connection = ConnectionGene(random_input.get_id(),
                                            out_node.get_id(),
                                            random.uniform(-1, 1),
                                            True, innovation_number)
                innovation_number += 1
                connection_genes.append(connection)

        return [nodes, connection_genes, innovation_number]

    @classmethod
    def construct_fully_connected_network(self, num_inputs, num_outputs):
        """
        This functions constructs the basic Neural Network Graph
        with only Input and Output layers.
        :param num_inputs: The number of input Neurons
        :param num_outputs: The number of output Neurons
        :returns: A list connected the added nodes, conneciton_genes and the next innovation number
        to be used
        """
        connection_genes = []
        nodes, input_nodes, output_nodes = self.add_initial_nodes_to_network(num_inputs, num_outputs)

        innovation_number = 1
        # ADD CONNECTIONS
        for in_node in input_nodes:
            for out_node in output_nodes:
                connection = ConnectionGene(in_node.get_id(),
                                            out_node.get_id(),
                                            random.uniform(-1, 1),
                                            True, innovation_number)
                innovation_number += 1
                connection_genes.append(connection)

        return [nodes, connection_genes, innovation_number]

    @staticmethod
    def add_initial_nodes_to_network(num_inputs, num_outputs):
        """
        This function adds the node genes to the network
        :param num_inputs: The number of input Neurons
        :param num_outputs: The number of output Neurons
        :returns: A list connecting lists of all the nodes object, the input_notes and the output_nodes.
        """
        nodes = []
        input_nodes, output_nodes = [], []
        for node_num in range(1, num_inputs + 1):
            node = NodeGene("INPUT", node_num)
            nodes.append(node)
            input_nodes.append(node)

        idx_to_start = len(nodes) + 1

        for node_num in range(idx_to_start, num_outputs + idx_to_start):
            node = NodeGene("OUTPUT", node_num)
            nodes.append(node)
            output_nodes.append(node)

        return [nodes, input_nodes, output_nodes]
