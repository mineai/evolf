
class SearchSpaceHandles:
    """
    This class specifies the dictionary that are the specific
    function handles that must be used with the evaluator.
    By default this handle is based off of Keras but can be
    simply replaced with numpy handles or scipy handles or
    any other handles that need to be used with the evaluator.

    NOTE: If the evaluator needs a loss function that will work with
    Keras loss functions, This function does not need to be overridden.
    """

    def specify_loss_search_space(self):
        """
        This function can be overridden to generate loss functions
        of some other type rather than keras. While overriding keep
        the structure the same.
        1) Import the numerical lbrary that contains the handles if needed
        2) Generate a dictionary containing the handles.
        3) return the dictionary

        :return loss_search_space: Dictionary containing key value pairs
        of function names and handles.
        """
        import keras.backend as K
        # This gives the range of possible keras functions usable
        loss_search_space = {
            "cos": K.cos,
            "sin": K.sin,
            "log": K.log,
            "exp": K.exp,
            "square": K.square,
            "sqrt": K.sqrt,
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "y": "y_pred",
            "t": "y_true",
            "pos_scalar": 1,
            "neg_scalar": -1,
            "mean": K.mean,
            "sum": K.sum,
            "max": K.max,
            "min": K.min
        }
        return loss_search_space



