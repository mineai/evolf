from evolutionary_algorithms.experimenthost.glo.utils.tree_utils \
    import TreeUtils

from evolutionary_algorithms.experimenthost.glo.populate.function_library \
    import FunctionLibrary


class EvaluateTree:
    """
    This class provides functions to evaluate and build the
    expression in the Trees.
    """

    @classmethod
    def build_function_list(cls, tree):
        """
        This function goes over the node types in the trees
        and collects their symbolic and tensorflow equivalent function
        from the Fitness Library. This function is never called on its own,
        it is just a helper function to build_symbolic_expression() in this class.
        :param tree: object of class Tree
        :return function_list: List containing all the functions
        :return tensorflow_handle_list: List containing the tensorflow equivalent
        function handles of the function_list
        :return symbolic_handle_list: List containing the symbolic equivalent function
        handles of the function_list
        """
        function_list = TreeUtils().traverse_tree(tree, "preorder")
        tensorflow_handle_list, symbolic_handle_list = [], []
        for func_obj in function_list:
            tensorflow_handle_list.append(FunctionLibrary.get_tensorflow_handle(func_obj))
            symbolic_handle_list.append(FunctionLibrary.get_symbolic_handle(func_obj))

        return function_list, tensorflow_handle_list, symbolic_handle_list

    @classmethod
    def build_symbolic_expression(cls, tree):
        """
        This function builds the symbolic expression that can be
        validated and evaluated with some numpy input.
        :param tree: object of class Tree
        :return function_list: List containing all the functions
        :return tensorflow_handle_list: List containing the tensorflow equivalent
        function handles of the function_list
        :return expression: The Sympy expression constructed. This function contains an
        expression that can be used with any numpy input.
        """
        function_list, tensorflow_handle_list,  symbolic_handle_list = cls.build_function_list(tree)

        root_label, root_function, expression = None, None, None
        stack = []

        for function, handle in zip(function_list, symbolic_handle_list):
            function_type = FunctionLibrary.get_function_type(function)

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

        return function_list, tensorflow_handle_list, expression
