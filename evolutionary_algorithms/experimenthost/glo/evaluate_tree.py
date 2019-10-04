from evolutionary_algorithms.experimenthost.glo.tree_utils \
    import TreeUtils

from evolutionary_algorithms.experimenthost.glo.function_library \
    import FunctionLibrary

class EvaluateTree:

    @staticmethod
    def build_function(tree):
        function_library_obj = FunctionLibrary()

        function_string = TreeUtils().traverse_tree(tree, "preorder")
        function = []
        for func_obj in function_string:
            function.append(function_library_obj.fetch_function_handle(func_obj))

        return function