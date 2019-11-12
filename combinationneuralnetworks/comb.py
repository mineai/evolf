import keras
from combinationneuralnetworks.data import Data
from combinationneuralnetworks.network_constructor import NetworkConstructor
from combinationneuralnetworks.original_network import OriginalNetwork

# Get Data
x, t = Data.get_data_ciphar()

# Split into Training and Test Sets
train_percentage = 0.8
validation_percentage = 0.1
data_dict = Data.process_data(x, t,
                              train_percentage,
                              validation_percentage)

train_x = data_dict['x_train']
train_t = data_dict['y_train']
test_x = data_dict['x_test']
test_t = data_dict['y_test']
validation_x = data_dict['x_validation']
validation_t = data_dict['y_validation']

# Define Data Params
input_shape = data_dict['input_shape']
num_classes = 10

# Number Of neural Networks
number_of_models = 10

# Split Data
train_x_sets, train_t_sets = Data.divide_data(train_x,
                                              train_t,
                                              number_of_models)

# Get Comparision Model
# comparision_model = OriginalNetwork.get_orignal_network(input_shape,
#                                                         num_classes)
# # Compile Model
# comparision_model.compile(loss='categorical_crossentropy',
#                             optimizer=keras.optimizers.Adadelta(),
#                             metrics=['accuracy'])
# comparision_model.summary()
#
# # Train the Comparision Model
# print(f"Training Comparision Model")
# comparision_model.fit(train_x,
#                         train_t,
#                         batch_size=32,
#                         epochs=75,
#                         verbose=True,
#                         validation_data=(x, t))

# Get Neural Networks
network_constructor = NetworkConstructor(number_of_models, input_shape, num_classes)
print(f"Training Split Models")
network_constructor.train_split_models(train_x_sets,
                                       train_t_sets,
                                       [x, t])

# Freeze Combination Models
network_constructor.freeze_combination_model_layers()

# Train Combination Model
network_constructor.compile_and_train_combination_model(validation_x,
                                                        validation_t)



