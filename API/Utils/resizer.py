from PIL import Image
import os


def resize_datasets(input_path, output_path, file_name, size=(50, 50)):
    try:
        absolut_input_path = os.path.abspath(input_path + file_name)
        if not os.path.exists(absolut_input_path):
            print(f"Le fichier {input_path + file_name} n'existe pas.")
            return

        image = Image.open(absolut_input_path)

        resized_image = image.resize(size)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        path = output_path + file_name
        resized_image.save(path)
        print(f"Saved : {file_name}")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")


for i in range(1, 2334):
    resize_datasets("../Data/Datasets/Originals/Cotton_candy/validation/", "../Data/Datasets/50x50/Cotton_candy_validation/", f"image_{i}.jpg",
                    size=(50, 50))
