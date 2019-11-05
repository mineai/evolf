from keras_search_space import KerasSearchSpace
from symbolic_search_space import SymbolicSearchSpace


class Populatefl:
    @staticmethod
    def populate_function_library(cls, function_library, search_space):
        ''' Populate Function Library:
            This allows one to set the usable functions in a single function
            library for a set population. This is set based on user input
            from the hocon. For now the hocon loaction is hardcoded
        '''
        function_library.search_space = {}
        binarysp = search_space.get('binary')
        unarysp = search_space.get('unary')

        function = {}
        for k in unarysp:
            function[k] = [{"tenserflow_handle": KerasSearchSpace.keras_search_space[k],"symbolic_handle":SymbolicSearchSpace.symbolic_search_space[k],"probability":unarysp.get(k),"type":"U"}]
        for k in binarysp:
            try:
                function[k[1]] = [{"tenserflow_handle": KerasSearchSpace.keras_search_space[k[1]],"symbolic_handle":SymbolicSearchSpace.symbolic_search_space[k[1]],"probability":binaryysp.get(k),"type":"B"}]
            except:
                function[k] = [{"tenserflow_handle": KerasSearchSpace.keras_search_space[k],"symbolic_handle":SymbolicSearchSpace.symbolic_search_space[k],"probability":binarysp.get(k),"type":"B"}]
        function_library.search_space = function
