from framework.lossconstructor.loss_funciton_constructor import LossFunctionConstructor
from servicecommon.utils.cosntruct_class_from_path import ConstructClassFromPath
from servicecommon.utils.overlayer import Overlayer


class CandidateEvaluatorTask:
    """
    This class is used in EVOLF to evaluate a tree
    candidate using the Client supplied scripts.
    """

    def __init__(self, evaluator_config):

        # Get the Evaluation Training and the Full Training Config
        self.training_config = evaluator_config.get("training_config")
        self.full_training_config = evaluator_config.get("full_training_config")

        # Overlay the full training config with the training config
        self.full_training_config = Overlayer.overlay_configs(self.training_config,
                                                              self.full_training_config)

        # Get the path of the client supplied evaluator
        evaluator_path = evaluator_config.get("evaluator_path")
        evaluator_classname = evaluator_config.get("evaluator_classname")

        # Load the Evaluator Class from the path
        EvaluatorClass = ConstructClassFromPath.construct(evaluator_path,
                                                               evaluator_classname)
        self.evaluator_obj = EvaluatorClass()

        # Get the Evaluator Model
        self.evaluator_model = self.evaluator_obj.build_evaluator_model()

        # Get the data dictionary
        self.data_dict = self.evaluator_obj.load_data()

        # Get the fitness objectives
        self.fitness_objectives = evaluator_config.get("fitness_objectives")

    def evaluate_candidate(self, candidate_tree, full_training=False):

        # Build candidate loss
        loss = LossFunctionConstructor.construct_loss(candidate_tree)

        # Log to stdout
        print(f"\n############ Loss Function: {candidate_tree.symbolic_expression} ##########")

        # Evaluate the tree and get the metrics
        if full_training:
            config = self.full_training_config
        else:
            config = self.training_config

        try:
            metrics = self.evaluator_obj.evaluate_loss(self.evaluator_model,
                                                       self.data_dict,
                                                       loss,
                                                       config)
        except Exception as e:
            metrics = {
                "error": e
            }

        if "error" not in metrics.keys():
            for objective in metrics.keys():
                if objective not in self.fitness_objectives.keys():
                    metrics.pop(objective, None)
            print(f"Metrics: {metrics}")

        return metrics










