import os
import base64
from PIL import Image
from io import BytesIO
import numpy as np
from numpy import ndarray


def recompose_png_to_jpg(base64_string: str):
    image_bytes = base64.b64decode(base64_string)

    png_image = Image.open(BytesIO(image_bytes))

    folder_path = "./Data"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    path = os.path.join(folder_path, "predict_image.jpg")

    png_image.convert('RGB').save(path, format='JPEG')

    return path


def resizer(path, size=(50, 50)):
    image = Image.open(path)
    resized = image.resize(size)
    resized.save(path)


def image_to_matrix(file_path: str, is_grey: bool) -> list:
    image = Image.open(file_path)
    if is_grey:
        grey_image = image.convert("L")
        matrix = np.array(grey_image)
    else:
        matrix = np.array(image)

    return list((matrix / 255.0).flatten())
