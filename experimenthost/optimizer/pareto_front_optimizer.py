import numpy as np


class ParetoFrontOptimizer:
    """
    This class is Evolfy way of optimizing between N
    feasible solutions in a D-dimensional space using a Pareto Front.
    """

    def __init__(self, fitness_objectives, evaluated_candidates):
        """
        The constructor initializes the class variables
        :param fitness_objectives:
        :param evaluated_candidates:
        """
        self.fitness_objectives = fitness_objectives
        self.evaluated_candidates = evaluated_candidates

    def extract_candidate_data(self):
        candidate_data = []
        for candidate in self.evaluated_candidates:
            candidate_info = []
            candidate_metrics = list(candidate.values())[0]
            for metric in candidate_metrics:
                candidate_info.append(candidate_metrics.get(metric))

            candidate_data.append(candidate_info)

        return candidate_data

    def set_evaluated_candidates(self, evaluated_candidates):
        self.evaluated_candidates = evaluated_candidates

    def select_candidate_from_indices(self, indices):
        candidates = []
        for candidate_idx in indices:
            candidates.append(self.evaluated_candidates[candidate_idx])

        return candidates

    def construct_dominant_pareto_front(self):

        points = self.extract_candidate_data()
        candidate_indices = []

        if isinstance(points, list):
            points = np.array(points)

        # Sort on first dimension
        if points.ndim == 1:
            candidate_indices.append(np.argmax(points))
        else:
            points = points[points[:, 0].argsort()]
            # Add first row to pareto_frontier
            pareto_frontier = points[0:1, :]
            # Test next row against the last row in pareto_frontier
            for candidate_num, row in enumerate(points[1:, :]):
                if sum([row[x] >= pareto_frontier[-1][x]
                        for x in range(len(row))]) == len(row):
                    # If it is better on all features add the row to pareto_frontier
                    pareto_frontier = np.concatenate((pareto_frontier, [row]))
                    candidate_indices.append(candidate_num)

        pareto_frontier = self.select_candidate_from_indices(candidate_indices)

        return pareto_frontier
