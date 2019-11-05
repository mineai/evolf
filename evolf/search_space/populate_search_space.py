from evolf.search_space.keras_search_space import KerasSearchSpace
from evolf.search_space.symbolic_search_space import SymbolicSearchSpace


class PopulateSearchSpace:
    @staticmethod
    def populate_search_space(search_space_obj, search_space):
        """
        Populate Function Library:
        This allows one to set the usable functions in a single function
        library for a set population. This is set based on user input
        from the hocon. For now the hocon loaction is hardcoded
        """

        for function_type in search_space:
            functions = search_space[function_type]
            for function in functions:
                search_space_obj.search_space[function] = {
                    "tensorflow_handle": KerasSearchSpace.keras_search_space[function],
                    "symbolic_handle": SymbolicSearchSpace.symbolic_search_space[function],
                    "probability": functions[function],
                    "type": function_type
                }
        return search_space_obj