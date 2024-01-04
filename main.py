import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# Bildverarbeitungs-Generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
model.add(MaxPooling2D(32))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dense(512, activation="relu"))
model.add(Dense(256, activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

# Kompiliere das Modell
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])



print(model.summary())

# Generieren und laden Sie das Training-Dataset
train_generator = train_datagen.flow_from_directory(
    'images/edges/train',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

# Generieren und laden Sie das Test-Dataset
test_generator = test_datagen.flow_from_directory(
    'images/edges/test',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

# Trainieren Sie das Modell
history = model.fit(train_generator, epochs=10, validation_data=test_generator)

def plot_accuracy_vs_training_data(history):
    # Extract the accuracy values from the history
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    # Compute the number of training examples used at each epoch
    num_training_samples = []
    for i in range(len(acc)):
        num_training_samples.append(i * 32)

    # Create a plot
    plt.figure(figsize=(12, 6))
    plt.plot(num_training_samples, acc, label='Training Accuracy')
    plt.plot(num_training_samples, val_acc, label='Validation Accuracy')
    plt.title('Model Accuracy vs. Training Data')
    plt.xlabel('Number of Training Samples')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

plot_accuracy_vs_training_data(history)