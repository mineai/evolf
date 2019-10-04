class Node:
    # Constructor
    def __init__(self, operator_type=None, data=None):
        self.data = data
        self.operator_type = operator_type
        self.node_id = None
        self.children = []
        self.left = None
        self.right = None

    def set_data(self, data):
        self.data = data

    def set_type(self, type):
        self.type = type
    
    def set_id(self, id):
        self.id = id    
