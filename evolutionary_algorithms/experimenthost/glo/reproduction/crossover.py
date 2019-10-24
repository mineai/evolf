class Crossover:
    """
    Class Comments
    """

    @staticmethod
    def crossover(tree_1, tree_2):

        """

        This function will pick random spots in two trees that are passed in that will
        be labeled cutting points. In tree1, the cutting point represents the node
        where the new tree fragment will be placed. In tree2, the cutting point
        represents the root node of the tree fragment that will be placed in tree1.
        The function will return the modified tree1.

        :param tree_1: The first of two trees that will take a piece of tree2, creating
        a completely new tree.
        :param tree_2: The second of two trees that will provide a piece of itself that
        will replace a node in tree1
        :return: tree_1 with the switched out node

        """

        import copy
        import random

        # Randomly generate ids to select nodes within each tree
        cutting_point_1 = random.randint(2, tree_1.number_of_nodes)
        cutting_point_2 = random.randint(2, tree_2.number_of_nodes)

        child = copy.deepcopy(tree_1)

        # Retrieve the Node objects by id
        selected_node_1 = child.get_node_by_id(cutting_point_1)
        selected_node_2 = copy.deepcopy(tree_2.get_node_by_id(cutting_point_2))

        # Replace selected_node_1 with selected_node_2 in its respective tree.
        if selected_node_1.parent.operator_type in ['U', 'R']:
            selected_node_1.parent.left = selected_node_2
        elif selected_node_1.parent.operator_type in ['B']:
            if selected_node_1.parent.left == selected_node_1:
                selected_node_1.parent.left = selected_node_2
            else:
                selected_node_1.parent.right = selected_node_2

        # Reset the node id's
        child.reset_tree()

        return child
