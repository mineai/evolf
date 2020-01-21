import os
import psutil
import shutil
import yaml
import tqdm
import time

from experimenthost.optimizer.optimizer import Optimizer

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

from framework.domain.get_default_config import GetDefaultConfig
from framework.population.population import Population
from framework.serialize.tree.tree_serializer import TreeSerializer
from searchspace.populate_search_space import PopulateSearchSpace
from searchspace.search_space import SearchSpace
from servicecommon.persistor.local.json.json_persistor import JsonPersistor


class StudioCompletionService:

    def __init__(self, candidates, generation_number,
                 experiment_id, search_space, timeout=300,
                 evaluator_config=None,
                 studio_config=None):
        self.candidates = candidates
        self.generation_number = generation_number
        self.experiment_id = experiment_id
        self.search_space = search_space
        self.timeout = timeout
        self.evaluator_config = evaluator_config
        self.studio_config = studio_config

        # Set up Generation Folder
        self.unevaluated_generation_path, \
        self.evaluated_generation_path, self.studio_config_path, \
        self.evaluator_config_path, self.search_space_path = self.generate_temp_exp_folder()

        # Set up Search space
        self.search_space_obj = SearchSpace()
        self.search_space_obj = PopulateSearchSpace.populate_search_space(self.search_space_obj,
                                                                          self.search_space)

        # Number of sent and received messages
        self.msgs_sent, self.msgs_recvd = 0, 0

        # Keep track of processes in studios queue
        self.studio_process_queue = []

        # Keep track of successful vs failed candidates and best 'n' solutions for stats
        self.successful_candidates, self.failed_candidates = [], []
        self.best_solutions = []

        # Keep track of total Evaluation time
        self.generation_eval_time = None

    def generate_temp_exp_folder(self):
        current_path = os.getcwd()
        temp_exp_path = os.path.join(current_path, f"temp/{self.experiment_id}")

        if os.path.exists(temp_exp_path):
            shutil.rmtree(temp_exp_path)
        os.makedirs(temp_exp_path)

        # Save the Search Space
        search_space_path = temp_exp_path
        json_persistor = JsonPersistor(self.search_space, folder=search_space_path, base_file_name="search_space")
        json_persistor.persist()

        # Dump the Search Space as a YAML File
        studio_config_path = temp_exp_path
        studio_config_path = os.path.join(studio_config_path, "studio_config.yaml")
        with open(studio_config_path, 'w') as outfile:
            yaml.dump(self.studio_config, outfile, default_flow_style=False)

        # Dump the evaluator config
        evaluator_config_path = temp_exp_path
        json_persistor = JsonPersistor(self.evaluator_config,
                                       folder=evaluator_config_path,
                                       base_file_name="evaluator_config")
        json_persistor.persist()

        # Creat Generation folder
        unevaluated_generation_path = os.path.join(temp_exp_path, f"unevaluated/{self.generation_number}")
        evaluated_generation_path = os.path.join(temp_exp_path, f"evaluated/{self.generation_number}")

        if not os.path.exists(unevaluated_generation_path):
            os.makedirs(unevaluated_generation_path)

        if not os.path.exists(evaluated_generation_path):
            os.makedirs(evaluated_generation_path)

        return unevaluated_generation_path, evaluated_generation_path, studio_config_path, \
               evaluator_config_path, search_space_path

    def kill(self, proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()

    def submit_jobs_with_data(self):

        print("\nSubmitting Jobs to Studio ML\n")
        # Loop over the Candidates
        for candidate_idx in tqdm.trange(len(self.candidates)):
            # Get the Candidate
            candidate = self.candidates[candidate_idx]

            # Serialize the Candidate
            candidate_serializer = TreeSerializer(candidate, self.search_space_obj)
            serialized_candidate = candidate_serializer.serialize()

            # Save The Serialized Candidate
            candidate_persistor = JsonPersistor(dict=serialized_candidate,
                                                folder=self.unevaluated_generation_path,
                                                base_file_name=str(candidate.id))
            candidate_persistor.persist()

            # Submit JOB using studio
            # Create the paths here without using the JSON Extensions
            candidate_location = os.path.join(self.unevaluated_generation_path, str(candidate.id))
            evaluator_config = os.path.join(self.evaluator_config_path, "evaluator_config")
            search_space = os.path.join(self.search_space_path, "search_space")

            # To Use the JSON Persistor the candidate_evaluator_task should seperate the folder from the file
            import subprocess
            command = f"exec studio run --config={self.studio_config_path} --force-git experimenthost/tasks/candidate_evaluator_task.py " \
                      f"--candidate_location={candidate_location} --evaluator_config={evaluator_config} " \
                      f"--search_space_location={search_space} --generation_number={self.generation_number} --experiment_id={self.experiment_id}"
            # command = command.split(" ")
            process = subprocess.Popen(command, shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.studio_process_queue.append(process)
            self.msgs_sent += 1

    def wait_for_evaluations(self):

        print("\nWaiting for results to return from Studio ML")

        time_elapsed = 0

        # Wait for results
        msgs_recvd_last = self.msgs_recvd
        with tqdm.tqdm(total=self.msgs_sent, desc="Number of Candidates Rcvd") as recvd_bar:
            with tqdm.tqdm(total=self.timeout, desc="Timeout") as timeout_bar:

                while self.msgs_recvd < self.msgs_sent:
                    self.msgs_recvd = len(os.listdir(self.evaluated_generation_path))

                    if self.msgs_recvd > msgs_recvd_last:
                        recvd_bar.update(self.msgs_recvd)
                        msgs_recvd_last = self.msgs_recvd

                    time.sleep(10)
                    time_elapsed += 10
                    timeout_bar.update(10)

                    # Clear Queue
                    if time_elapsed >= self.timeout:
                        print("Timeout Occurred")

                        for process in self.studio_process_queue:
                            self.kill(process.pid)

                        break

        # Read all the evaluated candidates
        successful_candidates, failed_candidates = [], []
        candidates = os.listdir(self.evaluated_generation_path)
        for candidate in candidates:
            candidate_without_extension = os.path.splitext(candidate)[0]
            candidate_restorer = JsonPersistor(dict=None,
                                               base_file_name=candidate_without_extension,
                                               folder=self.evaluated_generation_path)
            restored_candidate = candidate_restorer.restore()

            candidate_deserializer = TreeSerializer(restored_candidate, search_space_obj)
            deserialized_evaluated_candidate = candidate_deserializer.deserialize()

            if "error" in deserialized_evaluated_candidate.metrics:
                failed_candidates.append(deserialized_evaluated_candidate)
            else:
                successful_candidates.append(deserialized_evaluated_candidate)

        return successful_candidates, failed_candidates

    def run(self):
        start_time = time.time()

        self.submit_jobs_with_data()
        self.successful_candidates, self.failed_candidates = self.wait_for_evaluations()

        end_time = time.time()
        self.generation_eval_time = end_time - start_time

        self.best_solutions = self.get_best_results()
        self.report_stats()

    def report_stats(self):
        print(f"\n\n ########### Generation Evaluation Stats ################")
        print(f"Stat reports for generation: {self.generation_number}")
        print(f"Generation Eval Time: {self.generation_eval_time} seconds")
        print(f"Num Candidates to be submitted: {len(self.candidates)}")

        print(f"\n Number of candidates submitted: {self.msgs_sent}")
        print(f"Number of candidates recvd: {self.msgs_recvd}")
        print(f"Submission Success rate: {self.msgs_recvd / self.msgs_sent * 100}%")

        print(f"Num Candidates Successfully Evaluated: {len(self.successful_candidates)}")
        print(f"Num Candidates failed: {len(self.failed_candidates)}")
        print(f"Evaluation Success Rate: {len(self.successful_candidates) / len(candidates) * 100}%")

        print(f"\n ############## Evaluated Candidate Metrics for this generation ##############")
        for candidate in self.successful_candidates:
            print(f"{candidate.symbolic_expression}: {candidate.metrics}")

        print(f"\n ############## Best Candidate Metrics for this generation ##############")
        for candidate in self.best_solutions:
            print(f"{candidate.symbolic_expression}: {candidate.metrics}")

    def get_best_results(self):

        fitness_objectives = self.evaluator_config.get("fitness_objectives")
        num_best_candidates = self.evaluator_config.get("num_best_candidates")

        optimizer = Optimizer(fitness_objectives, self.successful_candidates)
        best_solutions = optimizer.optimize_pareto(num_best_candidates)

        return best_solutions


search_space_obj = SearchSpace()
search_space = GetDefaultConfig.get_default_config().get("searchspace")
search_space_obj = PopulateSearchSpace.populate_search_space(search_space_obj, search_space)
population = Population(2, 4, 5, search_space_obj=search_space_obj)

evaluator_config = {
    # The following two paths are
    # written as packages relative to
    # the evolf folder.

    "evaluator_path": "domains/mnist/mnist_evaluator",
    "evaluator_classname": "MnistEvaluator",

    # This is the training config that
    # will be used by the client's evaluator
    "training_config": {
        "epochs": 1,
        "early_stopping": True,
        "verbose": True,
        "batch_size": 1000
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

# Studio Config
studio_config = {
    "database": {
        "type": "s3",
        "endpoint": "http://127.0.0.1:9000",
        "bucket": "mineai-mnist-database",
        "authentication": None,
    },
    "storage": {
        "type": "s3",
        "endpoint": "http://127.0.0.1:9000",
        "bucket": "mineai-mnist-storage",
    },
    "server": {
        "authentication": None,
    },
    "cloud": {
        "queue": {
            "rmq": "amqp://guest:guest@localhost:5672/%2f?connection_attempts=30&retry_delay=1&socket_timeout=15"
        }
    },
    "saveMetricsFrequency": "1m",
    "saveWorkspaceFrequency": "1m",
    # DATA: Studio and parts are a lot more chatty on the
    # experiment host side. Decrease verbosity for sanity.
    "verbose": "error",
    "resources_needed": {
        "cpus": 4,
        "ram": "4g",
        "hdd": "60g",
        "gpus": 0,
        "gpuMem": "5g"
    }
}

generation_num = 1
candidates = population.trees

sss = StudioCompletionService(candidates, generation_num,
                              "R124134", search_space, 5000, evaluator_config, studio_config)
sss.run()
