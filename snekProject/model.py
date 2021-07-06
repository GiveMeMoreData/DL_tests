import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import TimeDistributed, MaxPooling2D, Conv2D, Flatten, Dense


def get_model():
    inputs = tf.keras.Input(shape=(64, 64, 3))
    x = tf.keras.layers.Conv2D(8, kernel_size=(2, 2), padding="same", activation=tf.nn.relu)(inputs)
    x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)  # 32x32

    x = tf.keras.layers.Conv2D(8, kernel_size=(2, 2), padding="same", activation=tf.nn.relu)(x)
    x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)  # 16x16

    x = tf.keras.layers.Conv2D(16, kernel_size=(2, 2), padding="same", activation=tf.nn.relu)(x)
    x = tf.keras.layers.Conv2D(16, kernel_size=(2, 2), padding="same", activation=tf.nn.relu)(x)
    x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)  # 8x8

    x = tf.keras.layers.Conv2D(32, kernel_size=(2, 2), padding="same", activation=tf.nn.relu)(x)
    x = tf.keras.layers.Conv2D(32, kernel_size=(2, 2), padding="same", activation=tf.nn.relu)(x)
    x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)  # 4x4

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128, activation=tf.nn.relu)(x)
    x = tf.keras.layers.Dense(128, activation=tf.nn.relu)(x)

    outputs = tf.keras.layers.Dense(5, activation=tf.nn.softmax)(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model

def get_model_small():
    inputs = tf.keras.Input(shape=(64, 64, 3))
    x = tf.keras.layers.Conv2D(16, kernel_size=(4, 4), padding="same", activation=tf.nn.relu)(inputs)
    x = tf.keras.layers.MaxPooling2D(pool_size=(4, 4), strides=(2, 2))(x)  # 32x32

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(64, activation=tf.nn.relu)(x)
    outputs = tf.keras.layers.Dense(5, activation=tf.nn.softmax)(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def get_model_flat():
    inputs = tf.keras.Input(shape=(6,))
    x = tf.keras.layers.Dense(8, activation=tf.nn.relu)(inputs)
    x = tf.keras.layers.Dense(8, activation=tf.nn.relu)(x)
    outputs = tf.keras.layers.Dense(5, activation=tf.nn.softmax)(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model
