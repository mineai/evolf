
class Visualize:

    def __init__(self, tree):
        self.tree = tree

    def print_tree(self, current_node, head_type="operator_type", level=0):

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
            num_tabs = '\t' * (self.tree.height - level)
            if head_type == "operator_type":
                ret = num_tabs + repr(current_node.type) + '\n'
            elif head_type == "data":
                ret = num_tabs + repr(current_node.data) + '\n'
            elif head_type == "node_id":
                ret = num_tabs + repr(current_node.id) + '\n'
            ret += self.print_tree(current_node.right, head_type, level)
            level += 1
            ret += self.print_tree(current_node.left, head_type, level)
            level += 1
            return ret
        return ''

    @staticmethod
    def print_tree_levels_list(root):
        from collections import deque
        buf = deque()
        output = []
        if not root:
            print('$')
        else:
            buf.append(root)
            count, nextCount = 1, 0
            while count:
                node = buf.popleft()
                if node:
                    output.append(node.data)
                    count -= 1
                    for n in (node.left, node.right):
                        if n:
                            buf.append(n)
                            nextCount += 1
                        else:
                            buf.append(None)
                else:
                    output.append('$')
                if not count:
                    print(output)
                    output = []
                    count, nextCount = nextCount, 0
            # print the remaining all empty leaf node part
            output.extend(['$'] * len(buf))
            print(output)
