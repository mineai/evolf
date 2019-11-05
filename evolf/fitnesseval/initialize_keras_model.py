from evolf.lossconstructor.loss_funciton_constructor import \
    LossFunctionConstructor
from evolf.fitnesseval.load_keras_evaluator import LoadKerasEvaluator


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
        import keras
        try:
            self.model.compile(loss=self.loss,
                               optimizer=keras.optimizers.Adadelta(),
                               metrics=['accuracy'])
            self.tree.working = True
            return True
        except:
            print("This tree failed to compile")
            self.tree.working = False
            return False
