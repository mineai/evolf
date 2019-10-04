import os
import time
import calendar

from evolutionary_algorithms.experimenthost.glo.population import Population
from evolutionary_algorithms.servicecommon.persistor.local.json.json_persistor \
            import JsonPersistor
from evolutionary_algorithms.servicecommon.persistor.local.pickle.pickle_persistor \
import PicklePersistor
from evolutionary_algorithms.experimenthost.glo.function_library import FunctionLibrary
from evolutionary_algorithms.experimenthost.glo.tree_utils \
    import TreeUtils
from evolutionary_algorithms.experimenthost.glo.visualize \
    import Visualize

from evolutionary_algorithms.experimenthost.glo.statistics import Statistics

class TestGLO:
    @staticmethod
    def run():
        population = Population(4, 4, 100)
        tree_list = population.generate_tree_list()
        TestGLO.print_tree_list(tree_list, "data")
        TestGLO().persist(tree_list, population)


    @staticmethod
    def persist(trees, population_obj):
        experiment_id = calendar.timegm(time.gmtime())

        print(f"To refer to this test Experiment, the ID is: {experiment_id}")

        base_dir = f"{os.getcwd()}/results/glo_test_{experiment_id}/candidates"

        os.makedirs(base_dir)

        for tree_idx, tree in enumerate(trees):
            candidate_path = f"{base_dir}/tree_{tree_idx}"
            os.makedirs(candidate_path)
            stats = Statistics.statistics(tree)

            json_persistor = JsonPersistor("stats", candidate_path)
            json_persistor.persist(stats)

            pickle_persistor = PicklePersistor("tree", candidate_path)
            pickle_persistor.persist(tree)


    @staticmethod
    def print_tree_list(tree_list, output_type):
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
                     "operator_type", and "node_id"

        returns: Nothing
        """
        index = 1
        bad_tree_count = 0
        for tree in tree_list:
            print('Tree #' + str(index))
            if tree.binary_count < 1:
                print('Bad Tree! Not enough binary operators.')
                bad_tree_count += 1
            if tree.literal_count < 2:
                print('Bad Tree! Not enough Literals.')
                bad_tree_count += 1

            print(Visualize.visualize_function(tree))

            print(Visualize.print_tree(tree, tree.root, output_type))
            index += 1

        print(str(bad_tree_count) + ' out of ' + str(len(tree_list)) + ' trees were bad.')





TestGLO().run()