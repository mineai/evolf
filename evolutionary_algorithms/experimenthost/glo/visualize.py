from evolutionary_algorithms.experimenthost.glo.tree \
    import Tree

class Visualize:
    def __init__(self, tree):
        self.tree = tree

    def print_tree(self, current_node, level=0):

            """
            
            Prints out the contents of a tree starting at the root node
            and working down to the leaves.

            """

            if current_node:
                num_tabs = '\t'*(self.tree.height - level)
                ret = num_tabs+repr(current_node.type)+'\n'
                ret += self.print_tree(current_node.right, level)
                level += 1
                ret += self.print_tree(current_node.left, level)
                level +=1
                return ret
            return ''