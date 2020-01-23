from flask import Flask, request
import pickle


from searchspace.search_space import SearchSpace
from searchspace.populate_search_space import PopulateSearchSpace
from framework.serialize.population.population_serializer import PopulationSerializer

from framework.population.population import Population

population_service_app = Flask(__name__)
search_space_obj = SearchSpace()

SERVICE_ENDPOINTS = {

    "persistence_service": {
        "initialize_search_space": "http://127.0.0.1:9001/initialize",  # POST
        "create_experiment_bucket": "http://127.0.0.1:9001/create-experiment-bucket",  # POST
        "persist_population": "http://127.0.0.1:9001/persist/population"
    }

}

"""
Set Up Routes
"""


# 1) Set Up Search Space Object
@population_service_app.route("/initialize", methods=["POST"])
def set_up_search_space():
    global search_space_obj
    pickled_data = request.data
    search_space = pickle.loads(pickled_data)
    search_space_obj = PopulateSearchSpace.populate_search_space(search_space_obj,
                                                                 search_space)
    return "True"


@population_service_app.route('/request_inital_population', methods=["POST"])
def generate_initial_population():

    # # Get the Request Data
    # pickled_data = request.data
    # # Decode the byte-instream
    # population_config = pickle.loads(pickled_data)

    # Get the Request Data
    job_info = request.json

    # Unpack the job_info dictionary
    population_config = job_info.get("evolution_config")
    visualization_config = job_info.get("visualization_config")

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
    # serialized_population_bytes = pickle.dumps(serialized_population)

    # Assemble a job info dictionary to send to the Persistence Microservice
    persistence_job_info = {}
    persistence_job_info['serialized_population'] = serialized_population
    persistence_job_info['visualization_config'] = visualization_config

    global SERVICE_ENDPOINTS

    # Send the Persistence Microservice the Serialized Population

    return serialized_population


if __name__ == '__main__':
    population_service_app.run(host="0.0.0.0",
                               port=5000,
                               debug=True)
