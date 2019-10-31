class Parser():
    """
    Interface for classes that take an object
    as an input and return some other construct.
    """

    def parse(self, input_obj):
        """
        :param input_obj: Object to be parsed

        :returns: An object parsed
        """

        raise NotImplementedError
