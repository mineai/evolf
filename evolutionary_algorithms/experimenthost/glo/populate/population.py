from evolutionary_algorithms.experimenthost.glo.elements.tree \
    import Tree



class Population:
    def __init__(self, min_height=3, max_height=10, population_size=25):
        self.min_height = min_height
        self.max_height = max_height
        self.population_size = population_size

        self.trees = []
        self.working_trees = []

    def generate_trees(self):
        """

        This function uses the class variable population_size that 
        will specify the size of the list of trees that the function 
        will generate. It appends a specified number of Tree() objects 
        to tree_list then iterates through them again to create the 
        populated trees. The function then returns that list.

        arguments: Nothing
        returns: tree_list (list of Tree() objects)

        """

        while len(self.trees) < self.population_size:
            self.trees.append(Tree(self.min_height, self.max_height))

        for tree in self.trees:
            token = tree.request_token()
            tree.root = tree.helper_function(token)

    def get_working_trees(self):

        for tree in self.trees:
            if tree.symbolic_expression is None:
                tree.construct_symbolic_expression()
            if tree.working is None:
                tree.validate_working()

            if tree.working:
                self.working_trees.append(tree)


