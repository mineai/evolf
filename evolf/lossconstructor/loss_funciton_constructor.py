class LossFunctionConstructor:
    """
    This class provides a wrapper to construct the loss function
    for Keras using a closure from the GLO Tress.
    """
    @staticmethod
    def construct_loss(tree):
        """
        A closure function that takes in a tree and evaluates it in a
        way that it can be used with a Keras Neural Network.
        :param tree: object of tree class.
        :return loss: The loss function generated in a way that Keras
        expects it to be in.
        """
        def loss(y_true, y_pred):
            stack = []
            cost = None

            for node in tree.nodes:
                function_type = node.operator_type
                handle = node.tensorflow_handle
                function = node.function_str

                if function_type in ["R", "U"]:
                    last_literal = stack.pop()
                    cost = node.coefficient * handle(last_literal)
                    stack.append(cost)

                elif function_type == "L":
                    if function == "y":
                        function = y_pred
                    elif function == "t":
                        function = y_true
                    stack.append(node.coefficient * function)
                elif function_type in ["B", "BBL"]:
                    last_two_literals = [stack.pop(), stack.pop()]
                    cost = node.coefficient * handle(last_two_literals[0], last_two_literals[1])
                    stack.append(cost)

            return cost
        return loss
