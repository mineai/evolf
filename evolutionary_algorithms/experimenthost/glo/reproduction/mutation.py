import random
import copy

from evolutionary_algorithms.experimenthost.glo.elements.node import Node
from evolutionary_algorithms.experimenthost.glo.populate.function_library import FunctionLibrary


class Mutation:

    @staticmethod
    def weighted_function_mutation(tree, mutate_node_function_rate=0.1):
        """
        THis function mutates nodes of the tree by replacing them with another
        weighted function of the same type.

        Note: this function does not mutate "R" nodes.
        :param tree: The tree object to be mutated
        :param mutate_node_function_rate:
        :return child: The mutated tree object
        """
        child = copy.deepcopy(tree)
        for node in child.nodes:
            if node.operator_type not in ["R"]:
                if random.random() < mutate_node_function_rate:
                    # Mutate the Operator in this node
                    operator_type = node.operator_type
                    new_function = FunctionLibrary.sample(operator_type)
                    node.function_str = new_function
                    node.tensorflow_handle = FunctionLibrary.get_tensorflow_handle(new_function)
                    node.symbolic_handle = FunctionLibrary.get_symbolic_handle(new_function)

                    # Create A multiplicative node for multiplication
                    operator_type = "B"
                    function_str = "*"
                    symbolic_handle = FunctionLibrary.get_symbolic_handle(function_str)
                    tensorflow_handle = FunctionLibrary.get_tensorflow_handle(function_str)
                    multiplicative_node = Node(operator_type=operator_type, function_str=function_str,
                                               symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)

                    # Weight Node
                    weight = random.uniform(-10, 10)
                    operator_type = "L"
                    if weight >= 0:
                        function_str = "pos_scalar"
                    else:
                        function_str = "neg_scalar"
                    symbolic_handle = weight * FunctionLibrary.get_symbolic_handle("pos_scalar")
                    tensorflow_handle = weight * FunctionLibrary.get_tensorflow_handle("pos_scalar")
                    weight_node = Node(operator_type=operator_type, function_str=function_str,
                                       symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)

                    child.insert_binary_parent(node, multiplicative_node, weight_node)

        child.reset_tree()
        return child

    @staticmethod
    def mutate_value_literal_nodes(tree, mutate_integer_nodes_rate=0.025):
        """
        This function mutates value literals by incrementing or decrementing them
        :param tree: The tree object to be mutated
        :param mutate_integer_nodes_rate:
        :return child: The mutated tree object
        """
        child = copy.deepcopy(tree)
        linearized_tree = child.nodes
        for node in linearized_tree:
            if node.function_str in ["pos_scalar", "neg_scalar"]:
                if random.random() < mutate_integer_nodes_rate:
                    random_int = random.randint(-2, 2)
                    node.symbolic_handle += random_int
                    node.tensorflow_handle += random_int

        child.reset_tree()
        return child

    @staticmethod
    def mutate_leaf_node(tree, mutate_leaf_rate=0.025):
        pass
