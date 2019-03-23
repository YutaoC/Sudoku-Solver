"""in this file, we train the model using nmist dataset"""

import tensorflow as tf


# process the dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = tf.keras.utils.normalize(x_train, axis=1)  # normalize the training data
x_test = tf.keras.utils.normalize(x_test, axis=1)  # normalize the testing data

# model
model = tf.keras.models.Sequential()  # create the model
model.add(tf.keras.layers.Flatten())  # flatten the data into one dimension
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))  # the first layer
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))  # the second layer
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))  # the output layer

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])  # model parameters
model.fit(x_train, y_train, epochs=5)  # train the model

# test the dataset
# val_loss, val_acc = model.evaluate(x_test, y_test)
# print(val_loss, val_acc)

model.save('num_reader.model')  # save the model
