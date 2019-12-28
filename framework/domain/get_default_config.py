class GetDefaultConfig:
    """
    This class holds a base default config for
    the SessionServer in EVOLF
    """

    @staticmethod
    def get_default_config():
        import os
        default_config = {
            "domain_config": {

                "domain": "Unnamed Domain",
                "model_config": {
                    "generate_model": True,
                    "model_path": f"{os.getcwd()}/evolf/domains/mnist/model",
                    "model_file_name": "mnist_model.json",
                    "weight_file_name": "mnist_model_weights.h5"
                },
                "data_config": {
                    "train_percentage": 0.9,
                    "validation_percentage": 0.05,
                    "test_percentage": 0.05
                },
            },

            "evaluator_config": {
                "epochs": 3,
                "verbose": True,
                "batch_size": 128,
                "model_path": f"{os.getcwd()}/evolf/domains/mnist/model",
                "model_file_name": "mnist_model.json",
                "weight_file_name": "mnist_model_weights.h5",

                "early_stopping_config": {
                    "monitor": "val_acc",
                    "mode": "max",
                    "print_early_stopping": True,
                    "patience": 1,
                    "min_delta": 1
                },

                "switch_threshold": 0.9796
            },

            "state_of_the_art_config": {
                "evaluate": False,
                "epochs": 10,
                "verbose": True,
                "batch_size": 128,
                "model_path": f"{os.getcwd()}/evolf/domains/mnist/model",
                "model_file_name": "mnist_model.json",
                "weight_file_name": "mnist_model_weights.h5",
                "loss": "categorical_crossentropy",
                "early_stopping_config": {
                    "monitor": "val_acc",
                    "mode": "max",
                    "print_early_stopping": True,
                    "patience": 10,
                    "min_delta": 1
                }
            },
            "searchspace": {
                "U": {
                    "log": 10,
                    "square": 3,
                    "sqrt": 3
                },
                "B": {
                    "+": 1,
                    "-": 1,
                    "*": 1,
                    "/": 1
                },
                "L": {
                    "y": 3,
                    "t": 3,
                    "pos_scalar": 1,
                    "neg_scalar": 1
                },
                "R": {
                    "mean": 1
                }
            },

            "evolution_config": {
                "initial_population_size": 100,
                "population_size": 20,
                "mating_pool_multiplier": 100,
                "num_parents": 2,
                "weighted_function_mutation_rate": 0.05,
                "mutate_value_literal_nodes_rate": 0.025,
                "mutate_leaf_node_rate": 0.025,
                "shrink_mutation_rate": 0.25,
                "hoist_mutation_rate": 0.25,
                "literal_swap_mutation_rate": 1.0,
                "elitism": 0.1,
                "num_of_generations": 50,
                "tree_min_height": 2,
                "tree_max_height": 3
            },

            "visualization_config": {
                "visualize_tree": True,
                "visualize_function": True,
                "visualize_avg_fitness": True,
                "visualize_best_fitness": True

            },

            "persistence_config": {
                "output_path": f"{os.getcwd()}/evolf/domains/mnist/results",
                "persist": True
            },

        }

        return default_config
