import numpy as np

from fitnesseval.nn_fitness_evaluator import NNFitnessEvaluator


class EvaluateStateOfTheArt:
    def evaluate_state_of_the_art(self):
        print("State of the Art Model: ")
        fitness_evaluator = NNFitnessEvaluator(None, self.state_of_the_art_config, self.data_dict)
        print(fitness_evaluator.model.summary())
        fitness_evaluator.train()
        fitness_evaluator.evaluate()

        self.state_of_the_art_testing_accuracy = fitness_evaluator.score[1]
        self.state_of_the_art_epoch_time = fitness_evaluator.times
        print("Testing Accuracy: ", self.state_of_the_art_testing_accuracy)
        avg_epoch_time = np.mean(self.state_of_the_art_epoch_time)
        print("Average Epoch Time: ", avg_epoch_time,
              "\n\n ###########################################################################")