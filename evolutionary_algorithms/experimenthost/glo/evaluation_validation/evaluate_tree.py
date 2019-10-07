from evolutionary_algorithms.experimenthost.glo.utils.tree_utils \
    import TreeUtils

from evolutionary_algorithms.experimenthost.glo.populate.function_library \
    import FunctionLibrary


class EvaluateTree:

    @classmethod
    def build_function_list(cls, tree):
        function_library_obj = FunctionLibrary()

        function_list = TreeUtils().traverse_tree(tree, "preorder")
        tensorflow_handle_list, symbolic_handle_list = [], []
        for func_obj in function_list:
            tensorflow_handle_list.append(function_library_obj.get_tensorflow_handle(func_obj))
            symbolic_handle_list.append(function_library_obj.get_symbolic_handle(func_obj))

        return function_list, tensorflow_handle_list, symbolic_handle_list

    @classmethod
    def build_symbolic_expression(cls, tree):

        function_list, _, symbolic_handle_list = cls.build_function_list(tree)

        root_label, root_function, expression = None, None, None
        stack = []

        function_library_obj = FunctionLibrary()

        for function, handle in zip(function_list, symbolic_handle_list):
            function_type = function_library_obj.get_function_type(function)

            if function_type == "R":
                root_function = handle
                root_label = function
            elif function_type == "L":
                stack.append(handle)
            elif function_type == "U":
                last_literal = stack.pop()
                expression = handle(last_literal)
                stack.append(expression)
            elif function_type == "B":
                last_two_literals = [stack.pop(), stack.pop()]
                expression = handle(last_two_literals[0], last_two_literals[1])
                stack.append(expression)

        return root_label, root_function, function_list, expression



    def lambdadize(self, tree):
        pass

