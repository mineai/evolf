class NodeConstructor:

    @staticmethod
    def create_weight_node(weight=None):
        # Weight Node
        if weight is None:
            weight = random.uniform(-10, 10)
        operator_type = "L"
        if weight >= 0:
            function_str = "pos_scalar"
        else:
            function_str = "neg_scalar"
        symbolic_handle = weight * FunctionLibrary.get_symbolic_handle("pos_scalar")
        tensorflow_handle = weight * FunctionLibrary.get_tensorflow_handle("pos_scalar")
        weight_node = Node(operator_type=operator_type, function_str=function_str,
                           symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)

        return weight_node

    @staticmethod
    def create_binary_node(operator=None):
        # Create A binary node
        operator_type = "B"
        if operator is None:
            operator = FunctionLibrary.sample(operator_type)

        symbolic_handle = FunctionLibrary.get_symbolic_handle(operator)
        tensorflow_handle = FunctionLibrary.get_tensorflow_handle(operator)
        binary_node = Node(operator_type=operator_type, function_str=operator,
                                   symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)
        return binary_node

    @staticmethod
    def create_unary_node(operator=None):
        # Create A binary node
        operator_type = "U"
        if operator is None:
            operator = FunctionLibrary.sample(operator_type)
        symbolic_handle = FunctionLibrary.get_symbolic_handle(operator)
        tensorflow_handle = FunctionLibrary.get_tensorflow_handle(operator)
        unary_node = Node(operator_type=operator_type, function_str=operator,
                           symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)
        return unary_node