import calendar
import time


class ExperimentFiler:

    def __init__(self, experiment_id):
        if experiment_id is None:
            self.experiment_id = self.generate_experiment_id()
        else:
            self.experiment_id = experiment_id

    def get_experiment_id(self):
        return self.experiment_id

    def generate_experiment_id(self):
        experiment_id = calendar.timegm(time.gmtime())
        return experiment_id
