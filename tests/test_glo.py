import os
import time
import calendar

from framework.population.population import Population
from servicecommon.persistor.local.json.json_persistor import JsonPersistor
from servicecommon.persistor.local.pickle.pickle_persistor import PicklePersistor
from servicecommon.utils.visualize \
    import Visualize

from servicecommon.utils.statistics import Statistics


class TestGLO:
    @staticmethod
    def run():
        population = Population(2, 4, 10)
        population.generate_population()
        population.get_working_trees()
        # TestGLO.print_tree_list(population.trees, "function_str")
        Visualize.visualize(population.trees)

        return population
        # TestGLO().persist(tree_list, population)

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
                     Examples of class variables that can be selected are "function_str",
                     "operator_type", and "node_id"

        returns: Nothing
        """
        bad_tree_count = 0
        for index, tree in enumerate(tree_list):
            tree.construct_symbolic_expression()
            tree.validate_working()

            print('Tree #' + str(index))
            if not tree.working:
                print('Bad Tree! Not enough Literals.')
                bad_tree_count += 1

            tree.generate_printable_expression()



            # print(Visualize.print_tree(tree, tree.root, output_type))

        print(str(bad_tree_count) + ' out of ' + str(len(tree_list)) + ' trees were bad.')


TestGLO().run()
