from rembg import remove
import os
import shutil

def remove_backgrounds(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Entferne den Hintergrund des Bildes
            with open(input_path, 'rb') as input_image:
                bg_removed_image = remove(input_image.read())

            # Speichere das Bild mit entferntem Hintergrund im output_folder
            with open(output_path, 'wb') as output_image:
                output_image.write(bg_removed_image)

remove_backgrounds("images/with_background/train/dogs", "images/removed_background/train/dogs")
remove_backgrounds("images/with_background/train/wolves", "images/removed_background/train/wolves")
remove_backgrounds("images/with_background/test/dogs", "images/removed_background/test/dogs")
remove_backgrounds("images/with_background/test/wolves", "images/removed_background/test/wolves")