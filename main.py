import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy

# Bildverarbeitungs-Generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

# Erstellen Sie das Sequential-Modell
model = Sequential()
model.add(VGG16(weights='imagenet', include_top=False, input_shape=(200, 200, 3)))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

# Kompilieren Sie das Modell
model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=['accuracy'])

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
history = model.fit(
    train_generator,
    steps_per_epoch=np.ceil(1000/32),
    epochs=20,
    validation_data=test_generator,
    validation_steps=np.ceil(800/32))

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

plot_accuracy_vs_training_data(history)