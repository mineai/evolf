
class EvaluatorConstructor:
    """
    This class serves as an interface that should
    be overridden to evaluate the loss function
    for a specific domain.
    """

    def build_evaluator_model(self):
        """
        This function acts as an interface to the domains to
        create the model/
        :params none:
        :return model: The created Keras model
        """
        raise NotImplementedError