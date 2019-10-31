from evolf.elements.tree.tree import Tree
from evolf.evolution.evaluate_generation import EvaluateGeneration
from evolf.evolution.evaluate_state_of_the_art import EvaluateStateOfTheArt
from evolf.evolution.initialize_next_gen import InitializeNextGen
from evolf.fitnesseval.nn_fitness_evaluator import NNFitnessEvaluator
from evolf.populate.population import Population
from evolf.utils.evolution_persistor import EvolutionPersistor


class Evolve(EvaluateStateOfTheArt, EvaluateGeneration, InitializeNextGen):

    def __init__(self, config, data_dict, search_space_obj):
        # # Parse and initialize variables
        self.config = config
        self.evolution_specs = self.config.get("evolution_specs")
        self.visualization_specs = self.config.get("visualization_specs")
        self.domain_config = self.config.get("domain_config")
        self.evaluator_specs = self.domain_config.get("evaluator_specs")
        self.persistence_specs = self.config.get("persistence_specs")
        self.state_of_the_art_config = self.domain_config.get("state_of_the_art_config")

        self.initial_population_size = self.evolution_specs.get("initial_population_size")
        self.population_size = self.evolution_specs.get("population_size")
        self.mating_pool_multiplier = self.evolution_specs.get("mating_pool_multiplier")
        self.number_parents = self.evolution_specs.get("num_parents")
        self.num_of_generations = self.evolution_specs.get("num_of_generations")
        self.tree_min_height = self.evolution_specs.get("tree_min_height")
        self.tree_max_height = self.evolution_specs.get("tree_max_height")
        self.output_path = self.persistence_specs.get("output_path")
        self.persist_status = self.persistence_specs.get("persist")
        self.visualize_tree_status = self.visualization_specs.get("visualize_tree")
        self.visualize_function_status = self.visualization_specs.get("visualize_function")
        self.visualize_avg_fitness = self.visualization_specs.get("visualize_avg_fitness")
        self.visualize_best_fitness = self.visualization_specs.get("visualize_best_fitness")
        self.state_of_the_art_loss = self.state_of_the_art_config.get("loss")
        self.evaluate_state_of_the_art_flag = self.state_of_the_art_config.get("evaluate")

        self.data_dict = data_dict

        self.state_of_the_art_testing_accuracy = None
        self.state_of_the_art_epoch_time = None

        self.persistor_obj = EvolutionPersistor(self.output_path)
        self.generation_number = 0
        self.current_tree = 1

        self.global_cache = []
        self.best_candidate_ever = None

        self.avg_fitness_list = []
        self.best_fitness_list = []

        self.search_space_obj = search_space_obj

        EvaluateStateOfTheArt.__init__(self)
        EvaluateGeneration.__init__(self)
        InitializeNextGen.__init__(self, self.evolution_specs)

    def evolve(self):

        if self.evaluate_state_of_the_art_flag:
            print("\n\n ########################################### Evaluating State of the Art\n\n")
            self.evaluate_state_of_the_art()
            print("\n\n ###########################################################################")

        population = Population(self.tree_min_height,
                                self.tree_max_height,
                                self.initial_population_size,
                                self.number_parents,
                                self.mating_pool_multiplier, search_space_obj=self.search_space_obj)

        while not len(population.working_trees):
            population = Population(self.tree_min_height,
                                    self.tree_max_height,
                                    self.initial_population_size,
                                    self.number_parents,
                                    self.mating_pool_multiplier, search_space_obj=self.search_space_obj)

        self.best_candidate_ever = population.working_trees[0]

        for generation in range(self.num_of_generations):
            print(f"Starting Evolution for Generation {generation}")

            # print("Evaluator NN: ")
            # dummy_tree = Tree(2, 2, )
            # fitness_evaluator = NNFitnessEvaluator(dummy_tree, self.evaluator_specs, self.data_dict)
            # print(fitness_evaluator.model.summary())
            # del fitness_evaluator, dummy_tree

            if generation == 0:
                eval_all = True
            else:
                eval_all = False
            population = self.evaluate_current_generation(population, eval_all)

            best_candidate = population.get_best_fitness_candidate()
            if best_candidate:
                print(f"\nBest Candidate for Generation {generation}: {best_candidate.symbolic_expression} \n \
                             Fitness: {best_candidate.fitness} \n \
                             Average Epoch Time: {best_candidate.avg_epoch_time}")
                # Update the lists of average fitness and best fitness for each generation
                self.best_fitness_list.append(best_candidate.fitness)

                self.persistor_obj.persist_best_candidate(best_candidate, self.generation_number, self.persist_status,
                                                          self.visualize_tree_status, self.visualize_function_status)

                if self.visualize_best_fitness:
                    plot_file_name = "Best_Fitness_Plot.png"
                    plot_title = f"Best Fitness Over {self.generation_number + 1} Generations"
                    x_label = "Generations"
                    y_label = "Best Fitness"
                    self.persistor_obj.create_fitness_plot(self.best_fitness_list, self.generation_number,
                                                           self.num_of_generations, plot_file_name, plot_title, x_label,
                                                           y_label)

            average_fitness = population.get_average_fitness()
            self.avg_fitness_list.append(average_fitness)
            print(f"\n\n Population Average Fitness: {average_fitness}")
            print("\n ###############################################################################")
            if self.visualize_avg_fitness:
                plot_file_name = "Average_Fitness_Plot.png"
                plot_title = f"Average Fitness Over {self.generation_number + 1} Generations"
                x_label = "Generations"
                y_label = "Average Fitness"
                self.persistor_obj.create_fitness_plot(self.avg_fitness_list, self.generation_number,
                                                       self.num_of_generations, plot_file_name, plot_title, x_label,
                                                       y_label)

            print(
                "#################### Starting Reproduction And Initializing New Generation ######################## \n")
            population = self.initialize_next_gen(population)

            self.generation_number += 1
            self.current_tree = 1
