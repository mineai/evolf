import calendar
import os
import shutil
import time
import pydot


class Visualize:

    @staticmethod
    def print_tree(tree, current_node, head_type="operator_type", level=0):

        """
            
            Prints out the contents of a tree starting at the root node
            and working down to the leaves.

            Possibly add an argument in the future that can select specific
            values to be displayed from each node

            head_type allows the user to choose the what function_str is being printed
            from each node. At the moment, the only kinds of printable function_str are
            the operator_type (U, B, or, L), function_str (+, sin, y, etc.), and the node_id (1,2,3,...)

            head_type can be accessed from test_glo through population

            """
        ret = ""
        if current_node:
            num_tabs = '\t' * (tree.height - level)
            if head_type == "operator_type":
                ret = num_tabs + repr(current_node.operator_type) + '\n'
            elif head_type == "function_str":
                ret = num_tabs + repr(current_node.function_str) + '\n'
            elif head_type == "node_id":
                ret = num_tabs + repr(current_node.id) + '\n'
            ret += Visualize.print_tree(tree, current_node.right, head_type, level)
            level += 1
            ret += Visualize.print_tree(tree, current_node.left, head_type, level)
            level += 1
            return ret
        return ''

    @staticmethod
    def visualize(trees, experiment_id=None, path=None):
        if path is None:
            if experiment_id is None:
                experiment_id = calendar.timegm(time.gmtime())
            path = f"{os.getcwd()}/results/glo_test_{experiment_id}/trees"

        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        if not isinstance(trees, list):
            trees = [trees]
        for tree_idx, tree in enumerate(trees):
            nodes = tree.nodes
            print(f"Visualizing Tree {tree_idx}")
            graph = pydot.Dot(graph_type='digraph',
                              label=f"{tree.generate_printable_expression()}",
                              fontsize=16,
                              fontname='Roboto',
                              rankdir="TB",
                              ranksep=1)

            for node_idx, node in enumerate(nodes):
                label = node.function_str
                color = "green"
                if node.function_str in ["pos_scalar", "neg_scalar"]:
                    label = '%.3f'% node.symbolic_handle
                if node.operator_type == "U":
                    color = "#F5A286"
                elif node.operator_type == "B":
                    color = "#A8CFE7"
                elif node.operator_type == "L":
                    color = "#F7D7A8"
                elif node.operator_type == "R":
                    color = "red"
                # label = node.node_id
                node_obj = pydot.Node(node.node_id,
                                      label=f"{label}",
                                      xlabel="",
                                      xlp=5,
                                      orientation=0,
                                      height=1,
                                      width=1,
                                      fontsize=16,
                                      shape='circle',
                                      style='rounded, filled',
                                      color=color,
                                      fontcolor="black")
                graph.add_node(node_obj)

            for node in nodes:
                children = [node.left, node.right]
                for child in children:
                    if child is None:
                        continue
                    src = node
                    dst = child

                    edge = pydot.Edge(src.node_id, dst.node_id,
                                      color="grey",
                                      label=f"",
                                      fontcolor="#979ba1",
                                      fontsize=10)
                    graph.add_edge(edge)

            tree_path = f"{path}/{tree_idx}"
            print("This tree is located in: ", tree_path)
            graph.write_png(f"{tree_path}.png")
