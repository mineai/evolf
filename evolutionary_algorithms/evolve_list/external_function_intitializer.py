from evolution_function_lib import EvolutionFunctionLib

class ExternalFunctionInitializer():
	def __init__(self):
		self.evolution_function_lib = EvolutionFunctionLib()

	def initialize_fitness_function(self, kwargs):
		if "fitness_function" in list(kwargs):
			print("Using External Fitness Function")
			fitness_function = kwargs["fitness_function"]
		else:
			print("Using Default Fintess Function")
			fitness_function = self.evolution_function_lib. \
                                default_fitness_function

		return fitness_function

	def initialize_crossover_function(self, kwargs):
		if "crosover_function" in list(kwargs):
    			print("Using Crossover Function Provided")
    			crosover_function = kwargs["crosover_function"]
		else:
			print("Using Default Crossover Function")
			crosover_function = self.evolution_function_lib. \
                                default_crossover_function

		return crosover_function

	def initialize_mutation_function(self, kwargs):
		if "mutation_function" in list(kwargs):
			print("Using Mutation Function Provided")
			mutation_function = kwargs["mutation_function"]
		else:
			print("Using Default Mutation Function")
			mutation_function = self.evolution_function_lib. \
                                    default_mutation_function

		return mutation_function


a = ExternalFunctionInitializer()
