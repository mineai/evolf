class Node:
    # Constructor
    def __init__(self, type=None, data=None):
        self.data = data
        self.type = type
        self.id = None
        self.left = None
        self.right = None