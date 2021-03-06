from framework.elements.node.node import Node


class TreeConstruction:

    def __init__(self, min_height, max_height, search_space_obj, construction_nodes=None):

        self.search_space_obj = search_space_obj
        if not construction_nodes:
            self.height = 1  # Current height of tree
            self.max_height = max_height  # Maximum Height Allowed for the tree
            self.min_height = min_height  # minimum height allowed for the tree
            self.number_of_nodes = 0  # Number of nodes in the tree

            # Keeps count of number of nodes of each type
            self.unary_count = 0
            self.binary_count = 0
            self.literal_count = 0

            root_type = "R"
            self.root = self.helper_function(root_type)
            self.assign_level_order_id()
        else:
            self.nodes = construction_nodes
            self.number_of_nodes = len(construction_nodes)
            self.root = [node for node in self.nodes if node.operator_type == "R"][0]
            self.initialize_height()
            self.assign_level_order_id()

    def request_token(self):
        """

        returns a token based on the instantaneous height of the tree
        taking into account the min and max heights set earlier

        arguments: Nothing
        returns: token (string) - either 'U', 'B', or 'L'

        """
        if self.height < self.min_height:
            function = self.search_space_obj.sample(["U", "B"])
        elif self.height >= self.max_height:
            function = self.search_space_obj.sample(["L"])
        else:
            function = self.search_space_obj.sample(["L", "U", "B"])

        return self.search_space_obj.get_function_type(function)

    def helper_function(self, token):
        """

        This function calls one the node generating function that corresponds to
        the token that is passed in. This function is the 'middle-man' in simulating
        random node generation.

        token: (string) contains the randomly selected token which is either
               going to be a 'U', 'B', or, 'L' and determines which node
               generating function is called.

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

        current_node = self.generate_node(token)
        self.literal_count += 1
        current_node.right = None
        current_node.left = None
        self.number_of_nodes += 1
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
        current_node = self.generate_node(token)
        self.height += 1
        self.binary_count += 1
        current_node.left = self.helper_function(self.request_token())
        current_node.right = self.helper_function(self.request_token())
        self.number_of_nodes += 1
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

        current_node = self.generate_node(token)
        self.height += 1
        if token is not "R":
            self.unary_count += 1
        current_node.left = self.helper_function(self.request_token())
        current_node.right = None
        self.number_of_nodes += 1
        return current_node

    def generate_node(self, token):
        sample_operator = self.search_space_obj.sample(token)
        tensorflow_handle = self.search_space_obj.get_tensorflow_handle(sample_operator)
        symbolic_handle = self.search_space_obj.get_symbolic_handle(sample_operator)
        node = Node(operator_type=token, function_str=sample_operator,
                    symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)
        node.coefficient = 1
        return node

    def initialize_parents(self):
        def initialize_parents_helper(start):
            # Root -> Left -> Right
            if start:
                if start.left:
                    start.left.parent = start
                if start.right:
                    start.right.parent = start
                initialize_parents_helper(start.left)
                initialize_parents_helper(start.right)

        initialize_parents_helper(self.root)

    """
    Functions to Reset Tree
    """

    def assign_level_order_id(self):

        def assign_level_order_id_helper(root):
            stack, queue = [], []
            queue.append(root)

            # Do something like normal level order traversal order.
            # Following are the differences with normal level order
            # traversal:
            # 1) Instead of printing a node, we push the node to stack
            # 2) Right subtree is visited before left subtree
            while len(queue) > 0:

                # Dequeue node and make it root
                root = queue.pop(0)
                stack.append(root)

                # Enqueue right child
                if root.right:
                    queue.append(root.right)

                    # Enqueue left child
                if root.left:
                    queue.append(root.left)

            # Now pop all items from stack one by one and print them
            node_id = 1
            stack = stack[::-1]
            while len(stack) > 0:
                root = stack.pop()
                root.node_id = node_id
                node_id += 1

        assign_level_order_id_helper(self.root)

    def initialize_height(self):

        def helper_function_get_height(node):
            if node is None:
                return 0
            else:

                # Compute the depth of each subtree
                left_depth = helper_function_get_height(node.left)
                right_depth = helper_function_get_height(node.right)

                # Use the larger one
                if left_depth > right_depth:
                    return left_depth + 1
                else:
                    return right_depth + 1

        self.height = helper_function_get_height(self.root)


