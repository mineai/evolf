from evolutionary_algorithms.experimenthost.glo.elements.tree.linear_tree import LinearTree
from evolutionary_algorithms.experimenthost.glo.elements.tree.tree_construction import TreeConstruction
from evolutionary_algorithms.experimenthost.glo.utils.visualize import Visualize
from evolutionary_algorithms.experimenthost.glo.evaluation_validation.evaluate_tree import EvaluateTree
from evolutionary_algorithms.experimenthost.glo.evaluation_validation.validate import Validate


class Tree(LinearTree, TreeConstruction):
    """
    The Tree() class constructs trees of heights specified by a range that is
    passed in on the Constructor call.
    """

    # Constructor
    def __init__(self, min_height=2, max_height=4):
        """
        The constructor Tree objects.

        -height tracks the height of the tree and is initialized to 0.

        -To create trees with fixed height, both min_height and max_height
        are set to max_height.

        """
        TreeConstruction.__init__(self, min_height, max_height)
        LinearTree.__init__(self, self.root)

        self.symbolic_expression = None

        # A flag set after validation to mark if this tree is working or not. None represents
        # that it has not yet been validated.
        self.working = None

        self.fitness = None  # The fitness of the tree
        self.avg_epoch_time = None  # If the NN is a fitness function, then the time for each Epoch.

        # Construct the Expression and the Linear Tree
        self.initialize_parents()
        self.assign_level_order_id()
        self.linearize_tree()
        self.construct_symbolic_expression()
        self.validate_working()
        # self.visualize_tree()

    """
    ################ Expression #################
    """

    def construct_symbolic_expression(self):
        """
        This function calls the build_symbolic_expression function from the
        EvaluateTree class and initializes the required class functions.
        It is responsible for building a symbolic expression from the tree.
        :return nothing:
        """
        self.symbolic_expression = EvaluateTree.build_symbolic_expression(self)

    def validate_working(self):
        """
        This function validates if the expression this tree contains
        is valid.
        :return:
        """
        literals = ["y_true", "y_pred"]
        self.working = Validate.has_required_literals(self.symbolic_expression, literals)

    """
    ################ Tree Modifications Operations #################
    """

    def insert_binary_parent(self, node, parent, another_child, position="right"):
        """
        This function takes in a "node" to which its "parent" has to be added. If "position" is
        "right", the node becomes the right child of the new parent "parent" and "another_child"
        becomes the "left" child. And vice-versa if position is "left"
        :param parent: A node object with operator type
        :param another_child: A Node object that has to become the other child of the binary parent
        :param node: A Node object and also the location to which the parent has to be inserted
        :param position: A string ("left" or "right") that ensures that the node variable becomes
        the corresponding child of the "parent"
        :return:
        """
        # If it is the root node
        assert node.parent is not None, "Cannot Insert a parent to the optimizer root node"
        if node.parent.operator_type == "U":
            node.parent.left = parent
        elif node.parent.operator_type == "B":
            if node.parent.left == node:
                node.parent.left = parent
            elif node.parent.right == node:
                node.parent.right = parent

        if position.lower() == "left":
            parent.left = node
            parent.right = another_child
        elif position.lower() == "right":
            parent.right = node
            parent.left = another_child

        node.parent = parent
        another_child.parent = parent
        self.number_of_nodes += 1
        parent.node_id = self.number_of_nodes
        self.number_of_nodes += 1
        another_child.node_id = self.number_of_nodes

    """
    ################ Utils ################
    """

    def generate_printable_expression(self):
        """
        This function prints the expression that is contained in this tree.
        :return nothing:
        """
        if self.symbolic_expression is None:
            raise ValueError("Expression Not Built Yet!")
        else:
            expression = f"Expression: {self.root.function_str} ( {self.symbolic_expression} )"
            # print(expression)
            return expression

    def visualize_tree(self, path=None):
        import os
        if path is None:
            path = f"{os.getcwd()}/results/glo_test_tree"
        Visualize.visualize(self, path=path)

    def reset_tree(self):
        self.nodes = []
        self.symbolic_expression = None
        self.working = None
        self.height = 0
        self.unary_count = 0
        self.binary_count = 0
        self.literal_count = 0

        self.initialize_height()
        self.assign_level_order_id()
        self.init_node_type_count()
        self.initialize_parents()
        self.linearize_tree()
        self.construct_symbolic_expression()
        self.validate_working()

        self.number_of_nodes = len(self.nodes)
