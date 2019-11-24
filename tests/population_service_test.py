import requests
import pickle

from framework.serialize.population.population_serializer import PopulationSerializer
from search_space.populate_search_space import PopulateSearchSpace
from search_space.search_space import SearchSpace

search_space = {

        "U": {
            "log": 4
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


}

pickled_search_space = pickle.dumps(search_space)

# Initialize Search Space
url = "http://127.0.0.1:5000/init"
response = requests.post(url=url, data=pickled_search_space)

# Request initial Population
url = "http://127.0.0.1:5000/request_inital_population"

population_config = {
    "min_height": 3,
    "max_height": 5,
    "population_size": 100
}

population_config_bytes = pickle.dumps(population_config)
response = requests.post(url=url, data=population_config_bytes)
population_bytes = response._content
deserialized_population = pickle.loads(population_bytes)

search_space_obj = SearchSpace()
search_space_obj = PopulateSearchSpace.populate_search_space(search_space_obj,
                                                                 search_space)
population_deserializer = PopulationSerializer(deserialized_population, search_space_obj)
pop_obj = population_deserializer.deserialize()


[print(tree.symbolic_expression) for tree in pop_obj.trees]