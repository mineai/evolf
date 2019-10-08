import random
from evolutionary_algorithms.experimenthost.glo.elements.node \
    import Node
from evolutionary_algorithms.experimenthost.glo.evaluation_validation.evaluate_tree import EvaluateTree
from evolutionary_algorithms.experimenthost.glo.evaluation_validation.validate import Validate
from evolutionary_algorithms.experimenthost.glo.populate.function_library \
    import FunctionLibrary


class Tree:
    """

    The Tree() class constructs trees of heights specified by a range that is
    passed in on the Constructor call. 

    """

    # Constructor
    def __init__(self, min_height=3, max_height=10):
        """
            The constructor Tree objects.

            -height tracks the height of the tree and is initialized to 0.

            -To create trees with fixed height, both min_height and max_height
            are set to max_height.

            -I also initialized counters for U, B, and L nodes to keep track of 
            how often each is used in each tree.
        """

        self.height = 0
        self.root = None
        self.current_id = 0
        self.max_height = max_height
        self.min_height = min_height
        self.unary_count = 0
        self.binary_count = 0
        self.literal_count = 0

        self.root_function = None
        self.root_function_label = None
        self.symbolic_expression = None

        self.function_list = None
        self.tensorflow_handle_list = None

        self.token_list = FunctionLibrary.get_token_types()

        self.working = None
        self.fitness = None

    def request_token(self):
        """

        returns a token based on the instantanious height of the tree
        taking into account the min and max heights set earlier

        arguments: Nothing
        returns: token (string) - either 'U', 'B', or 'L'

        """
        if self.height == 0:
            return "R"
        elif self.height < self.min_height:
            return self.token_list[random.randint(0, 1)]
        elif self.height >= self.max_height:
            return 'L'
        else:
            return self.token_list[random.randint(0, 2)]

    def helper_function(self, token):
        """

        This function calls one the node generating function that corresponds to 
        the token that is passed in. This function is the 'middle-man' in simulating
        random node generation.
        
        token: (string) contains the randomly selected token which is either
               going to be a 'U', 'B', or, 'L' and determines which node 
               generating funtion is called.

        returns: a Node() object that is returned the node generating functions,
                 unary(), binary(), or literal().

        """
        if token in ['U', 'R']:
            return self.unary(token)
        elif token == 'B':
            return self.binary(token)
        elif token == 'L':
            return self.literal(token)
        return None

    def literal(self, token):
        """

        A literal Node will not have any children

        Example Output:

                L
            /       \
        None        None

        """

        sample_operator = FunctionLibrary.sample(token)
        current_node = Node(token, sample_operator[token])
        self.literal_count += 1
        current_node.right = None
        current_node.left = None
        self.current_id += 1
        current_node.node_id = self.current_id
        return current_node

    def binary(self, token):
        """
        A binary Node will have two children, each of
        which are going to be randomly selected using
        request_token() and helper_function()

        * Tree height is iterated here

        Example Output:
                B
            /       \
            U       L

        """
        sample_operator = FunctionLibrary.sample(token)
        current_node = Node(token, sample_operator[token])
        self.height += 1
        self.binary_count += 1
        current_node.left = self.helper_function(self.request_token())
        current_node.right = self.helper_function(self.request_token())
        self.current_id += 1
        current_node.node_id = self.current_id
        return current_node

    def unary(self, token):

        """
        
        A unary Node will have one child that will be
        randomly selected using request_token() and helper_function()

        * Tree height is iterated here

        Example Output:
                U
            /       \
            B       None

        """

        sample_operator = FunctionLibrary.sample(token)
        current_node = Node(token, sample_operator[token])
        self.height += 1
        self.unary_count += 1
        current_node.left = self.helper_function(self.request_token())
        current_node.right = None
        self.current_id += 1
        current_node.node_id = self.current_id
        return current_node

    def construct_symbolic_expression(self):
        self.root_function_label, self.root_function, self.function_list, self.tensorflow_handle_list, \
        self.symbolic_expression = \
            EvaluateTree.build_symbolic_expression(self)

    def validate_working(self):
        self.working = Validate.validate_literal_existance(self.symbolic_expression)

    def print_expression(self):
        if self.symbolic_expression is None:
            raise ValueError("Expression Not Built Yet!")
        else:
            print(f"Expression: {self.root_function_label} ( {self.symbolic_expression} )")
