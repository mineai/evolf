import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras import backend as K
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, Conv2D, MaxPooling2D
import random
import copy
from tqdm import trange
import math
import numpy as np

from evolutionary_algorithms.reproduction.selection.selection_functions_library \
		import SelectionFunctionsLibrary

from evolutionary_algorithms.servicecommon.utils.math_utils \
		import MathUtils

from evolutionary_algorithms.servicecommon.utils.list_utils \
		import ListUtils

from evolutionary_algorithms.reproduction.crossover.crossover_functions \
		import CrossoverFunctions

class NeuroevolutionMnist():

	def __init__(self, population_size,
				epochs,
				batch_size):
		self.x_train, self.y_train, self.x_test, self.y_test = self.setup_mnist()

		self.train_data = [self.x_train, self.y_train]
		self.test_data = [self.x_test, self.y_test]

		self.model = self.build_keras_model()

		self.num_examples = len(self.y_train)
		self.population_size = population_size

		self.epochs = epochs
		self.batch_size = batch_size

		self.chunks_x = ListUtils().block_list( self.x_train, math.ceil(self.num_examples / self.population_size) )[:self.population_size]
		self.chunks_y = ListUtils().block_list( self.y_train, math.ceil(self.num_examples / self.population_size) )[:self.population_size]

	@staticmethod
	def setup_mnist():
		# the data, split between train and test sets
		(x_train, y_train), (x_test, y_test) = mnist.load_data()
		img_rows, img_cols = 28, 28
		if K.image_data_format() == 'channels_first':
			x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
			x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
			input_shape = (1, img_rows, img_cols)
		else:
			x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
			x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
			input_shape = (img_rows, img_cols, 1)

		x_train = x_train.astype('float32')
		x_test = x_test.astype('float32')
		x_train /= 255
		x_test /= 255

		num_classes = 10
		# convert class vectors to binary class matrices
		y_train = keras.utils.to_categorical(y_train, num_classes)
		y_test = keras.utils.to_categorical(y_test, num_classes)

		return x_train, y_train, x_test, y_test

	@staticmethod
	def build_keras_model():
		img_rows, img_cols = 28, 28
		input_shape = (img_rows, img_cols, 1)
		num_classes = 10
		model = Sequential()
		model.add(Conv2D(32, kernel_size=(3, 3),
			 activation='relu',
			 input_shape=input_shape))
		model.add(Conv2D(64, (3, 3), activation='relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(BatchNormalization(momentum=0.75, epsilon=0.001))
		model.add(Dropout(0.25))
		model.add(Flatten())
		model.add(Dense(128, activation='relu'))
		# model.add(BatchNormalization(momentum=0.75, epsilon=0.001))
		model.add(Dropout(0.5))
		model.add(Dense(num_classes, activation='softmax'))

		return model

	def train_model(self, model, data):
		x, y = data
		hist = model.fit(x, y,
		  batch_size=self.batch_size,
		  epochs=self.epochs,
		  verbose=1,
		  validation_data=(x, y))
		return hist

	@staticmethod
	def evaluate_model(model, data):
		x, y = data
		accuracy = model.evaluate(x, y, verbose=0)[1]
		return accuracy

	def generate_population(self, num_models):
		population = []
		fitness = []
		for model_num in trange(num_models):
			model_copy = keras.models.clone_model(self.model,
										input_tensors = None)
			model_copy.compile(loss=keras.losses.categorical_crossentropy,
				optimizer=keras.optimizers.Adadelta(),
				metrics=['accuracy'])
			hist = self.train_model(model_copy, [self.chunks_x[model_num], self.chunks_y[model_num]])
			fitness_of_model = hist.history['acc'][0]
			# fitness_of_model = self.evaluate_model(model_copy, self.test_data)

			population.append(model_copy)
			fitness.append(fitness_of_model)

		return population, fitness

	@staticmethod
	def get_flattened_weights(weight_tensors_list):
		"""
		This function takes in the trainable weights of the model
		and flattens them into a 1-D Array
		:params weight_tensors_list: A np.array containing weights of the
		model.
		:returns flattened_weights: A 1-D python list containing all the weights
		:returns shapes: A list of tuples represention tuples of the original
						np arrays
		"""
		shapes = []
		flattened_weights = []
		for weight_tensor in weight_tensors_list:
			shape = weight_tensor.shape
			flattened_weight = weight_tensor.flatten()
			shapes.append(shape)
			flattened_weights.extend(flattened_weight.tolist())
		return flattened_weights, shapes

	@staticmethod
	def revert_weight_shape(flattened_weight_list, shape_list):
		weight_tensor_list = []
		start_idx = 0
		for shape in shape_list:
			end_idx = start_idx + np.prod(shape)
			weights = np.array(flattened_weight_list[start_idx:end_idx])
			weights = weights.reshape(shape)
			weight_tensor_list.append(weights)
			start_idx = end_idx

		return weight_tensor_list



if __name__ == "__main__":

	# TO RUN:  python3 -m  evolutionary_algorithms.experimenthost.neuroevolution.neuroevolution_mnist

	nev = NeuroevolutionMnist(population_size=10,
					epochs=1,
					batch_size=32)


	num_generations = 10
	rate_mutation = 0.1
	mating_pool = 1000
	num_parents = 5

	population, fitness = nev.generate_population(nev.population_size)
	fitness = MathUtils().softmax(fitness)

	mating_pool = SelectionFunctionsLibrary().default_mating_pool(population, fitness,
																	mating_pool)

	parents = SelectionFunctionsLibrary().natural_selection(mating_pool, num_parents)

	genes_of_parents = []
	for parent in parents:
		weights_of_model = nev.model.get_weights()
		flattened_weights, shapes = nev.get_flattened_weights(weights_of_model)
		genes_of_parents.append(flattened_weights)

	child = CrossoverFunctions().crossover_function_lists(genes_of_parents)
	child_weights = nev.revert_weight_shape(child, shapes)

	child_model = keras.models.clone_model(self.model,
								input_tensors = None)
	child_model.compile(loss=keras.losses.categorical_crossentropy,
		optimizer=keras.optimizers.Adadelta(),
		metrics=['accuracy'])
	child_model.set_weights(child_weights)
	child_performance = nev.evaluate_model(child_model, self.test_data)
	print(child_performance)



	# print(weights_of_model)
	# print("\n\n")
	# print(weight_tensor)

	# print(flattened_weights)
