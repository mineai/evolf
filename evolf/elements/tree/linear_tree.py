class LinearTree:

    def __init__(self, root):
        self.nodes = []  # Consists of all the nodes in a pre-order traversal manner.
        # The symbolic expression of the tree (the formula this tree represents)
        self.root = root

    def linearize_tree(self):
        if len(self.nodes):
            self.nodes = []

        def helper_function_generate_nodes(start, traversal=[]):
            # Root -> Left -> Right
            if start:
                traversal.append(start)
                if start.left:
                    start.left.parent = start
                if start.right:
                    start.right.parent = start
                traversal = helper_function_generate_nodes(start.left, traversal)
                traversal = helper_function_generate_nodes(start.right, traversal)
            return traversal

        self.nodes = helper_function_generate_nodes(self.root)[::-1]