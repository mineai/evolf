class Node:
    # Constructor
    def __init__(self, operator_type=None, data=None):
        self.data = data
        self.operator_type = operator_type
        self.node_id = None
        self.left = None
        self.right = None