import os
import numpy as np

from experimenthost.optimizer.optimizer import Optimizer

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

from experimenthost.tasks.candidate_evaluator_task import CandidateEvaluatorTask
from framework.domain.get_default_config import GetDefaultConfig
from framework.population.population import Population
from searchspace.populate_search_space import PopulateSearchSpace
from searchspace.search_space import SearchSpace


class GenerationEvaluatorTask:

    def __init__(self, generation_number, candidates,
                 evaluator_config):
        """
        This constructor initializes the class variables needed
        and the Candidate Evaluator task number.
        :param generation_number: The Generation number
        :param candidates: A list containing the candidates to evaluated.
        :param evaluator_config: Config for the evaluator
        """

        self.generation_number = generation_number
        self.candidates = candidates

        self.candidate_evaluator_task = CandidateEvaluatorTask(evaluator_config)

        # Get the fitness objectives
        self.fitness_objectives = evaluator_config.get("fitness_objectives")

        # Get optimizer config
        self.num_best_candidates = evaluator_config.get("num_best_candidates", 5)
        self.optimization_method = evaluator_config.get("optimization_method", "pareto")

    def evaluate_generation(self):
        evaluated_candidates = []
        failed_candidates = []

        for candidate in self.candidates:
            metrics = self.candidate_evaluator_task.evaluate_candidate(candidate,
                                                                       full_training=False)

            if "error" in metrics.keys():
                failed_candidates.append({
                    candidate: metrics["error"]
                })
            elif np.isnan(list(metrics.values())).any():
                failed_candidates.append({
                    candidate: "Nan Loss function"
                })
            else:
                evaluated_candidates.append({
                    candidate: metrics
                })

        return evaluated_candidates, failed_candidates

    def get_optimals(self):
        evaluated_candidates, failed_candidates = self.evaluate_generation()

        # Create the Optimizer Object
        optimizer = Optimizer(self.fitness_objectives,
                              evaluated_candidates,
                              self.optimization_method)
        optimal_solutions = optimizer.optimize_pareto(self.num_best_candidates)

        return optimal_solutions


search_space_obj = SearchSpace()
search_space = GetDefaultConfig.get_default_config().get("searchspace")
search_space_obj = PopulateSearchSpace.populate_search_space(search_space_obj, search_space)
population = Population(2, 4, 80, search_space_obj=search_space_obj)

evaluator_config = {
    # The following two paths are
    # written as packages relative to
    # the evolf folder.

    "evaluator_path": "domains/mnist/mnist_evaluator",
    "evaluator_classname": "MnistEvaluator",

    # This is the training config that
    # will be used by the client's evaluator
    "training_config": {
        "epochs": 2,
        "early_stopping": True,
        "verbose": True,
        "batch_size": 2000
    },

    # This is the config that will be used by client's
    # evaluator during full training.
    # Only configs that change from the training
    # need to be specified here.
    "full_training_config": {
        "epochs": 100,
        "early_stopping": False
    },

    #   Objectives to optimize that the
    #   clients evaluator will return.
    "fitness_objectives": {
        "test_acc": "maximize",
        # "loss": "minimize"
    },
    "num_best_candidates": 2,
    "optimization_method": "pareto front"
}
generation_num = 1
candidates = population.trees

gaet = GenerationEvaluatorTask(generation_num,
                               candidates,
                               evaluator_config)
optimal_solutions = gaet.get_optimals()

# print(f"Best Candidate: {optimal_solutions[0].symbolic_expression}")
print(optimal_solutions)
for idx, optimal_solution_front in enumerate(optimal_solutions):
    print(f"\nFront {idx}: ")
    if isinstance(optimal_solution_front, list):
        for solution in optimal_solution_front.keys():
            print(solution.symbolic_expression)
    else:
        optimal = list(optimal_solution_front.keys())[0]
        print(optimal.symbolic_expression)
