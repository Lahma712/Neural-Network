import tensorflow as tf
import numpy as np
from extra_keras_datasets import emnist

epochs = 10 #number of times the network iterates over training set
(training_images,training_labels), (test_images,test_labels) = emnist.load_data(type = 'digits')
training_images = tf.keras.utils.normalize(training_images, axis=1)
test_images = tf.keras.utils.normalize(test_images, axis=1)
aliased_training_images = (training_images > 0).astype(float) #tdatasets get aliased (are normally anti-aliased from MNIST)
aliased_test_images = (test_images > 0).astype(float)  

compl_training_images = np.concatenate((aliased_training_images, aliased_test_images), axis = 0) #adds test images to training images to increase training dataset -> better performance
compl_training_labels = np.concatenate((training_labels, test_labels), axis=0)
network = tf.keras.models.Sequential()

#2 hidden layers, each layer having 150 neurons (output layer having 10 neurons)
network.add(tf.keras.layers.Flatten(input_shape = (28,28)))
network.add(tf.keras.layers.Dense(300, activation = tf.nn.relu))
#network.add(tf.keras.layers.Dense(150, activation = tf.nn.relu))
network.add(tf.keras.layers.Dense(300, activation = tf.nn.relu))
network.add(tf.keras.layers.Dense(10, activation = tf.nn.softmax))

network.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics = ['accuracy'])
network.fit(compl_training_images, compl_training_labels, epochs = epochs)
network.save('network.model') #saves model

