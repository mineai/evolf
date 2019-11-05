import numpy as np
from tqdm import trange
from evolf.fitnesseval.nn_fitness_evaluator import NNFitnessEvaluator


class EvaluateGeneration:

    def evaluate_candidate(self, population, tree_idx):
        tree = population.trees[tree_idx]

        print(f" \n\n \t\t Loss Function: {tree.generate_printable_expression()} \n")

        evaluated_tree = self.is_tree_evaluated(population.trees[tree_idx])
        if evaluated_tree:
            print("This Tree has already been evaluated.")
            print("Status: ", evaluated_tree.working)
            print("Fitness: ", evaluated_tree.fitness)

            print(" \n\n ###########################################################################")
            return

        fitness_evaluator = NNFitnessEvaluator(tree, self.evaluator_specs, self.data_dict)

        if tree.working:
            fitness_evaluator.train()
            fitness_evaluator.evaluate()

            tree.fitness = fitness_evaluator.score[1]
            print("Tree Fitness", tree.fitness)

            tree.avg_epoch_time = np.mean(fitness_evaluator.times)
            print("Average Epoch Time: ", tree.avg_epoch_time,
                  "\n\n ###########################################################################")

            # Create tree_<index>_fitness folder at output_path
            self.persistor_obj.create_tree_folder(self.current_tree, tree, self.generation_number,
                                                  tree.fitness, self.persist_status,
                                                  self.visualize_tree_status, self.visualize_function_status)

            self.current_tree += 1

        else:
            tree.fitness = 0
            print("This tree failed while training",
                  "\n\n ###########################################################################")
        self.global_cache.append(tree)

    def is_tree_evaluated(self, tree):
        for evaluated_tree in self.global_cache:
            if tree.symbolic_expression == evaluated_tree.symbolic_expression:
                return evaluated_tree
        return False

    def evaluate_current_generation(self, population):

        best_candidate_this_gen = population.trees[0]

        print("############# Starting Evaluation ################## \n\n")
        self.persistor_obj.create_generation_folder(self.generation_number)

        for tree_idx in trange(len(population.trees)):
            tree = population.trees[tree_idx]
            self.evaluate_candidate(population, tree_idx)
            if best_candidate_this_gen < tree:
                best_candidate_this_gen = tree

            print(f"\nBest Running in this Generation: {best_candidate_this_gen.generate_printable_expression()}, "
                  f"with fitness {best_candidate_this_gen.fitness}")
            print(f"\nBest Candidate Ever: {self.best_candidate_ever.generate_printable_expression()}, "
                  f"with fitness {self.best_candidate_ever.fitness}")

            print(f"State of the art Performance {self.state_of_the_art_testing_accuracy}")

            if self.best_candidate_ever < tree:
                self.best_candidate_ever = tree


        return population
