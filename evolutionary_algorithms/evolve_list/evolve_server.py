import math
from evolutionary_algorithms.evolve_list.population import Population
from evolutionary_algorithms.evolve_list.evolution_functions_lib_list import EvolutionFunctionLibList

class EvolveServer():

    def __init__(self, population_size, mutation_rate,
                num_of_generations,
                target, num_parents, **kwargs):

        if isinstance(target, str):
            target = list(target)

        self.target = target
        self.gene_length = len(self.target)
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_of_generations = num_of_generations
        self.num_parents = num_parents


        self.population_obj = Population(self.population_size,
                                        self.mutation_rate,
                                        self.target,
                                        **kwargs)
        print(self.population_obj)

        self.current_generation = 0

    def build_initial_population(self, pop_size, gene_length, population_object):
        return population_object.initialize_population(pop_size, gene_length,
                                                        population_object.dna)

    def generate_next_generation(self, pop_size, num_parents, mating_pool,
                                pop_obj, target, mutation_rate):
        next_gen = []
        for candidate_num in range(pop_size):
            parents = pop_obj.natural_selection(num_parents, mating_pool)
            child = pop_obj.dna.crosover_function(target, parents)
            child = pop_obj.dna.mutation_function(child, mutation_rate,
                                                        pop_obj.dna.gene_generator)
            next_gen.append(child)

        return next_gen

    def sort_population_by_fitness_desc(self, population, fitness):
        population = [x for _, x in sorted(zip(fitness, population))][::-1]
        return population

    def serve(self, target, num_of_generations, pop_size, gene_length,
            population_object, num_parents, mutation_rate, mating_pool_mutiplier,
            elitism):

        print("\n\n\n ########## Evolution Server Starting......")
        print("\n Initializing Population")
        population = self.build_initial_population(pop_size, gene_length,
                                                            population_object)
        population_fitness = population_object.calculate_fitness(
                                                        population,
                                                        population_object.target,
                                                        population_object.dna)

        best_candidate_info = population_object.get_best_fitness_candidate(population,
                                                                    population_fitness)

        best_candidate_fitness = list(best_candidate_info)[0]
        best_candidate = best_candidate_info[best_candidate_fitness]



        print("Best Candidate Initial Population: ",
            population_object.utils.get_dna_string_from_list(best_candidate))
        print("Best Candidate Fitness Initial Population: ",
            best_candidate_fitness)

        print("\n ########## Stating Evolvution for ", num_of_generations, " generations.....")

        elites = []
        elites_to_keep = math.floor(pop_size * elitism)
        for generation in range(1, num_of_generations + 1):
            print("\n ########## Generation: ", generation)

            mating_pool = population_object.generate_mating_pool(population,
                                                                population_fitness,
                                                                mating_pool_mutiplier)

            population = self.generate_next_generation(pop_size, num_parents,
                                                        mating_pool,
                                                        population_object,
                                                        target, mutation_rate)
            if elites:
                population[:elites_to_keep] = elites[:elites_to_keep]
            population_fitness = population_object.calculate_fitness(
                                                            population,
                                                            population_object.target,
                                                            population_object.dna)

            population_by_fitness_desc = self.sort_population_by_fitness_desc(population,
                                                                            population_fitness)

            elites = population_by_fitness_desc[:elites_to_keep]
            best_candidate_info = population_object.get_best_fitness_candidate(population,
                                                                        population_fitness)

            best_candidate_fitness = list(best_candidate_info)[0]
            best_candidate = best_candidate_info[best_candidate_fitness]
            print("Best Candidate: ",
                population_object.utils.get_dna_string_from_list(best_candidate))
            print("Best Candidate Fitness: ",
                best_candidate_fitness)


            if population_object.utils.get_dna_string_from_list(best_candidate) == target:
                break


population_size = 5000
mutation_rate = 0.02
num_of_generations = 10000
target = "Its Kwaffee and not Coffee. And its Workoot not Workout"
# target = "Near the beginning of his career, Einstein thought that Newtonian mechanics was no longer enough to reconcile the laws of classical mechanics with the laws of the electromagnetic field. This led him to develop his special theory of relativity during his time at the Swiss Patent Office in Bern (1902–1909). However, he realized that the principle of relativity could also be extended to gravitational fields, and he published a paper on general relativity in 1916 with his theory of gravitation. He continued to deal with problems of statistical mechanics and quantum theory, which led to his explanations of particle theory and the motion of molecules. He also investigated the thermal properties of light which laid the foundation of the photon theory of light. In 1917, he applied the general theory of relativity to model the structure of the universe"

# target = "Unicorn"
num_parents = 2
mating_pool_mutiplier = 10000
elitism = 0.01

efl = EvolutionFunctionLibList()
kwargs = {"fitness_function_not": efl.fitness_function_words}

evserver = EvolveServer(population_size, mutation_rate,
                        num_of_generations,
                        target, num_parents, **kwargs)

evserver.serve(target, num_of_generations, population_size,
                evserver.gene_length,
                evserver.population_obj, evserver.num_parents,
                evserver.mutation_rate, mating_pool_mutiplier, elitism)
