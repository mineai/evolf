from evolf.servicecommon.persistor.local.json.json_persistor import JsonPersistor
from evolf.servicecommon.utils.statistics import Statistics
from evolf.servicecommon.utils.visualize import Visualize

import os
import calendar
import time
import csv
import matplotlib.pyplot as plt


class EvolutionPersistor:

    def __init__(self, path):
        self.experiment_id = 0
        self.experiment_root_path = ""
        self.set_experiment_id()
        self.create_root_experiment_folder(path)

    def set_experiment_id(self):
        self.experiment_id = calendar.timegm(time.gmtime())

    def create_root_experiment_folder(self, path):
        self.experiment_root_path = f"{path}/evolf_{self.experiment_id}"
        os.makedirs(self.experiment_root_path)
        print(f'Your Experiment ID is {self.experiment_id}')

    def create_generation_folder(self, generation_idx):
        generation_path = f"{self.experiment_root_path}/Generation_{generation_idx}"
        os.mkdir(generation_path)
        candidate_path = f"{generation_path}/Candidates"
        os.mkdir(candidate_path)

    def create_tree_folder(self, tree_index, tree, generation_number, fitness, persist_status, visualize_tree_status, visualize_function_status):
        tree_path = f"{self.experiment_root_path}/Generation_{generation_number}/Candidates/Tree{tree_index}_{fitness}"
        os.mkdir(tree_path)

        # This code only works when put before the json_persistence.
        # When you put it after, it only visualizes

        if visualize_tree_status:
            try:
                Visualize.visualize([tree], self.experiment_id, tree_path)
            except:
                print("Failed to Visualize Expression Tree")

        if persist_status:
            try:
                tree_stats = Statistics.statistics(tree)

                json_persistor = JsonPersistor("stats", tree_path)
                json_persistor.persist(tree_stats)
            except:
                print("Failed to Persist Tree Stats Into a JSON File")

        if visualize_function_status:
            try:
                self.plot_loss(tree.symbolic_expression, tree_path)
            except:
                print("Failed to Visualize Loss Function")

    def plot_loss(self, expression, path):
        from sympy.plotting import plot3d
        graph = plot3d(expression, show=False)
        graph.save(f"{path}/loss_function")
        plt.close("all")

    def persist_best_candidate(self, best_candidate, generation_idx, persist_status, visualize_tree_status, visualize_function_status):
        best_candidate_path = f"{self.experiment_root_path}/Generation_{generation_idx}/Best_Candidate"
        os.mkdir(best_candidate_path)

        # This code only works when put before the json_persistence.
        # When you put it after, it only visualizes
        if visualize_tree_status:
            try:
                Visualize.visualize([best_candidate], self.experiment_id, best_candidate_path)
            except:
                print("Failed to Visualize Expression Tree")

        if persist_status:
            try:
                tree_stats = Statistics.statistics(best_candidate)

                json_persistor = JsonPersistor("stats", best_candidate_path)
                json_persistor.persist(tree_stats)
            except:
                print("Failed to Persist Tree Stats Into a JSON File")

        if visualize_function_status:
            try:
                self.plot_loss(best_candidate.symbolic_expression, best_candidate_path)
            except:
                print("Failed to Visualize Loss Function")

        # set the file path and name for the csv file
        csv_file_name = f"{self.experiment_root_path}/Best_Trees.csv"

        # create an input list to write to the csv file
        csv_input = [str(generation_idx), best_candidate.generate_printable_expression(), str(best_candidate.fitness)]

        # if the file exists, append the next generation's best candidate to the end

        if os.path.exists(csv_file_name):
            with open(csv_file_name, 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(csv_input)
            writeFile.close()

        # if the file does not exist, create a new file and write to the first row

        else:
            with open(csv_file_name, 'w+') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(csv_input)
            writeFile.close()

    def create_fitness_plot(self, fitness_list, generation_idx, num_of_generations, file_name="plot.png", plot_title="my plot", x_axis_label="x axis", y_axis_label="y axis"):
        generation_list = []
        file_name = f"{self.experiment_root_path}/{file_name}"

        # create the list of generations that were completed
        generation_list = list(range(0, generation_idx+1))
        # for idx in range(0,generation_idx+1):
        #     generation_list.append(idx)
        plt.figure()
        plt.plot(generation_list, fitness_list, 'ro-')

        # label the points with the fitness
        for generation in generation_list:
            current_fitness = "%.3f"%fitness_list[generation]
            plt.annotate(f"{current_fitness}", (generation, fitness_list[generation]))

        plt.title(plot_title)
        plt.axis([0, num_of_generations, 0, 1])
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)

        plt.savefig(file_name)
        plt.close()


