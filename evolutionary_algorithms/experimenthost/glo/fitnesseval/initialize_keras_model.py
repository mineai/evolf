from evolutionary_algorithms.experimenthost.glo.lossconstructor.loss_funciton_constructor import \
    LossFunctionConstructor
from evolutionary_algorithms.experimenthost.glo.fitnesseval.load_keras_evaluator import LoadKerasEvaluator
import keras


class InitializeKerasModel(LoadKerasEvaluator):

    def __init__(self, tree, evaluator_config, loss=None):
        LoadKerasEvaluator.__init__(self, evaluator_config)
        self.tree = tree
        if loss is not None:
            self.loss = loss
        else:
            self.loss = LossFunctionConstructor.construct_loss(self.tree)
        self.compile_model()

    def compile_model(self):
        try:
            self.model.compile(loss=self.loss,
                               optimizer=keras.optimizers.Adadelta(),
                               metrics=['accuracy'])
            return True
        except:
            self.tree.working = False
            return False
