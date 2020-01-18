import numpy as np
from tqdm import trange

from fitnesseval.nn_fitness_evaluator import NNFitnessEvaluator


class EvaluateStateOfTheArt:

    def evaluate_state_of_the_art(self):
        print("State of the Art Model: ")

        run_accs = []
        for run in trange(self.average_over_num_runs):
            fitness_evaluator = NNFitnessEvaluator(None, self.state_of_the_art_config, self.data_dict)
            print(fitness_evaluator.model.summary())
            fitness_evaluator.train()
            fitness_evaluator.evaluate()

            state_of_the_art_testing_accuracy = fitness_evaluator.score[1]
            self.state_of_the_art_epoch_time = fitness_evaluator.times
            print(f"Testing Accuracy: ", state_of_the_art_testing_accuracy)
            run_accs.append(state_of_the_art_testing_accuracy)

        print(f"\nAverage Fitness over {self.average_over_num_runs} runs: {np.mean(run_accs)}")
        print(f"\nHighest Fitness over {self.average_over_num_runs} runs: {np.max(run_accs)}")
        self.state_of_the_art_testing_accuracy = np.max(run_accs)
        avg_epoch_time = np.mean(self.state_of_the_art_epoch_time)
        print("Average Epoch Time: ", avg_epoch_time,
              "\n\n ###########################################################################")
