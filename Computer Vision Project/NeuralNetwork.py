import constants as C

import numpy as np

from keras.layers import Input, Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.callbacks import LearningRateScheduler, TensorBoard, EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model, load_model
from keras.optimizers import SGD


# Class to reduce the learning rate linearly
class LinearLRScheduler(object):
    def __init__(self, start, stop, max_epochs):
        self.ls = np.linspace(start, stop, max_epochs)

    def get(self, epoch):
        return self.ls[epoch]


class NeuralNetwork(object):
    def __init__(self):
        self.model = None

    @staticmethod
    def load(filepath=C.MODEL_FILE):
        cnn = NeuralNetwork()
        cnn.model = load_model(filepath)
        return cnn

    def save(self, filepath=C.MODEL_FILE):
        self.model.save(filepath)

    def predict(self, X, batch_size):
        return self.model.predict(X, batch_size, verbose=1)

    def create(self):
        # Input layer
        x = Input((1,) + C.IMG_DIMS)
    
        # Convolutional layers
        conv_layers = Conv2D(filters=C.CONV2D_FIRST_NUMFILTERS, kernel_size=C.CONV2D_FIRST_KERNEL,
                             data_format='channels_first', activation=C.CONV2D_FIRST_ACTIVATION)(x)
        conv_layers = MaxPooling2D(data_format='channels_first')(conv_layers)
        conv_layers = Dropout(C.DROPOUT_FIRST)(conv_layers)
    
        conv_layers = Conv2D(filters=C.CONV2D_SECOND_NUMFILTERS, kernel_size=C.CONV2D_SECOND_KERNEL,
                             data_format='channels_first', activation=C.CONV2D_SECOND_ACTIVATION)(conv_layers)
        conv_layers = MaxPooling2D(data_format='channels_first')(conv_layers)
        conv_layers = Dropout(C.DROPOUT_SECOND)(conv_layers)
    
        conv_layers = Conv2D(filters=C.CONV2D_THIRD_NUMFILTERS, kernel_size=C.CONV2D_THIRD_KERNEL,
                             data_format='channels_first', activation=C.CONV2D_THIRD_ACTIVATION)(conv_layers)
        conv_layers = MaxPooling2D(data_format='channels_first')(conv_layers)
        conv_layers = Dropout(C.DROPOUT_THIRD)(conv_layers)
        conv_layers = Flatten()(conv_layers)
    
        # Dense layers
        dense_layers = Dense(C.DENSE_NODES, activation=C.DENSE_ACTIVATION)(conv_layers)
        dense_layers = Dense(2, activation='softmax')(dense_layers)
    
        # Compiling it
        self.model = Model(inputs=[x], outputs=[dense_layers])
        sgd = SGD(lr=C.LEARNING_RATE_INITIAL, momentum=C.SGD_MOMENTUM, nesterov=C.SGD_NESTEROV)
        
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        print(self.model.summary())

    def train(self, X_val, y_val, X_train, y_train, batch_size=C.BATCH_SIZE, max_epochs=C.MAX_EPOCHS):
        # Callbacks
        gen = ImageDataGenerator(data_format='channels_first', horizontal_flip=C.IMAGE_GENERATOR_FLIP,
                                 rotation_range=C.IMAGE_GENERATOR_ROTATION)
        early_stopping = EarlyStopping('val_loss', patience=C.EARLY_STOPPING_PATIENCE, verbose=1)
        tensorboard = TensorBoard(log_dir=C.LOGDIR, write_graph=True, write_images=True)
    
        # Training
        self.model.fit_generator(gen.flow(X_train, y_train, batch_size, seed=C.SEED), epochs=max_epochs,
                            validation_data=(X_val, y_val), steps_per_epoch=len(X_train) // batch_size,
                            callbacks=[early_stopping,
                                       tensorboard,
                                       LearningRateScheduler(LinearLRScheduler(
                                           C.LEARNING_RATE_INITIAL,
                                           C.LEARNING_RATE_FINAL,
                                           max_epochs).get
                                       )]
                            )
