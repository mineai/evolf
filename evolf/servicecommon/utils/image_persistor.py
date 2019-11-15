class ImagePersistor:
    """
    class variables:
        - linearized_tree: A list containing the nodes from a tree in level order.

        - search_space_dictionary: A dictionary that contains a key named "search_space"

        - search_space_operators: A list of all operators from the search space dictionary
        excluding root (R) operator types.

        - fitness: Holds the fitness passed in on object creation so the fitness can be
        easily attributed to the resulting image.

    methods:
        - set_operators(): Extrapolates all of the search space operators from the
        dictionary and puts them in the list defined as search_space_operators

        - get_image(): returns a matrix of 1's and 0's that represents the tree with
        respect to the defined search space.

        - get_image_row(index): returns a list containing 0's corresponding to operators
        that the node doesn't contain and a 1 corresponding to the operator that it does
    """

    def __init__(self, linearized_tree, search_space_dictionary, fitness):
        self.linearized_tree = linearized_tree
        self.search_space_dictionary = search_space_dictionary
        self.fitness = fitness
        self.search_space_operators = []

    def set_operators(self):
        """

        Extrapolates all of the search space operators from the dictionary and
        puts them in the list defined as search_space_operators

        :return: None
        """

        all_operators = []
        ss_dictionary = self.search_space_dictionary.get("search_space")
        operator_types = ss_dictionary.keys()

        for key in operator_types:
            if key not in ['R']:
                operators = ss_dictionary.get(key).keys()
                for operator in operators:
                    all_operators.append(operator)

        self.search_space_operators = all_operators

    def get_image(self):
        """

        returns a matrix of 1's and 0's that represents the tree with respect
        to the defined search space.

        :return: tree_
        """

        tree_image = []

        self.set_operators()

        for node in self.linearized_treetree:
            if node in self.search_space_operators:
                tree_image.append(self.get_image_row(self.search_space_operators.index(node)))

        return tree_image

    def get_image_row(self, index):

        """

        returns a list containing 0's corresponding to operators that the node
        doesn't contain and a 1 corresponding to the operator that it does

        :param index:
        :return: row: array of 0's and a 1
        """

        row = []
        length = len(self.search_space_operators)

        for i in range(0, length):
            if i == index:
                row.append(1)
            else:
                row.append(0)

        return row
