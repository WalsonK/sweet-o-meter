from PIL import Image
import os


def resize_datasets(input_path, output_path, size=(50, 50)):
    try:
        absolut_input_path = os.path.abspath(input_path)
        if not os.path.exists(absolut_input_path):
            print(f"Le fichier {input_path} n'existe pas.")
            return

        image = Image.open(absolut_input_path)

        resized_image = image.resize(size)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        path = output_path + "/image_1.jpg"
        resized_image.save(path)

    except Exception as e:
        print(f"Une erreur est survenue : {e}")


resize_datasets("/Users/walson/Documents/Cours/Rattrapage PA/sweetometer/sweet-o-meter/API/Data/Datasets/Originals/"
                "Churros/Google/image_1.jpg", "../Data/Datasets/50x50/Churros")
