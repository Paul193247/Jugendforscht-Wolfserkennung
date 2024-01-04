import concurrent.futures
from rembg import remove
import os
import shutil

def remove_background(file_path, output_folder):
    if file_path.endswith('.png') or file_path.endswith('.jpg'):
        output_path = os.path.join(output_folder, os.path.basename(file_path))

        # Entferne den Hintergrund des Bildes
        with open(file_path, 'rb') as input_image:
            bg_removed_image = remove(input_image.read())

        # Speichere das Bild mit entferntem Hintergrund im output_folder
        with open(output_path, 'wb') as output_image:
            output_image.write(bg_removed_image)

def process_images(input_folder, output_folder):
    # Erstellen Sie den Ausgabeverzeichnis, falls es noch nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Durchsuchen Sie den Eingabeordner nach allen Dateien
    file_paths = [os.path.join(input_folder, file) for file in os.listdir(input_folder)
                 if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Verarbeiten Sie alle Bilder gleichzeitig
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda file_path: remove_background(file_path, output_folder), file_paths)


process_images("images/with_background/test/wolves", "images/removed_background/test/wolves")
process_images("../../Downloads/images.cv_4e0zrqh8ggu56aji8shqnm/data/train/white_wolf", "images/removed_background/train/wolves")