from evolutionary_algorithms.experimenthost.glo.tree \
    import Tree
from evolutionary_algorithms.experimenthost.glo.visualize \
    import Visualize


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

    def statistics(self, tree):
        
        stats = {
            "height": tree.height,
            "U": tree.unary_count,
            "B": tree.binary_count,
            "L":tree.literal_count
        }

        return stats
        


    def print_tree_list(self, tree_list, output_type):
        """

        This function prints out all of the trees from the list of trees passed
        in along with displaying a message if the tree doesn't meet certain criteria.

        Trees must have:
            - At least 1 Binary operator
            - At least 2 Literals

        tree_list: (list of Tree() objects) This is the list that the function
                   iterates through printing out the contents of each individual
                   Tree() object by calling the print_tree() function in the 
                   Visualize class.
        
        output_type: (string) This variable will specify what kind of class variable
                     from the Node() class will be printed when printing each tree.
                     Examples of class variables that can be selected are "data", 
                     "type", and "id"

        returns: Nothing



        """
        index = 1
        bad_tree_count = 0
        for tree in tree_list:
            print('Tree #'+str(index))
            if tree.binary_count < 1:
                print('Bad Tree! Not enough binary operators.')
                bad_tree_count += 1
            if tree.literal_count < 2:
                print('Bad Tree! Not enough Literals.')
                bad_tree_count += 1
            visualize = Visualize(tree)
            print(visualize.print_tree(tree.root, output_type))
            index += 1
        print(str(bad_tree_count)+' out of '+str(len(tree_list))+' trees were bad.')
