from framework.domain.evaluator.generate_data_dict import GenerateDataDict
from framework.domain.evaluator.evaluator_constructor import EvaluatorConstructor
from framework.domain.evaluator.loss_function_evaluator import LossFunctionEvaluator
from framework.domain.searchspace.search_space_handles import SearchSpaceHandles


class DomainEvaluator(GenerateDataDict, LossFunctionEvaluator, EvaluatorConstructor, SearchSpaceHandles):
    """
    This Class inherits from three base interfaces whose functions
    must be overwritten and specified by respective domain whose loss
    function has to be evolved.

    The functions in this interface consists of:
    1) build_evaluator_model: This function must be overwritten and a keras model
    should be built and returned.

    2) evaluate_loss: This function must be overwritten to
    train and test the model with the given data. The metrics
    that need to be used for loss function optimization
    must be gathered as key:value pairs in a dictionary and returned.
    The keys should be the fitness_objectives specified in the config.

    3) load_data: This function should be overwritten to fetch/load/unpack
    the data and return the predictors and the labels.

    4) specify_loss_search_space

    This class does nothing but serves as a combination of
    three other interfaces so that the end user has to
    inherit only once.

    """
    pass


