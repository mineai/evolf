from evolutionary_algorithms.experimenthost.glo.tree_utils \
    import TreeUtils

from evolutionary_algorithms.experimenthost.glo.function_library \
    import FunctionLibrary

class Visualize:

    @staticmethod
    def print_tree(tree, current_node, head_type="operator_type", level=0):

        """
            
            Prints out the contents of a tree starting at the root node
            and working down to the leaves.

            Possibly add an argument in the future that can select specific
            values to be displayed from each node

            head_type allows the user to choose the what data is being printed
            from each node. At the moment, the only kinds of printable data are
            the operator_type (U, B, or, L), data (+, sin, y, etc.), and the node_id (1,2,3,...)

            head_type can be accessed from test_glo through population

            """
        ret = ""
        if current_node:
            num_tabs = '\t' * (tree.height - level)
            if head_type == "operator_type":
                ret = num_tabs + repr(current_node.type) + '\n'
            elif head_type == "data":
                ret = num_tabs + repr(current_node.data) + '\n'
            elif head_type == "node_id":
                ret = num_tabs + repr(current_node.id) + '\n'
            ret += Visualize.print_tree(tree, current_node.right, head_type, level)
            level += 1
            ret += Visualize.print_tree(tree, current_node.left, head_type, level)
            level += 1
            return ret
        return ''

    @staticmethod
    def visualize_function(tree, reverse=True):
        func_str = TreeUtils().preorder_print(tree.root)
        if reverse:
            func = func_str.split(" ")[::-1]
        else:
            func = func_str.split(" ")
        func.remove('')
        return func

    @staticmethod
    def build_function(func):
        function_library_obj = FunctionLibrary()
        function = []
        for func_obj in func:
            function.append(function_library_obj.fetch_function_handle(func_obj))

        return function



