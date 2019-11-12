def get_data():
    import keras
    from keras.datasets import cifar10
    import numpy as np

    num_classes = 10
    # the function_str, split between train and test sets
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    x = np.concatenate((x_train, x_test))
    y = np.concatenate((y_train, y_test))

    # convert class vectors to binary class matrices
    predictors = x.astype('float32')
    labels = keras.utils.to_categorical(y, num_classes)

    print(predictors.shape)

    return predictors, labels

def create_model(input_shape, num_classes):
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Flatten, Activation
    from keras.layers import Conv2D, MaxPooling2D

    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    return model

def divide_data(x, t, num_sets):
    
    train_x_sets = np.split(x, num_sets)
    train_t_sets = np.split(t, num_sets)
    
    return train_x_sets, train_t_sets
    
def process_data(predictors, labels, train_percentage, validation_percentage):
    num_samples = len(predictors)
    num_train_samples = int(num_samples * train_percentage)
    num_validation_samples = int(num_samples * validation_percentage)

    x_train, y_train = predictors[:num_train_samples], labels[:num_train_samples]
    x_validation, y_validation = predictors[num_train_samples:num_train_samples + num_validation_samples], \
                                 labels[num_train_samples:num_train_samples + num_validation_samples]
    x_test, y_test = predictors[num_train_samples + num_validation_samples:], \
                     labels[num_train_samples + num_validation_samples:]


    input_shape = x_train.shape[1:]
    data_dict = {
            "x_train": x_train,
            "x_test": x_test,
            "y_train": y_train,
            "y_test": y_test,
            "x_validation": x_validation,
            "y_validation": y_validation,
            "input_shape": input_shape
        }

    return data_dict

from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D, concatenate
import numpy as np

def create_base_model(input_shape, num_classes, name):
    input_layer = Input(shape=input_shape)
    conv = Conv2D(64, kernel_size=(3, 3),
                     activation='relu')(input_layer)
    conv = Conv2D(64, kernel_size=(3, 3),
                     activation='relu')(conv)
    max_pool_1 = MaxPooling2D(pool_size=(2, 2))(conv)
    
    conv = Conv2D(128, kernel_size=(3, 3),
                     activation='relu')(max_pool_1)
    conv = Conv2D(128, kernel_size=(3, 3),
                     activation='relu')(conv)
    conv = Conv2D(128, kernel_size=(3, 3),
                     activation='relu')(conv)
    conv = Conv2D(128, kernel_size=(3, 3),
                     activation='relu')(conv)
    max_pool_1 = MaxPooling2D(pool_size=(2, 2))(conv)
    dropout_1 = Dropout(0.25)(max_pool_1)
    
    flatten = Flatten()(dropout_1)
    dense = Dense(512, activation='relu')(flatten)
    dropout_2 = Dropout(0.5)(dense)
    output = Dense(num_classes, activation='softmax')(dropout_2)
    
    model_cut = Model(inputs=[input_layer], outputs=[conv], name=f"{name}_cut")
    model_complete = Model(inputs=[input_layer], outputs=[output], name=f"{name}_full")
    
    return model_cut, model_complete


def create_combination_model(input_shape, num_classes):
    input_layer = Input(shape=input_shape[1:])
    conv = Conv2D(64, kernel_size=(1, 1),
                     activation='relu')(input_layer)
    conv = Conv2D(64, kernel_size=(1, 1),
                     activation='relu')(conv)
    conv = Conv2D(64, kernel_size=(3, 3),
                     activation='relu')(conv)
    flatten = Flatten()(conv)
    dense = Dense(512, activation='relu')(flatten)
    output = Dense(num_classes, activation='softmax')(dense)
    
    model = Model(inputs=[input_layer],
                 outputs=[output])
    return model

def collect_output_tensors(models):
    output_tensors = []
    for model in models:
        output_tensors.append(model.output)
    return output_tensors

def collect_input_tensors(models):
    input_tensors = []
    for model in models:
        input_tensors.append(model.input)
        
    return input_tensors



def create_combination(models, num_classes):
    input_tensors = collect_input_tensors(models)
    
    # Collect the Real Models
    real_models = []
    for model in models:
        model_dense_x = model(model.input)
        real_models.append(model_dense_x)
        
    
    # Concatenate
    combination_layer = concatenate(real_models, axis=-1)
    
    # Define Combination model
    input_shape = combination_layer._shape_tuple()
    combination_model = create_combination_model(input_shape, num_classes)
    combination_model_init = combination_model(combination_layer)
    
    model = Model(input_tensors, combination_model_init)
      
    return model

x, t = get_data()

train_percentage = 0.5
validation_percentage = 0.4
data_dict = process_data(x, t, train_percentage, validation_percentage)

train_x = data_dict['x_train']
train_t = data_dict['y_train']
test_x = data_dict['x_test']
test_t = data_dict['y_test']
validation_x = data_dict['x_validation']
validation_t = data_dict['y_validation']


num_train_sets = 20
train_x_sets, train_t_sets = divide_data(train_x, train_t, num_train_sets)

data_input_shape = data_dict['input_shape']
num_classes = 10

import keras
models_cut, models_full = [], []
for model_idx in range(num_train_sets):
    model_cut, model_full = create_base_model(data_input_shape, 
                                   num_classes, 
                                   f"ciphar_model_{model_idx}")
    models_cut.append(model_cut)
    models_full.append(model_full)

final_model = create_combination(models_cut, num_classes)

final_model.compile(loss='categorical_crossentropy',
                                   optimizer=keras.optimizers.Adadelta(),
                                   metrics=['accuracy'])
state_of_the_art = create_model(data_input_shape,
                                   num_classes)
state_of_the_art.compile(loss='categorical_crossentropy',
                                   optimizer=keras.optimizers.Adadelta(),
                                   metrics=['accuracy'])
state_of_the_art.fit(train_x_sets[model_idx], train_t_sets[model_idx],
                       batch_size=32,
                       epochs=75,
                       verbose=True,
                       validation_data=(x, t))
for model in models_full:
    model.compile(loss='categorical_crossentropy',
                                   optimizer=keras.optimizers.Adadelta(),
                                   metrics=['accuracy'])
    model.fit(train_x_sets[model_idx], train_t_sets[model_idx],
                           batch_size=32,
                           epochs=25,
                           verbose=True,
                           validation_data=(x, t))

for model in models_full:
    scores = model.evaluate(x, t, verbose=True)
    print("Test Score: ", scores[1])

def freeze_final_model_layers(final_model):
    for layer in final_model.layers[:-1]:
        class_name = layer.__class__.__name__
        if class_name == 'Model':
            for nested_layer in layer.layers[1:]:
                nested_layer.trainable = False

freeze_final_model_layers(final_model)
final_model.compile(loss='categorical_crossentropy',
                                   optimizer=keras.optimizers.Adadelta(),
                                   metrics=['accuracy'])
final_model.summary()

full_training_data_x = [validation_x] * num_train_sets
full_test_data_x = [x] * num_train_sets
full_training_data_t = validation_t

final_model.fit(full_training_data_x, 
                full_training_data_t,
               batch_size=32,
               epochs=50,
               verbose=True,
               validation_data=(full_test_data_x, t))

