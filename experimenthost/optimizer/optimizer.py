import copy

from experimenthost.optimizer.pareto_front_optimizer import ParetoFrontOptimizer


class Optimizer:
    """
    This class is used to Optimize the objectives
    and return a single fitness value.

    Public Enemy Number 1: This class is meant for
    multi-objective function optimization but as of
    now it optimizes only for one objective, which is just
    returned as passed in.
    """

    def __init__(self, objectives, evaluated_candidates, method="pareto_front"):
        self.objectives = objectives
        self.evaluated_candidates = evaluated_candidates

        if method.find("pareto") != -1:
            self.optimizer = ParetoFrontOptimizer(objectives,
                                                  evaluated_candidates)

    def get_index_from_candidate(self, candidate_obj):
        for idx, candidate in enumerate(self.evaluated_candidates):
            if candidate == candidate_obj:
                return idx

    def optimize_pareto(self, num_best_candidates):
        """
        This function should combine the objectives of the candidates
        and extract a few feasible candidate solution.
        :return best_solutions: A list containing the number
        of best candidates to be selected.
        """
        best_solutions = self.optimizer.construct_dominant_pareto_front()

        total_solutions = len(best_solutions)

        while total_solutions < num_best_candidates:
            new_candidates_for_pareto_front = copy.copy(self.evaluated_candidates)
            for best_solution in best_solutions:
                index_to_remove = self.get_index_from_candidate(best_solution)
                del new_candidates_for_pareto_front[index_to_remove]
            self.optimizer.set_evaluated_candidates(new_candidates_for_pareto_front)
            new_solutions = self.optimizer.construct_dominant_pareto_front()

            num_solutions_to_add = num_best_candidates - total_solutions
            best_solutions.append(new_solutions[:num_solutions_to_add])

            total_solutions += num_solutions_to_add

        best_solutions = best_solutions[:num_best_candidates]

        return best_solutions
