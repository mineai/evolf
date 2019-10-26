import copy
import random
from random import *
from evolutionary_algorithms.experimenthost.glo.utils.visualize \
    import Visualize
class Crossover:
    """
    Class Comments
    """
    
    tracker = 0  # Value to track the traversal through to the crossover point

    tracking = 0  # Current value of the crossover point

    ismain = True  # Marks if tree is main or auxillary

    mainnode = None  # Stores main node

    auxnode = None  # Stores auxiallary node


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
        # child.reset_tree()

        return child
    '''CROSSOVER ALGORITHM OVERVIEW:
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
    time'''

# Methods for level order traversal through trees------------------------------

    @classmethod
    def getGivenLevel(cls, root, level):

        if root is None:

            return

        if level == 1:

            cls.tracker += 1
            if(cls.tracker == cls.tracking):

                print ("Chosen " + str(cls.tracking))
                if(cls.ismain):

                    cls.mainnode = root

                else:

                    cls.auxnode = copy.deepcopy(root)

        elif level > 1:

            cls.getGivenLevel(root.left, level-1)
            cls.getGivenLevel(root.right, level-1)

    @classmethod
    def height(cls, node):

        if node is None:

            return 0

        else:

            lheight = cls.height(node.left)
            rheight = cls.height(node.right)
            if lheight > rheight:

                return lheight+1

            else:

                return rheight+1

    @classmethod
    def getLevelOrder(cls, root):

        h = cls.height(root)
        print("New tree")
        for i in range(1, h+1):

            cls.getGivenLevel(root, i)

# End--------------------------------------------------------------------

    @classmethod
    def crossover_n_trees(cls, lists):
        
        n = 1
        listofmainco = []
        listofothco = []
        lists.sort(reverse=True)
        maintree = copy.deepcopy(lists[0])
        numofcop = len(lists)-1

        for num in range(0, numofcop):
            random_num = randint(2, maintree.number_of_nodes)
            while random_num in listofmainco:
                random_num = randint(2, maintree.number_of_nodes)
            listofmainco.append(random_num)

        for num in range(0, numofcop):
            try:
                listofothco.append(randint((2*n), lists[num+1].number_of_nodes))
                n += 1
            except:
                listofothco.append(-1)
        print('These are the main coeffs')
        print(listofmainco)
        print('These are the sub coeffs')
        print(listofothco)
        print(list)
        tree_copies = [copy.deepcopy(maintree)]
        for val in range(0, len(lists)-1):

            cls.tracking = listofmainco[val]
            cls.tracker = 0
            cls.ismain = True
            cls.getLevelOrder(maintree.root)
            cls.tracker = 0
            cls.ismain = False
            cls.tracking = listofothco[val]
            cls.getLevelOrder(copy.deepcopy(lists[val+1].root))

            if(cls.mainnode.parent.left == cls.mainnode):

                cls.mainnode.parent.left = cls.auxnode

            elif(cls.mainnode.parent.right == cls.mainnode):

                cls.mainnode.parent.right = cls.auxnode

            maintree.reset_tree()
            tree_copies.append(copy.deepcopy(maintree))
            tree_copies.append(copy.deepcopy(lists[val+1]))

        Visualize.visualize(tree_copies)
        cls.getLevelOrder(maintree.root)
        return maintree

