from flask import Flask, request
import pickle


from search_space.search_space import SearchSpace
from search_space.populate_search_space import PopulateSearchSpace
from framework.serialize.population.population_serializer import PopulationSerializer

from framework.population.population import Population

population_service_app = Flask(__name__)
search_space_obj = SearchSpace()

"""
Set Up Routes
"""


# 1) Set Up Search Space Object
@population_service_app.route("/init", methods=["POST"])
def set_up_search_space():
    global search_space_obj
    pickled_data = request.data
    search_space = pickle.loads(pickled_data)
    search_space_obj = PopulateSearchSpace.populate_search_space(search_space_obj,
                                                                 search_space)
    return 200

@population_service_app.route('/request_inital_population', methods=["POST"])
def generate_initial_population():

    # Get the Request Data
    pickled_data = request.data
    # Decode the byte-instream
    population_config = pickle.loads(pickled_data)
    # Get the Configurations
    min_height = population_config.get("min_height", 3)
    max_height = population_config.get("max_height", 5)
    population_size = population_config.get("population_size", 25)
    num_parents = population_config.get("num_parents", 2)
    mating_pool_multiplier = population_config.get("mating_pool_multiplier",
                                                   100)

    # Create a new population
    global search_space_obj
    population = Population(min_height, max_height, population_size,
                            num_parents, mating_pool_multiplier,
                            search_space_obj=search_space_obj)

    # Serialize Population
    population_serializer = PopulationSerializer(population,
                                                 search_space_obj)
    serialized_population = population_serializer.serialize()

    # Pickle The population
    serialized_population_bytes = pickle.dumps(serialized_population)

    return serialized_population_bytes

if __name__ == '__main__':
    population_service_app.run(host="127.0.0.1",
                               port=5000,
                               debug=True)
