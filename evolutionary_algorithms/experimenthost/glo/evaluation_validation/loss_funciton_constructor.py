from evolutionary_algorithms.experimenthost.glo.populate.function_library import FunctionLibrary

class LossFunctionConstructor:

    @staticmethod
    def construct_loss(tree):

        function_list = tree.function_list
        tensorflow_handle_list = tree.tensorflow_handle_list
        function_library_obj = FunctionLibrary()

        def loss(y_pred, y_true):
            stack = []
            cost = None
            for function, handle in zip(function_list, tensorflow_handle_list):
                function_type = function_library_obj.get_function_type(function)

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
                    elif last_literal == "-1":
                        last_literal = -1
                    elif last_literal == "1":
                        last_literal = 1

                    cost = handle(last_literal)
                    stack.append(cost)

                elif function_type == "B":
                    last_two_literals = [stack.pop(), stack.pop()]

                    if last_two_literals[0] == "y":
                        last_two_literals[0] = y_pred
                    elif last_two_literals[0] == "t":
                        last_two_literals[0] = y_true
                    elif last_two_literals[0] == "-1":
                        last_two_literals[0] = -1
                    elif last_two_literals[0] == "1":
                        last_two_literals[0] = 1

                    if last_two_literals[1] == "y":
                        last_two_literals[1] = y_pred
                    elif last_two_literals[1] == "t":
                        last_two_literals[1] = y_true
                    elif last_two_literals[1] == "-1":
                        last_two_literals[1] = -1
                    elif last_two_literals[1] == "1":
                        last_two_literals[1] = 1

                    cost = handle(last_two_literals[0], last_two_literals[1])
                    stack.append(cost)

            return cost

        return loss
