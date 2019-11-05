class ConnectionGene:
    """
    This class serves as the Connection Gene as described in the
    original NEAT Paper.
    """
    def __init__(self, in_node, out_node, weight, expressed, innovation_number):
        """
        The Constructor initializes the instance variables of this class.
        :param in_node: Integer that stores the ID of the input node
        :param out_node: Integer that stores the ID of the output node
        :param weight: The weight of this Connection
        :param expressed: Is the weight enabled?
        :param innovation_number: Integer value storing the Historical marking
                                for each weight
        """
        self._in_node = in_node
        self._out_node = out_node
        self._weight = weight
        self._expressed = expressed
        self._innovation_number = innovation_number


    def get_in_node(self):
        """
        This function acts as a getter
        to fetch the in node
        :return: Private member _in_node
        """
        return self._in_node

    def get_out_node(self):
        """
        This function acts as a getter
        to fetch the out node
        :return: Private member _out_node
        """
        return self._out_node

    def get_weight(self):
        """
        This function acts as a getter
        to fetch the weight of the connection
        :return: Private member _weight
        """
        return self._weight

    def is_expressed(self):
        """
        This function acts as a getter
        to tell if the conenction is enabled or not
        :return: Private member _expressed
        """
        return self._expressed

    def get_innovation_number(self):
        """
        This function acts as a getter
        to fetch the historical marker
        :return: Private member _innovation_number
        """
        return self._innovation_number

    def disable(self):
        """
        This function disables the expressed
        private member
        """
        self._expressed = False

    def enable(self):
        """
        This function enables the expressed
        private member
        """
        self._expressed = True

    def toggle_expression(self):
        """
        This function toggles the expressed
        private member
        """
        if self.is_expressed():
            self.disable()
        else:
            self.enable()

    def clone_gene(self):
        """
        This function clones the gene and returns a new object.
        :return:
        """
        return ConnectionGene(self._in_node,
                              self._out_node,
                              self._weight,
                              self._expressed,
                              self._innovation_number)

    def set_weight(self, value):
        """
        This function sets the value of the private variable
        _weight
        :param value:
        :return:
        """
        self._weight = value
