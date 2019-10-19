import calendar
import os, sys
import time
import numpy as np
from tqdm import trange
import multiprocessing
from multiprocessing import Pool

from evolutionary_algorithms.experimenthost.glo.populate.population import Population
from evolutionary_algorithms.experimenthost.glo.reproduction.mutation import Mutation
from evolutionary_algorithms.experimenthost.glo.utils.statistics import Statistics
from evolutionary_algorithms.servicecommon.persistor.local.json.json_persistor import JsonPersistor

from evolutionary_algorithms.experimenthost.glo.domains.mnist.generate_mnist_data import GenerateMnistData
from evolutionary_algorithms.experimenthost.glo.domains.mnist.network_constructor import NetworkConstructor
from evolutionary_algorithms.experimenthost.glo.domains.mnist.network_initializer import NetworkInitializer

class EvolveMnistLoss():

    def __init__(self):
        self.data = GenerateMnistData.get_data()
        self.input_shape = self.data[-1]

        self.experiment_id = calendar.timegm(time.gmtime())

        self.population = self.generatate_working_population()

        self.network_constructor = NetworkConstructor(self.input_shape)


    def generatate_working_population(self, min_height=2, max_height=2, pop_size=100):
        population = Population(min_height, max_height, pop_size)
        population.generate_population()
        population.get_working_trees()

        return population

    def evaluate_tree(self, tree):
        neural_network = NetworkInitializer(tree, self.data, self.network_constructor, epochs=1)
        print("\n########################################################\n")
        print(tree.generate_printable_expression())
        print("\n")
        compiled = neural_network.compile_model()
        if compiled:
            neural_network.train()
            neural_network.evaluate()

        if len(neural_network.score):
            tree.fitness = neural_network.score[1]
        tree.avg_epoch_time = np.mean(neural_network.times)

        if compiled:
            print(f"Fitness: {tree.fitness}")
            print(f"Avg_time: {tree.avg_epoch_time}")
            print("\n########################################################")


    def run(self):
        print(f"To refer to this test Experiment, the ID is: {self.experiment_id}")

        for tree_idx in trange(len(self.population.trees)):
            tree = self.population.trees[tree_idx]
            tree = Mutation.weighted_function_mutation(tree, 0.75)
            tree.reset_tree()

            if not tree.working:
                continue

            self.evaluate_tree(tree)



        print(f"\nTo refer to this test Experiment, the ID is: {self.experiment_id}")


evolve_mnist = EvolveMnistLoss()
evolve_mnist.run()
#
# fitness = []
# [fitness.append(x.fitness) for x in glo_obj.population.working_trees]
#
# if len(fitness):
#     best_fitness_candidate = np.argmax(filter(lambda x: x != None, fitness))
#     print("\n\n Best fitness was of Candidate: ", best_fitness_candidate)
# else:
#     print("All trees failed")
