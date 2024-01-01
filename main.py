import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten, Dense, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

# Bildverarbeitungs-Generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

base_model = MobileNetV2(weights='imagenet', include_top=False)

# Füge die erforderlichen Layer hinzu, um die Anzahl der Klassen anzupassen
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

# Erstelle das finale Modell
model = Model(inputs=base_model.input, outputs=predictions)

# Kompiliere das Modell
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print(model.summary())

# Generieren und laden Sie das Training-Dataset
train_generator = train_datagen.flow_from_directory(
    'images/train',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

# Generieren und laden Sie das Test-Dataset
test_generator = test_datagen.flow_from_directory(
    'images/test',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary')

# Trainieren Sie das Modell
history = model.fit(train_generator, epochs=20, validation_data=test_generator)

def plot_accuracy_vs_training_data(history):
    # Extract the accuracy values from the history
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    # Compute the number of training examples used at each epoch
    num_training_samples = []
    for i in range(len(acc)):
        num_training_samples.append(i * train_datagen.batch_size)

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