import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np

# Daten in die richtige Form bringen
datagen = ImageDataGenerator(rescale=1./255)

# Das Trainings- und Testset erstellen
train_data = datagen.flow_from_directory(
    'images/train/',
    target_size=(200, 200),
    batch_size=32,
    class_mode='binary'
)

test_data = datagen.flow_from_directory(
    'images/test/',
    target_size=(200, 200),
    batch_size=32,
    class_mode='binary'
)

# Das Model erstellen
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Das Model kompilieren
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Das Model trainieren
history = model.fit(train_data, validation_data=test_data, epochs=20)

# Define your function to plot training accuracy against the amount of training data
def plot_accuracy_vs_training_data(history):
    # Extract the accuracy values from the history
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    # Compute the number of training examples used at each epoch
    num_training_samples = []
    for i in range(len(acc)):
        num_training_samples.append(i * train_data.batch_size)

    # Create a plot
    plt.figure(figsize=(12, 6))
    plt.plot(num_training_samples, acc, label='Training Accuracy')
    plt.plot(num_training_samples, val_acc, label='Validation Accuracy')
    plt.title('Model Accuracy vs. Training Data')
    plt.xlabel('Number of Training Samples')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

# Now you can call this function with your history object
plot_accuracy_vs_training_data(history)