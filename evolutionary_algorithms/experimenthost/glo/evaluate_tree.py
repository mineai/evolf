from evolutionary_algorithms.experimenthost.glo.tree_utils \
    import TreeUtils

from evolutionary_algorithms.experimenthost.glo.function_library \
    import FunctionLibrary

from sympy import *

class EvaluateTree:

    @classmethod
    def build_function_list(cls, tree):
        function_library_obj = FunctionLibrary()

        function_list = TreeUtils().traverse_tree(tree, "preorder")
        function_handle_list = []
        for func_obj in function_list:
            function_handle_list.append(function_library_obj.fetch_function_handle(func_obj))

        return function_list, function_handle_list

    def lambdadize(self, tree):
        stack = []

