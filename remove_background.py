import concurrent.futures
from rembg import remove
import os
import shutil

def remove_background(file_path, output_folder):
    if file_path.endswith('.png') or file_path.endswith('.jpg') and os.path.basename(file_path) not in os.listdir(output_folder):
        output_path = os.path.join(output_folder, os.path.basename(file_path))

        # Entfernen des Hintergrundes des Bildes
        with open(file_path, 'rb') as input_image:
            bg_removed_image = remove(input_image.read())

        # Speichern des Bildes mit entferntem Hintergrund im output_folder
        with open(output_path, 'wb') as output_image:
            output_image.write(bg_removed_image)

def process_images(input_folder, output_folder):
    # Erstellen des Ausgabeverzeichnises, falls es noch nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Durchsuchen des Eingabeordner nach allen Dateien
    file_paths = [os.path.join(input_folder, file) for file in os.listdir(input_folder)
                 if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Verarbeiten alle Bilder gleichzeitig
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda file_path: remove_background(file_path, output_folder), file_paths)


process_images("images/with_background/test/wolves", "images/removed_background/test/wolves")
process_images("images/with_background/train/wolves", "images/removed_background/train/wolves")
process_images("images/with_background/test/dogs", "images/removed_background/test/dogs")
process_images("images/with_background/train/dogs", "images/removed_background/train/dogs")
process_images("images/with_background/test/other", "images/removed_background/test/other")
process_images("images/with_background/train/other", "images/removed_background/train/other")