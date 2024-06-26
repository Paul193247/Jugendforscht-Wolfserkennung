import concurrent.futures
from PIL import Image, ImageFilter
import os

def process_image(file_path, output_folder):
    if os.path.exists(os.path.join(output_folder, file_name)):
        return
    image = Image.open(file_path)

    # Konvertieren Sie das Bild in Graustufen
    gray_image = image.convert('L')

    # Anwenden des Kantenfilters
    edge_image = gray_image.filter(ImageFilter.FIND_EDGES, radius=2)

    # Speichern Sie das bearbeitete Bild im Ausgabeverzeichnis
    file_name = os.path.basename(file_path)
    edge_image.save(os.path.join(output_folder, file_name))

def process_images(input_folder, output_folder):
    # Erstellen Sie den Ausgabeverzeichnis, falls es noch nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Durchsuchen Sie den Eingabeordner nach allen Dateien
    file_paths = [os.path.join(input_folder, file) for file in os.listdir(input_folder)
                 if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Verarbeiten Sie alle Bilder gleichzeitig
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda file_path: process_image(file_path, output_folder), file_paths)

process_images("images/with_background/test/wolves", "images/removed_background/test/wolves")
process_images("images/with_background/train/wolves", "images/removed_background/train/wolves")
process_images("images/with_background/test/dogs", "images/removed_background/test/dogs")
process_images("images/with_background/train/dogs", "images/removed_background/train/dogs")
process_images("images/with_background/test/other", "images/removed_background/test/other")
process_images("images/with_background/train/other", "images/removed_background/train/other")