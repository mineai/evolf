from evolutionary_algorithms.experimenthost.glo.populate.function_library import FunctionLibrary


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
        def loss(y_pred, y_true):
            stack = []
            cost = None

            for node in tree.nodes:
                function_type = node.operator_type
                handle = node.tensorflow_handle
                function = node.function_str
                if function_type == "R":
                    last_literal = stack.pop()

                    if last_literal == "y":
                        last_literal = y_pred
                    elif last_literal == "t":
                        last_literal = y_true

                    cost = handle(last_literal)
                    stack.append(cost)

                elif function_type == "L":
                    stack.append(function)

                elif function_type == "U":
                    last_literal = stack.pop()

                    if last_literal == "y":
                        last_literal = y_pred
                    elif last_literal == "t":
                        last_literal = y_true
                    elif last_literal == "neg_scalar":
                        last_literal = last_literal
                    elif last_literal == "pos_scalar":
                        last_literal = last_literal

                    cost = handle(last_literal)
                    stack.append(cost)

                elif function_type == "B":
                    last_two_literals = [stack.pop(), stack.pop()]

                    if last_two_literals[0] == "y":
                        last_two_literals[0] = y_pred
                    elif last_two_literals[0] == "t":
                        last_two_literals[0] = y_true
                    elif last_two_literals[0] == "neg_scalar":
                        last_two_literals[0] = int(last_two_literals[0])
                    elif last_two_literals[0] == "pos_scalar":
                        last_two_literals[0] = int(last_two_literals[0])

                    if last_two_literals[1] == "y":
                        last_two_literals[1] = y_pred
                    elif last_two_literals[1] == "t":
                        last_two_literals[1] = y_true
                    elif last_two_literals[1] == "neg_scalar":
                        last_two_literals[1] = int(last_two_literals[1])
                    elif last_two_literals[1] == "pos_scalar":
                        last_two_literals[1] = int(last_two_literals[1])

                    cost = handle(last_two_literals[0], last_two_literals[1])
                    stack.append(cost)

            return cost
        return loss
