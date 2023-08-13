import os.path

from Python_Library.library import MLP
from Utils.tools import image_to_matrix
import matplotlib.pyplot as plt

folder = "./Data/Datasets/15x15"

inputs = []
outputs = []

# Churros : 5 946 | Apple_candy : 7 330 | Cotton_candy : 6 309

for i in range(3):
    if i == 0:
        folder = "./Data/Datasets/15x15/Churros"
        for y in range(1, 5947):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                inputs.append(image_to_matrix(file, True))
                outputs.append([1., -1., -1.])

    if i == 1:
        folder = "./Data/Datasets/15x15/Apple_candy"
        for y in range(1, 7331):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                inputs.append(image_to_matrix(file, True))
                outputs.append([-1., 1., -1.])

    if i == 2:
        folder = "./Data/Datasets/15x15/Cotton_candy"
        for y in range(1, 6310):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                inputs.append(image_to_matrix(file, True))
                outputs.append([-1., -1., 1.])

print(f"------------------------\n Data Loaded : {len(inputs)} \n------------------------")


model = MLP([225, 10, 3])

print(f"------------------------\n Training Start \n------------------------")
data = model.fit(inputs, outputs, True, 100, 0.01)

print(f"------------------------\n Accuracy : {data['accuracy'][-1]} \n------------------------")
plt.plot(range(len(data['accuracy'])), data['accuracy'], label='Droit de l\'accuracy')
plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.title('Evolution of the accuracy')
plt.legend()
plt.grid()
plt.show()

plt.plot(range(len(data['loss'])), data['loss'], label='Droit du loss')
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.title('Evolution of the loss')
plt.legend()
plt.grid()
plt.show()





