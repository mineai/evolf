class ExternalFunctionInitializer():
	
	def initialize_fitness_function(self, kwargs, default_fitness_function):
		if "fitness_function" in list(kwargs):
			print("Using External Fitness Function")
			fitness_function = kwargs["fitness_function"]
		else:
			print("Using Default Fintess Function")
			fitness_function = default_fitness_function

		return fitness_function

	def initialize_crossover_function(self, kwargs, default_crossover_function):
		if "crosover_function" in list(kwargs):
    			print("Using Crossover Function Provided")
    			crosover_function = kwargs["crosover_function"]
		else:
			print("Using Default Crossover Function")
			crosover_function = default_crossover_function

		return crosover_function

	def initialize_mutation_function(self, kwargs, default_mutation_function):
		if "mutation_function" in list(kwargs):
			print("Using Mutation Function Provided")
			mutation_function = kwargs["mutation_function"]
		else:
			print("Using Default Mutation Function")
			mutation_function = default_mutation_function

		return mutation_function

	def initialize_generate_gene(self, default_generate_gene_function):
		if "generate_gene_function" in list(kwargs):
			print("Using External Generate Gene Function")
			gene_generator_function = kwargs["generate_gene_function"]
		else:
			print("Using Default Generate Gene Function")
			gene_generator_function = default_generate_gene_function

		return gene_generator_function
