# filename: rsz.py
# goal: This script resizes an image to 1000x1000 while preserving the aspect ratio.
#       If the input image is not valid, it logs an error message and returns the original image unchanged.
#       If the image a contient un canal alpha (transparence), on l'aplatit sur un fond blanc.

import argparse
import shutil
from PIL import Image, UnidentifiedImageError

def resize_image_to_square(input_path, output_path, size=1000):
    try:
        original_image = Image.open(input_path)
    except UnidentifiedImageError:
        print(f"Erreur : le fichier {input_path} n'est pas une image valide. Renvoi de l'image d'origine.")
        shutil.copy(input_path, output_path)
        return

    # Convertir l'image en RGBA si elle est en palette (mode 'P')
    if original_image.mode == 'P':
        original_image = original_image.convert("RGBA")

    # Si l'image possède un canal alpha (ex. RGBA), on l'aplatit sur un fond blanc
    if original_image.mode == "RGBA":
        # Créer une image de fond blanc
        background = Image.new("RGB", original_image.size, (255, 255, 255))
        # Copier l'image originale dessus en utilisant l'alpha comme masque
        background.paste(original_image, mask=original_image.split()[3])
        original_image = background

    # Récupérer la taille initiale
    original_width, original_height = original_image.size
    # Calculer le ratio de redimensionnement pour conserver l'aspect ratio
    ratio = min(size / original_width, size / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # Redimensionner l'image
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

    # Créer une nouvelle image carrée (fond blanc) de taille cible
    final_image = Image.new("RGB", (size, size), (255, 255, 255))

    # Calculer les offsets pour centrer l'image redimensionnée dans le carré
    offset_x = (size - new_width) // 2
    offset_y = (size - new_height) // 2

    # Coller l'image redimensionnée sur le fond blanc
    final_image.paste(resized_image, (offset_x, offset_y))

    # Sauvegarder l'image finale
    final_image.save(output_path)

def main():
    parser = argparse.ArgumentParser(
        description="Resize an image to 1000x1000 while preserving the aspect ratio."
    )
    parser.add_argument("input_image", help="Path to the input image file")
    parser.add_argument("output_image", help="Path to the output image file")
    args = parser.parse_args()
    resize_image_to_square(args.input_image, args.output_image, 1000)

if __name__ == "__main__":
    main()