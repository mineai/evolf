from evolutionary_algorithms.servicecommon.persistor.local.json.json_persistor import JsonPersistor
from evolutionary_algorithms.servicecommon.persistor.local.pickle.pickle_persistor import PicklePersistor
from evolutionary_algorithms.experimenthost.glo.utils.statistics import Statistics
from evolutionary_algorithms.experimenthost.glo.utils.visualize import Visualize

import os
import calendar
import time
import shutil


class EvolutionPersistor:

    def __init__(self, path):
        self.experiment_id = 0
        self.experiment_root_path = ""
        self.set_experiment_id()
        self.create_root_experiment_folder(path)

    def set_experiment_id(self):
        self.experiment_id = calendar.timegm(time.gmtime())

    def create_root_experiment_folder(self, path):
        self.experiment_root_path = f"{path}/glo_{self.experiment_id}"
        os.makedirs(self.experiment_root_path)

    def create_generation_folder(self, generation_idx):
        generation_path = f"{self.experiment_root_path}/Generation_{generation_idx}"
        os.mkdir(generation_path)
        candidate_path = f"{generation_path}/Candidates"
        os.mkdir(candidate_path)

    def create_tree_folder(self, tree_index, tree, generation_number, fitness):
        tree_path = f"{self.experiment_root_path}/Generation_{generation_number}/Candidates/Tree{tree_index}_{fitness}"
        os.mkdir(tree_path)

        # This code only works when put before the json_persistence.
        # When you put it after, it only visualizes
        try:
            Visualize.visualize([tree], self.experiment_id, tree_path)
        except:
            print("Failed to Visualize Expression Tree")

        tree_stats = Statistics.statistics(tree)

        json_persistor = JsonPersistor("stats", tree_path)
        json_persistor.persist(tree_stats)

        try:
            self.plot_loss(tree.symbolic_expression, tree_path)
        except:
            print("Failed to Visualize Loss Function")

        # pickle_persistor = PicklePersistor("tree", tree_path)
        # pickle_persistor.persist(tree)

    def plot_loss(self, expression, path):
        from sympy.plotting import plot3d
        graph = plot3d(expression, show=False)
        graph.save(f"{path}/loss_function")

    def persist_best_candidate(self, best_candidate, generation_idx):
        best_candidate_path = f"{self.experiment_root_path}/Generation_{generation_idx}/Best_Candidate"
        os.mkdir(best_candidate_path)

        # This code only works when put before the json_persistence.
        # When you put it after, it only visualizes
        try:
            Visualize.visualize([tree], self.experiment_id, best_candidate_path)
        except:
            print("Failed to Visualize Expression Tree")

        tree_stats = Statistics.statistics(best_candidate)
        
        json_persistor = JsonPersistor("stats", best_candidate_path)
        json_persistor.persist(tree_stats)

        try:
            self.plot_loss(best_candidate.symbolic_expression, best_candidate_path)
        except:
            print("Failed to Visualize Loss Function")


