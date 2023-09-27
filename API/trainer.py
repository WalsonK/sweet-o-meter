import os.path

from Python_Library.library import MLP
from Utils.tools import image_to_matrix
import matplotlib.pyplot as plt

folder = "./Data/Datasets/20x20"

inputs = []
outputs = []
validation = ([], [])

# Churros : 18 527 | Apple_candy : 19 951 | Cotton_candy : 20 988
# Pour validation
# Churros : 2 058 | Apple_candy : 1 898 | Cotton_candy : 2 333

for i in range(3):
    if i == 0:
        folder = "./Data/Datasets/25x25/Churros"
        for y in range(1, 18528):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                inputs.append(image_to_matrix(file, False))
                outputs.append([1., -1., -1.])
        folder = "./Data/Datasets/25x25/Churros_validation"
        for y in range(1, 2059):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                validation[0].append(image_to_matrix(file, False))
                validation[1].append([1., -1., -1.])

    if i == 1:
        folder = "./Data/Datasets/25x25/Apple_candy"
        for y in range(1, 19952):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                inputs.append(image_to_matrix(file, False))
                outputs.append([-1., 1., -1.])
        folder = "./Data/Datasets/25x25/Apple_candy_validation"
        for y in range(1, 1899):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                validation[0].append(image_to_matrix(file, False))
                validation[1].append([-1., 1., -1.])

    if i == 2:
        folder = "./Data/Datasets/25x25/Cotton_candy"
        for y in range(1, 20989):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                inputs.append(image_to_matrix(file, False))
                outputs.append([-1., -1., 1.])
        folder = "./Data/Datasets/25x25/Cotton_candy_validation"
        for y in range(1, 2334):
            file = os.path.join(folder, f"image_{y}.jpg")
            if not os.path.exists(file):
                print(f"File : {file} n'existe pas")
            else:
                validation[0].append(image_to_matrix(file, False))
                validation[1].append([-1., -1., 1.])

print(f"------------------------\n Data Loaded : {len(inputs)} \n------------------------")


model = MLP([1875, 128, 64, 3])

print(f"------------------------\n Training Start \n------------------------")
data = model.fit(inputs, outputs, validation, True, 100, 0.002)

print(f"------------------------\n Accuracy : {round(sum(data['accuracy']) / len(data['accuracy']), 3)} ")
print(f"Test Accuracy : {round(sum(data['validation_accuracy']) / len(data['validation_accuracy']), 3)} \n"
      f"------------------------")
plt.plot(range(len(data['accuracy'])), data['accuracy'], label='Train')
plt.ylim(0.0, 1.0)
plt.plot(range(len(data['validation_accuracy'])), data['validation_accuracy'], label='Test', color='orange')
plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.title('Evolution of the accuracy')
plt.legend()
plt.grid()
plt.show()

plt.plot(range(len(data['loss'])), data['loss'], label='Train', color='blue')
plt.plot(range(len(data['validation_loss'])), data['validation_loss'], label='Test', color='orange')
plt.ylim(0.0, 6.0)
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.title('Evolution of the loss')
plt.legend()
plt.grid()
plt.show()

model.save("model1")





