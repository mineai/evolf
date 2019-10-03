from evolutionary_algorithms.experimenthost.glo.population import Population
from evolutionary_algorithms.servicecommon.persistor.local.json.json_persistor \
            import JsonPersistor
from evolutionary_algorithms.servicecommon.persistor.local.pickle.pickle_persistor \
import PicklePersistor
from evolutionary_algorithms.experimenthost.glo.function_library import FunctionLibrary


import os
import time
import calendar

class TestGLO:
    @staticmethod
    def run():
        population = Population(3,10,100)
        tree_list = population.generate_tree_list()
        population.print_tree_list(tree_list,"id")
        TestGLO().persist(tree_list, population)
        function_sample = FunctionLibrary().sample("B")
        print('function sample: ',function_sample["B"])


    @staticmethod
    def persist(trees, population_obj):
        experiment_id = calendar.timegm(time.gmtime())

        print(f"To refer to this test Experiment, the ID is: {experiment_id}")

        base_dir = f"{os.getcwd()}/results/glo_test_{experiment_id}/candidates"

        os.makedirs(base_dir)

        for tree_idx, tree in enumerate(trees):
            candidate_path = f"{base_dir}/tree_{tree_idx}"
            os.makedirs(candidate_path)
            stats = population_obj.statistics(tree)

            json_persistor = JsonPersistor("stats", candidate_path)
            json_persistor.persist(stats)

            pickle_persistor = PicklePersistor("tree", candidate_path)
            pickle_persistor.persist(tree)



TestGLO().run()