from evolutionary_algorithms.experimenthost.glo.tree \
    import Tree



class Population:
    def __init__(self, min_height=3, max_height=10, population_size=25):
        self.min_height = min_height
        self.max_height = max_height
        self.population_size = population_size

    def generate_tree_list(self):
        """

        This function uses the class variable population_size that 
        will specify the size of the list of trees that the function 
        will generate. It appends a specified number of Tree() objects 
        to tree_list then iterates through them again to create the 
        populated trees. The function then returns that list.

        arguments: Nothing
        returns: tree_list (list of Tree() objects)

        """
        tree_list = []

        while(len(tree_list) < self.population_size):
            tree_list.append(Tree(self.min_height,self.max_height))

        for tree in tree_list:
            token = tree.request_token()
            tree.root = tree.helper_function(token)

        return tree_list

