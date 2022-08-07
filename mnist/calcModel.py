import configparser
from numpy.random import seed
import tensorflow as tf
from tensorflow.python.framework import ops


config = configparser.ConfigParser()
config.read('config.ini')
seed(int(config['Numpy']['seed']))
tf.random.set_seed(int(config['Model']['seed']))
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

ops.reset_default_graph()

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

model.save('saved_model')
