class Node:
    """
    This class Initializes the node function_str type and
    its member variables
    """
    # Constructor
    def __init__(self, operator_type=None, function_str=None, symbolic_handle=None, tensorflow_handle=None):
        """
        The Constructor initializes the required Node
        member variables
        :param operator_type: The type of the operator -> U, B, L or R
        :param function_str: The function handle
        """
        self.function_str = function_str
        self.operator_type = operator_type
        self.symbolic_handle = symbolic_handle
        self.tensorflow_handle = tensorflow_handle
        self.node_id = None
        self.left = None
        self.right = None
        self.parent = None
        self.coefficient = 1