from framework.serialize.tree.tree_serializer import TreeSerializer
from experimenthost.evaluator.nnacceval.load_keras_evaluator import LoadKerasEvaluator
from framework.lossconstructor.loss_funciton_constructor import LossFunctionConstructor

class TreeNNAccEvaluator:

    def __init__(self, tree, data_dict, evaluator_config,
                 search_space_obj=None):

        # Initialize Class variables from Arguments
        self.tree = tree
        self.data_dict = data_dict
        self.search_space_obj = search_space_obj

        # Load the data
        self.x_train, self.y_train, \
        self.x_test, self.y_test, \
        self.x_validation, self.y_validation = self.initialize_data(data_dict)

        # Read the evaluator specs
        self.epochs = evaluator_config.get("epochs")
        self.verbose = evaluator_config.get("verbose", 1)
        self.batch_size = evaluator_config.get("batch_size", 32)

        early_stopping_config = evaluator_config.get("early_stopping_config")
        self.es_monitor = early_stopping_config.get("monitor", "val_acc")
        self.es_mode = early_stopping_config.get("mode", "max")
        self.print_early_stopping = early_stopping_config.get("print_early_stopping", True)
        self.es_patience = early_stopping_config.get("patience", 1)
        self.es_min_delta = early_stopping_config.get("min_delta", 1)
        self.model_folder = evaluator_config.get("model_load_path")
        self.model_filename = evaluator_config.get("model_file_name")
        self.weight_filename = evaluator_config.get("weight_file_name")

        # Initialize the model loader obj
        self.model_loader = LoadKerasEvaluator(self.model_folder,
                                         self.model_filename,
                                         self.weight_filename)

    def initialize_data(self, data_dict):
        x_train = data_dict.get("x_train")
        y_train = data_dict.get("y_train")
        x_test = data_dict.get("x_test")
        y_test = data_dict.get("y_test")
        x_validation = data_dict.get("x_validation")
        y_validation = data_dict.get("y_validation")

        return x_train, y_train, \
               x_test, y_test, \
               x_validation, y_validation

    def get_evaluator(self):
        model = self.model_loader.initialize_model()
        return model

    def compile_evaluator(self, model, loss):
        self.model_loader.compile_model(model, loss)

    def setup_callbacks(self):
        from keras.callbacks import EarlyStopping
        early_stopping_callback = EarlyStopping(monitor=self.es_monitor,
                                                mode=self.es_mode,
                                                verbose=self.print_early_stopping,
                                                patience=self.es_patience,
                                                min_delta=self.es_min_delta)
        return [early_stopping_callback]

    def construct_loss(self):
        # import pdb; pdb.set_trace()
        loss = LossFunctionConstructor.construct_loss(self.tree)
        return loss

    def process_tree(self):
        tree_deserializer = TreeSerializer(self.tree, self.search_space_obj)
        self.tree = tree_deserializer.deserialize()

    def evaluate_tree(self, model):

        # Get Callbacks
        callbacks = self.setup_callbacks()

        model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=self.verbose,
                       validation_data=(self.x_validation, self.y_validation),
                       callbacks=callbacks)

        test_acc = model.evaluate(self.x_test,
                                    self.y_test,
                                    verbose=self.verbose)[1]

        return test_acc

    def evaluate(self):
        if isinstance(self.tree, dict):
            self.process_tree()

        # Generate Loss
        loss = self.construct_loss()

        # Get Evaluator
        model = self.get_evaluator()
        self.compile_evaluator(model, loss)

        # Get the Fitness
        fitness = self.evaluate_tree(model)

        return fitness

