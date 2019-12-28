import argparse
import os
import sys

sys.path.append(os.getcwd())
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

from framework.lossconstructor.loss_funciton_constructor import LossFunctionConstructor
from framework.serialize.tree.tree_serializer import TreeSerializer
from searchspace.populate_search_space import PopulateSearchSpace
from searchspace.search_space import SearchSpace
from servicecommon.persistor.local.json.json_persistor import JsonPersistor
from servicecommon.utils.cosntruct_class_from_path import ConstructClassFromPath
from servicecommon.utils.overlayer import Overlayer


class CandidateEvaluatorTask():
    """
    This class is used in EVOLF to evaluate a tree
    candidate using the Client supplied scripts.
    """

    def __init__(self, search_space_obj, generation, experiment_id, evaluator_config):

        self.search_space_obj = search_space_obj
        self.generation = generation
        self.experiment_id = experiment_id

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

        tree_serializer = TreeSerializer(candidate_tree, self.search_space_obj)
        serialized_tree = tree_serializer.serialize()

        serialized_tree.update({"metrics": metrics})
        serialized_tree.update({"generation_timestamp":
                                    self.generation})

        # Save the evaluated candidate to the file system
        filepath = os.getcwd()
        filepath = os.path.join(filepath, f"temp/{experiment_id}/evaluated/{self.generation}")
        evaluated_candidate_persistor = JsonPersistor(dict=serialized_tree,
                                                      base_file_name=f"{candidate_tree.id}",
                                                      folder=filepath)
        evaluated_candidate_persistor.persist()
        return serialized_tree


if __name__ == "__main__":
    # Argument Parser
    parser = argparse.ArgumentParser(description="This Script used to submit to use the client scripts to"
                                                 "evaluate a loss function")
    parser.add_argument("--generation_number",
                        help="Generation number of the candidate")
    parser.add_argument("--experiment_id",
                        help="Experiment if of this generation")
    parser.add_argument("--evaluator_config",
                        help="The Evaluator config Hocon Config file location")
    parser.add_argument("--candidate_location",
                        help="The Location of the candidate that has to be evaluated in a JSON format")
    parser.add_argument("--search_space_location",
                        help="The Location of the Pickled search space")
    args = parser.parse_args()

    # Read the Args
    evaluator_config_location = args.evaluator_config
    candidate_location = args.candidate_location
    search_space_location = args.search_space_location
    generation_number = int(args.generation_number)
    experiment_id = args.experiment_id

    # Clean the Args
    if evaluator_config_location[-1] == "/":
        evaluator_config_location = evaluator_config_location[:-1]
    if candidate_location[-1] == "/":
        candidate_location = candidate_location[:-1]
    if search_space_location[-1] == "/":
        search_space_location = search_space_location[:-1]

    # Separate out folder name and file name from args
    evaluator_config_folder = os.path.dirname(evaluator_config_location)
    evaluator_config_filename = os.path.basename(evaluator_config_location)

    candidate_folder = os.path.dirname(candidate_location)
    candidate_filename = os.path.basename(candidate_location)

    search_space_folder = os.path.dirname(search_space_location)
    search_space_filename = os.path.basename(search_space_location)

    # Restore the files
    evaluator_config_restorer = JsonPersistor(None, folder=evaluator_config_folder,
                                              base_file_name=evaluator_config_filename)
    evaluator_config = evaluator_config_restorer.restore()

    search_space_restorer = JsonPersistor(None, folder=search_space_folder,
                                          base_file_name=search_space_filename)
    search_space = search_space_restorer.restore()

    candidate_restorer = JsonPersistor(None, folder=candidate_folder,
                                       base_file_name=candidate_filename)
    candidate = candidate_restorer.restore()

    # Load the Search Space
    search_space_obj = SearchSpace()
    search_space_obj = PopulateSearchSpace.populate_search_space(search_space_obj,
                                                                 search_space)

    # Deserialize the Candidate
    candidate_deserializer = TreeSerializer(candidate, search_space_obj)
    deserialized_candidate = candidate_deserializer.deserialize()

    candidate_evaluator = CandidateEvaluatorTask(search_space_obj, generation_number, experiment_id, evaluator_config)
    evaluated_serialized_candidate = candidate_evaluator.evaluate_candidate(deserialized_candidate)
