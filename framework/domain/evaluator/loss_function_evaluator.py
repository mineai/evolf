

class LossFunctionEvaluator:

    def evaluate_loss(self, evaluator_model, data_dict, loss, loss_evaluator_config={}):
        """
        Thus function serves as an interface to train and test the
        model.
        :param evaluator_model: Model to be used to evaluate the loss function
        :param data_dict: Dictionary containing the data.
        :param loss: The loss function that should be used to evaluate the model
        :param loss_evaluator_config: The config if any that needs to be used by the
        evaluator
        :return metrics: A dictionary containing the metrics that need
        to be used to determine the fitness. These fitness objectives
        can be specified through the HOCON, else by default the keyword
        that will need to be used is 'fitness'
        """
        raise NotImplementedError
