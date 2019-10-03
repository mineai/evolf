from evolutionary_algorithms.experimenthost.glo.tree \
    import Tree

class Visualize:
    def __init__(self, tree):
        self.tree = tree

    def print_tree(self, current_node, head_type="type", level=0):

            """
            
            Prints out the contents of a tree starting at the root node
            and working down to the leaves.

            Possibly add an argument in the future that can select specific
            values to be displayed from each node

            head_type allows the user to choose the what data is being printed
            from each node. At the moment, the only kinds of printable data are
            the type (U, B, or, L), data (+, sin, y, etc.), and the id (1,2,3,...)

            head_type can be accessed from test_glo through population

            """
            ret = ""
            if current_node:
                
                num_tabs = '\t'*(self.tree.height - level)
                if head_type == "type":
                    ret = num_tabs+repr(current_node.type)+'\n'
                elif head_type == "data":
                    ret = num_tabs+repr(current_node.data)+'\n'
                elif head_type == "id":
                    ret = num_tabs+repr(current_node.id)+'\n'
                ret += self.print_tree(current_node.right, head_type, level)
                level += 1
                ret += self.print_tree(current_node.left, head_type, level)
                level +=1
                return ret
            return ''
            