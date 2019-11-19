import random
import copy

from framework.elements.node.node_constructor import NodeConstructor
from framework.elements.tree.tree import Tree


class Mutation:

    @staticmethod
    def weighted_function_mutation(tree, mutate_node_function_rate=0.1, search_space_obj=None):
        """
        THis function mutates nodes of the tree by replacing them with another
        weighted function of the same type.

        Note: this function does not mutate "R" nodes.
        :param tree: The tree object to be mutated
        :param mutate_node_function_rate:
        :return child: The mutated tree object
        """
        child = copy.deepcopy(tree)

        # Select a random node as the root of the new subtree
        selected_node_id = random.randint(1, child.number_of_nodes)
        selected_node = child.get_node_by_id(selected_node_id)

        # If it picks a terminal node, keep selecting nodes at random
        # until it picks a non-terminal
        while selected_node.operator_type in ['L']:
            selected_node_id = random.randint(1, child.number_of_nodes)
            selected_node = child.get_node_by_id(selected_node_id)

        if random.random() < mutate_node_function_rate:
            # Mutate the Operator in this node
            operator_type = selected_node.operator_type
            new_function = search_space_obj.sample(operator_type)
            selected_node.function_str = new_function
            selected_node.tensorflow_handle = search_space_obj.get_tensorflow_handle(new_function)
            selected_node.symbolic_handle = search_space_obj.get_symbolic_handle(new_function)

            weight = random.uniform(--10, 10)
            selected_node.coefficient = weight

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
        # child = tree
        linearized_tree = child.nodes
        for node in linearized_tree:
            if node.function_str in ["pos_scalar", "neg_scalar"]:
                if random.random() < mutate_integer_nodes_rate:
                    random_int = random.randint(-2, 2)
                    node.symbolic_handle += random_int
                    node.tensorflow_handle += random_int
            # else:
            #     print(f'node.function_str = {node.function_str}')
            #     print('Mutation did not occur')

        child.reset_tree()
        return child

    @staticmethod
    def mutate_leaf_node(tree, mutate_leaf_rate=0.025, search_space_obj=None):
        """

        :param tree:
        :param mutate_leaf_rate:
        :return:
        """
        child = copy.deepcopy(tree)
        # child = tree
        for node in child.nodes:
            if node.operator_type == "L":
                if random.random() < mutate_leaf_rate:
                    new_tree = Tree(2, random.randint(2, 3), search_space_obj=search_space_obj)
                    if node.parent.operator_type in ["U", "R"]:
                        node.parent.left = new_tree.root.left
                    elif node.parent.operator_type in ["B"]:
                        if node.parent.left == node:
                            node.parent.left = new_tree.root.left
                        else:
                            node.parent.right = new_tree.root.left
                    break

        child.reset_tree()
        return child

    @staticmethod
    def hoist_mutation(tree, mutation_rate=0.025):

        """

        This mutation selects a subtree at random and returns that subtree as the mutation of the original tree.

        :param tree:
        :param mutation_rate:
        :return child:
        """

        child = copy.deepcopy(tree)
        if child.height <= 3:
            return child

        mutation_prob = random.random()
        if mutation_prob < mutation_rate:
            # Select a random node as the root of the new subtree
            selected_node_id = random.randint(3, child.number_of_nodes)
            selected_node = child.get_node_by_id(selected_node_id)

            # If it picks a terminal node, keep selecting nodes at random
            # until it picks a non-terminal
            while selected_node.operator_type in ['L']:
                selected_node_id = random.randint(3, child.number_of_nodes)
                selected_node = child.get_node_by_id(selected_node_id)

            child.root.left = selected_node

        child.reset_tree()
        return child

    @staticmethod
    def shrink_mutation(tree, mutation_rate=0.025, search_space_obj=None):
        """

        This mutation selects a non-terminal node at random and changes it to a
        terminal node.

        :param tree:
        :param mutation_rate:
        :return child:
        """

        child = copy.deepcopy(tree)
        if child.height <= 3:
            return child

        mutation_prob = random.random()
        if mutation_prob < mutation_rate:
            # Select a node at random
            selected_node_id = random.randint(3, child.number_of_nodes)
            selected_node = child.get_node_by_id(selected_node_id)

            # If the selected node is a terminal, keep selecting nodes at
            # random until you select a non-terminal
            while selected_node.operator_type in ['L']:
                selected_node_id = random.randint(3, child.number_of_nodes)
                selected_node = child.get_node_by_id(selected_node_id)

            # Create a terminal node to replace the randomly selected non terminal
            new_node = NodeConstructor.create_literal_node(search_space_obj=search_space_obj)

            if selected_node.parent.operator_type in ["U", "R"]:
                selected_node.parent.left = new_node
            elif selected_node.parent.operator_type in ["B"]:
                if selected_node.parent.left == selected_node:
                    selected_node.parent.left = new_node
                else:
                    selected_node.parent.right = new_node

        child.reset_tree()
        return child

    @staticmethod
    def literal_swap_mutation(tree, mutation_rate=0.025, search_space_obj=None):

        """

        This mutation will swap y_pred variables with y_true variables and vis versa.

        :param tree:
        :param mutation_rate: probability of the mutation occurring
        :param search_space_obj: used to create the new literal that will replace the old one.
        :return child:
        """

        child = copy.deepcopy(tree)

        # determine whether or not the mutation will occur using the mutation_rate
        if random.random() < mutation_rate:
            t_swapped = False
            y_swapped = False
            for node in child.nodes:
                new_node = None
                if node.function_str in ['y'] and not y_swapped:
                    # create a y_true node
                    new_node = NodeConstructor.create_literal_node('t', search_space_obj=search_space_obj)
                elif node.function_str in ['t'] and not t_swapped:
                    # create a y_pred
                    new_node = NodeConstructor.create_literal_node('y', search_space_obj=search_space_obj)

                # check if a swap occurred
                if new_node is not None:
                    if node.parent.operator_type in ["U", "R"]:
                        node.parent.left = new_node
                    elif node.parent.operator_type in ["B"]:
                        if node.parent.left == node:
                            node.parent.left = new_node
                        else:
                            node.parent.right = new_node

        child.reset_tree()
        return child
