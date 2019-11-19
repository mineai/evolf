

class Serialize:
    """
    This class acts as an interface to serialize
    custom classes.
    """

    def serialize(self):
        """
        Override this function to serialize a desired class.
        :return: nothing
        """
        raise NotImplementedError

    def deserialize(self):
        """
        Override this function to read in an object
        of desired format and reconstruct the class
        object.
        :return:
        """
        raise NotImplementedError