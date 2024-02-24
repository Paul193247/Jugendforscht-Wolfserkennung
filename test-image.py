from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image, ImageFilter
from rembg import remove

model = load_model("model.h5")


img = Image.open("img.jpeg")
img = remove(img)
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
img.save("img2.jpg")

img = image.load_img("img2.jpg", target_size=(256, 256))

img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

print("loaded photo")

predictions = model.predict(img_array)

print("Vorhersagen:", predictions)
class_labels = {'dogs': 0, 'wolves': 1}
predicted_class = np.argmax(predictions)
predicted_label = [k for k, v in class_labels.items() if v == predicted_class][0]
print("Vorhergesagte Klasse:", predicted_label)