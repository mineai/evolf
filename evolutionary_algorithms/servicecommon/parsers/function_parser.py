class FunctionParser():
    """
    This class takes in a function object and its arguments and calls the
    function. If the function has a return value it will be returned, otherwise
    None is returned.

    Note: To use the static methods of this class, pass None's in the constructor.
    """


    def __init__(self, function_obj=None, args=None):
        """
        :param function_obj: The function object to be called.
        :param args: A list/tuple containing all the arguments the function
        would require

        :returns nothing
        """
        self._function = function_obj
        self._function_args = args

    def call_function(self):
        """
        This function calls the function and returns the value.
        If no return value is specified a None will be returned.
        :params none

        :returns return_value: The value returned by the function
        """
        if self._function_args is not None:
            return_value = self._function(*self._function_args)
        else:
            return_value = self._function()
        return return_value


    @staticmethod
    def contains_explicit_return(function_obj):
        """
        This function inspects if the input function
        has a return value or not.
        :param function_obj: Function Obj to be inspected

        :returns has_return_value: Boolean wether the function has a return
        value or not.
        """
        import ast
        import inspect
        has_return_value  = any(isinstance(node, ast.Return) \
                for node in ast.walk(ast.parse(inspect.getsource(function_obj))))
        return has_return_value
