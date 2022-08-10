import configparser
from numpy.random import seed
import tensorflow as tf
from tensorflow.python.framework import ops
import random


config = configparser.ConfigParser()
config.read('config.ini')
seed(int(config['Numpy']['seed']))
tf.random.set_seed(int(config['Model']['seed']))
tf.keras.utils.set_random_seed(int(config['Keras']['seed']))
tf.config.experimental.enable_op_determinism()
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

ops.reset_default_graph()

tf.config.optimizer.set_experimental_options({'disable_meta_optimizer': True, 'disable_model_pruning': True})
print(tf.config.optimizer.get_experimental_options())

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu', kernel_initializer=tf.random_uniform_initializer(seed=int(config['Model']['seed']))),
  tf.keras.layers.Dropout(0.2, seed=int(config['Model']['seed'])),
  tf.keras.layers.Dense(10, kernel_initializer=tf.random_uniform_initializer(seed=int(config['Model']['seed'])))
])

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

random.seed(11)
model.fit(x_train, y_train, epochs=5, verbose=2, shuffle=False, batch_size=16)

model.evaluate(x_test,  y_test, verbose=2)

model.save('saved_model')
