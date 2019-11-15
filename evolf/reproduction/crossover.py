import copy
import random
from random import randint

from evolf.populate.population import Population


class Crossover:
    """
    Class Comments
    """

    tracker = 0  # Value to track the traversal through to the crossover point

    tracking = 0  # Current value of the crossover point

    is_main = True  # Marks if tree is main or auxiliary

    main_node = None  # Stores main node

    aux_node = None  # Stores auxiliary node

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

        tree_1, tree_2 = copy.deepcopy(tree_1), copy.deepcopy(tree_2)

        # Randomly generate ids to select nodes within each tree
        cutting_point_1 = random.randint(3, tree_1.number_of_nodes)
        cutting_point_2 = random.randint(3, tree_2.number_of_nodes)

        # Make Child 1
        child1 = copy.deepcopy(tree_1)
        # Retrieve the Node objects by id
        selected_node_1 = child1.get_node_by_id(cutting_point_1)
        selected_node_2 = copy.deepcopy(tree_2.get_node_by_id(cutting_point_2))

        print(f"Selected Node #1: {selected_node_1.function_str}")
        print(f"Selected Node #2: {selected_node_2.function_str}")

        # Replace selected_node_1 with selected_node_2 in its respective tree.
        if selected_node_1.parent.operator_type in ['U', 'R']:
            selected_node_1.parent.left = selected_node_2
        elif selected_node_1.parent.operator_type in ['B', "BBL"]:
            if selected_node_1.parent.left == selected_node_1:
                selected_node_1.parent.left = selected_node_2
            else:
                selected_node_1.parent.right = selected_node_2

        # Make Child 2
        child2 = copy.deepcopy(tree_2)
        selected_node_2 = copy.deepcopy(tree_1.get_node_by_id(cutting_point_1))
        selected_node_1 = child2.get_node_by_id(cutting_point_2)

        # Replace selected_node_1 with selected_node_2 in its respective tree.
        if selected_node_1.parent.operator_type in ['U', 'R']:
            selected_node_1.parent.left = selected_node_2
        elif selected_node_1.parent.operator_type in ['B', "BBL"]:
            if selected_node_1.parent.left == selected_node_1:
                selected_node_1.parent.left = selected_node_2
            else:
                selected_node_1.parent.right = selected_node_2
                
        child1.reset_tree()
        child2.reset_tree()

        return [child1, child2]


    @classmethod
    def crossover_n_trees(cls, lists):

        """

        CROSSOVER ALGORITHM OVERVIEW:
        This algorithm performs the crossover operation for genetic AI on n trees
        using the following procedure:
        1. Sorts the trees on basis of fitness
        2. Stores the fitest tree as the main tree
        3. Enumerates the number of auxilliary trees invloved (x)
        4. Uses finds x number of crossover points on the main trees
        5. Finds one point on each auxilliary tree
        6. Edits uses the tree below the crossover point on
        each auxilliary tree to replace the each crossover on the main tree
        7. The above operation occurs one at a time and the tree gets reset each
        time

        :param lists:
        :return:
        """

        # Methods for level order traversal through trees------------------------------

        def get_given_level(root, level):

            if root is None:
                return

            if level == 1:
                cls.tracker += 1

                if cls.tracker == cls.tracking:
                    if cls.is_main:
                        cls.main_node = root
                    else:
                        cls.aux_node = copy.deepcopy(root)

            elif level > 1:
                get_given_level(root.left, level-1)
                get_given_level(root.right, level-1)

        def height(node):

            if node is None:
                return 0
            else:
                left_height = height(node.left)
                right_height = height(node.right)

                if left_height > right_height:
                    return left_height+1
                else:
                    return right_height+1

        def get_level_order(root):
            h = height(root)
            for idx in range(1, h+1):
                get_given_level(root, idx)

    # End--------------------------------------------------------------------

        tree_level = 1
        list_of_main_coeff = []
        list_of_other_coeff = []
        lists.sort(reverse=True)
        main_tree = copy.deepcopy(lists[0])
        num_of_aux_trees = len(lists)-1

        for num in range(0, num_of_aux_trees):
            random_num = randint(3, main_tree.number_of_nodes)
            while random_num in list_of_main_coeff:
                random_num = randint(3, main_tree.number_of_nodes)
            list_of_main_coeff.append(random_num)

        for num in range(0, num_of_aux_trees):
            try:
                list_of_other_coeff.append(randint((2*tree_level), lists[num+1].number_of_nodes))
                tree_level += 1
            except:
                list_of_other_coeff.append(-1)

        for val in range(0, len(lists)-1):

            cls.tracking = list_of_main_coeff[val]
            cls.tracker = 0
            cls.is_main = True
            get_level_order(main_tree.root)
            cls.tracker = 0
            cls.is_main = False
            cls.tracking = list_of_other_coeff[val]
            get_level_order(copy.deepcopy(lists[val+1].root))

            if cls.main_node.parent.left == cls.main_node:

                cls.main_node.parent.left = cls.aux_node

            elif cls.main_node.parent.right == cls.main_node:

                cls.main_node.parent.right = cls.aux_node

            main_tree.reset_tree()

        get_level_order(main_tree.root)
        return main_tree
