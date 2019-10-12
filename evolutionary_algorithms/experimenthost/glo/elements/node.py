class Node:
    """
    This class Initializes the node data type and
    its member variables
    """
    # Constructor
    def __init__(self, operator_type=None, data=None):
        """
        The Constructor initializes the required Node
        member variables
        :param operator_type: The type of the operator -> U, B, L or R
        :param data: The function handle
        """
        self.data = data
        self.operator_type = operator_type
        self.node_id = None
        self.left = None
        self.right = None

    def set_data(self, data):
        """
        This function sets the class variable data
        :param data: Function Handle
        :return nothing:
        """
        self.data = data

    def set_type(self, type):
        """
        This function sets the class variable type
        :param type: String defining the type
        :return nothing:
        """
        self.type = type
    
    def set_id(self, id):
        """
        This function sets the class variable node_id
        :param id: The node id to be assigned
        :return nothing:
        """
        self.node_id = id
