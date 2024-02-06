import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv2D, MaxPooling2D
import matplotlib.pyplot as plt
from sendmessage import sendmessage

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



model = Sequential([Conv2D(30, (3, 3), activation='relu', input_shape=(256, 256, 3)),
                    MaxPooling2D(2, 2), 
                    Conv2D(64, (3, 3), activation='relu'),
                    MaxPooling2D(2, 2), 
                    Flatten(),
                    Dense(750, activation='relu'),
                    Dense(2, activation='softmax')])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])



print(model.summary())

# Generieren und laden des Training-Datasets
train_generator = train_datagen.flow_from_directory(
    'images/edges/train',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary')

# Generieren und laden des Test-Datasets
test_generator = test_datagen.flow_from_directory(
    'images/edges/test',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary')

# Trainieren des Modells
history = model.fit(train_generator, epochs=40, validation_data=test_generator)

def plot_accuracy_vs_training_data(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    num_training_samples = []
    for i in range(len(acc)):
        num_training_samples.append(i * 32)

    plt.figure(figsize=(12, 6))
    plt.plot(num_training_samples, acc, label='Training Accuracy')
    plt.plot(num_training_samples, val_acc, label='Validation Accuracy')
    plt.title('Model Accuracy vs. Training Data')
    plt.xlabel('Number of Training Samples')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

sendmessage("Model ist fertig trainiert")
plot_accuracy_vs_training_data(history)