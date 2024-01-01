from PIL import Image, ImageDraw
import random
import os

# Funktion zum Erstellen eines Bildes
def create_image(with_horizontal, with_vertical):
    width, height = 200, 200
    image = Image.new('RGB', (width, height), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)

    if with_horizontal:
        h = random.randint(0, height)
        x1, y1 = random.randint(0, width), h
        x2, y2 = random.randint(0, width), h
        draw.line([(x1, y1), (x2, y2)], fill = (0, 0, 0))

    if with_vertical:
        w = random.randint(0, width)
        x1, y1 = w, random.randint(0, height)
        x2, y2 = w, random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill = (0, 0, 0))

    return image

# Funktion zum Erstellen von Bildern
def create_images(count_train, count_test):
    # Erstellen Sie die erforderlichen Verzeichnisse
    if not os.path.exists('images/test/with_horizontal'):
        os.makedirs('images/test/with_horizontal')

    if not os.path.exists('images/test/with_vertical'):
        os.makedirs('images/test/with_vertical')

    if not os.path.exists('images/train/with_horizontal'):
        os.makedirs('images/train/with_horizontal')

    if not os.path.exists('images/train/with_vertical'):
        os.makedirs('images/train/with_vertical')

    for i in range(count_train):
        image_horizontal = create_image(True, False)
        image_horizontal.save(f'images/train/with_horizontal/{i}.jpg')

        image_vertical = create_image(False, True)
        image_vertical.save(f'images/train/with_vertical/{i}.jpg')
    for i in range(count_test):
        image_horizontal = create_image(True, False)
        image_horizontal.save(f'images/test/with_horizontal/{i}.jpg')

        image_vertical = create_image(False, True)
        image_vertical.save(f'images/test/with_vertical/{i}.jpg')

create_images(1000, 100)