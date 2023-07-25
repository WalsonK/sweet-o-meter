import os
import numpy as np
from numpy import ndarray
from PIL import Image


def png_to_matrix(file_path: str) -> ndarray:
    absolute_path = os.path.abspath(file_path)
    image = Image.open(absolute_path)
    grey_image = image.convert("L")
    matrix = np.array(grey_image)
    return (matrix / 255.0).flatten()


test = png_to_matrix("/Users/walson/Documents/Cours/Rattrapage "
                     "PA/sweetometer/sweet-o-meter/API/Data/Datasets/50x50/Churros/image_1.jpg")

print(test)
print(len(test))
