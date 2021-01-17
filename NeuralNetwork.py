import tensorflow as tf
import numpy as np
import sys

import matplotlib.pyplot as plt

epochs = 20

objects = tf.keras.datasets.mnist
np.set_printoptions(threshold=sys.maxsize)

(training_images,training_labels), (test_images,test_labels) = objects.load_data()

training_images = tf.keras.utils.normalize(training_images, axis=1)
test_images = tf.keras.utils.normalize(test_images, axis=1)



new_training_images = (training_images > 0).astype(float)

#plt.imshow(new_training_images[2000])
#plt.show()

network = tf.keras.models.Sequential()
network.add(tf.keras.layers.Flatten(input_shape = (28,28)))

network.add(tf.keras.layers.Dense(150, activation = tf.nn.relu))
network.add(tf.keras.layers.Dense(150, activation = tf.nn.relu))
network.add(tf.keras.layers.Dense(150, activation = tf.nn.relu))
network.add(tf.keras.layers.Dense(10, activation = tf.nn.softmax))

network.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics = ['accuracy'])
network.fit(new_training_images, training_labels, epochs = epochs)
network.save('network.model')

