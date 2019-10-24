from evolutionary_algorithms.servicecommon.persistor.local.json.json_persistor import JsonPersistor
from evolutionary_algorithms.servicecommon.persistor.local.pickle.pickle_persistor import PicklePersistor
from evolutionary_algorithms.experimenthost.glo.utils.statistics import Statistics

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

    def create_tree_folder(self, tree_index, tree, generation_number):
        tree_path = f"{self.experiment_root_path}/Generation_{generation_number}/Candidates/Tree{tree_index}"
        os.mkdir(tree_path)

        tree_stats = Statistics.statistics(tree)

        json_persistor = JsonPersistor("stats", tree_path)
        json_persistor.persist(tree_stats)

        # pickle_persistor = PicklePersistor("tree", tree_path)
        # pickle_persistor.persist(tree)