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
        expression = None
        stack = []

        for node in tree.nodes:
            function_type = node.operator_type
            if function_type == "R":
                continue
            elif function_type == "L":
                stack.append(node.coefficient * node.symbolic_handle)
            elif function_type == "U":
                last_literal = stack.pop()
                expression = node.coefficient * node.symbolic_handle(last_literal)
                stack.append(expression)
            elif function_type == "B":
                last_two_literals = [stack.pop(), stack.pop()]
                expression = node.coefficient * node.symbolic_handle(last_two_literals[0], last_two_literals[1])
                stack.append(expression)

        return expression
