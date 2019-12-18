class GenerateDataDict:
    """
    This class serves as the interface which should
    be overriden in the domain to load data
    for the evaluator.
    """

    def load_data(self):
        """
        This Function is overriden
        to generate the data and must
        return the predictors and the labels
        :return data_dict: Dictionary containing the
        required stuff to train the model
        """
        raise NotImplementedError
