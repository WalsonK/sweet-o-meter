import os.path
from typing import List
import numpy as np
import json
from numba import jit


class MLP:
    def __init__(self, npl: List[int]):
        self.neuron_per_layer = npl
        self.layers = len(npl) - 1
        self.weights = []
        self.neuron_data = []
        self.deltas = []

        # Weights Initialisation
        for layer in range(self.layers + 1):
            self.weights.append([])
            if layer == 0:
                continue
            for i in range(self.neuron_per_layer[layer - 1] + 1):
                self.weights[layer].append([])
                for j in range(self.neuron_per_layer[layer] + 1):
                    self.weights[layer][i].append(0.0 if j == 0 else np.random.uniform(-1.0, 1.0))

        # Neuron data Initialisation
        for layer in range(self.layers + 1):
            self.neuron_data.append([])
            for j in range(self.neuron_per_layer[layer] + 1):
                self.neuron_data[layer].append(1.0 if j == 0 else 0.0)

        # Deltas Initialisation
        for layer in range(self.layers + 1):
            self.deltas.append([])
            for j in range(self.neuron_per_layer[layer] + 1):
                self.deltas[layer].append(0.0)

    def propagate(self, inputs: List[float], is_classification: bool):
        # Fill inputs
        for i in range(self.neuron_per_layer[0]):
            self.neuron_data[0][i + 1] = inputs[i]

        # Update neuron output, layer after layer
        for layer in range(1, self.layers + 1):
            for j in range(1, self.neuron_per_layer[layer] + 1):
                total = 0.0
                for i in range(0, self.neuron_per_layer[layer - 1] + 1):
                    total += self.weights[layer][i][j] * self.neuron_data[layer - 1][i]

                if layer < self.layers or is_classification:
                    total = np.tanh(total)

                self.neuron_data[layer][j] = total

    def predict(self, inputs: List[float], is_classification: bool) -> List[float]:
        self.propagate(inputs, is_classification)
        return self.neuron_data[self.layers][1:]

    def fit(self, all_inputs: List[List[float]], expected_outputs: List[List[float]],
            is_classification: bool, iteration: int, learning_rate: float):
        data = {"loss": [], "accuracy": []}
        accuracy_data = {"correct_predict": 0, "data": []}

        for _ in range(iteration):
            rand = np.random.randint(0, len(all_inputs))
            rand_inputs = all_inputs[rand]
            rand_outputs = expected_outputs[rand]

            self.propagate(rand_inputs, is_classification)

            # Calc semi gradient last layer
            for j in range(1, self.neuron_per_layer[self.layers] + 1):
                self.deltas[self.layers][j] = (self.neuron_data[self.layers][j] - rand_outputs[j - 1])
                if is_classification:
                    self.deltas[self.layers][j] *= (1 - self.neuron_data[self.layers][j] ** 2)

            # Calc other layer
            for layer in reversed(range(1, self.layers + 1)):
                for i in range(1, self.neuron_per_layer[layer - 1] + 1):
                    total = 0.0
                    for j in range(1, self.neuron_per_layer[layer] + 1):
                        total += self.weights[layer][i][j] * self.deltas[layer][j]
                    self.deltas[layer - 1][i] = (1 - self.neuron_data[layer - 1][i] ** 2) * total

            # Update Weights
            for layer in range(1, self.layers + 1):
                for i in range(0, self.neuron_per_layer[layer - 1] + 1):
                    for j in range(1, self.neuron_per_layer[layer] + 1):
                        self.weights[layer][i][j] -= learning_rate * self.neuron_data[layer - 1][i] * self.deltas[layer][j]

            # Calc of loss
            predicted = self.predict(rand_inputs, is_classification)
            data['loss'].append(mean_squared_error(np.array(rand_outputs), np.array(predicted)))
            # Calc of accuracy
            data["accuracy"].append(categorical_accuracy(predicted, rand_outputs, accuracy_data))

        return data

    def save(self, filename: str):
        data = {
          "neuron_per_layer": self.neuron_per_layer,
          "layers": self.layers,
          "weights": self.weights,
          "neuron_data": self.neuron_data,
          "deltas": self.deltas
        }

        filename += ".json"
        folder_path = "./Data/models"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        path = os.path.join(folder_path, filename)

        with open(path, 'w') as json_file:
            json.dump(data, json_file)

    def load(self, file_path):
        if not os.path.exists(file_path):
            raise Exception("Le fichier JSON n'existe pas : " + file_path)

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            self.neuron_per_layer = data['neuron_per_layer']
            self.layers = data['layers']
            self.weights = data['weights']
            self.neuron_data = data['neuron_data']
            self.deltas = data['deltas']

    def print_mlp(self):
        print(f"PMC : layers : {self.layers}")
        print(f"PMC : n per layer len : {len(self.neuron_per_layer)}")
        for i in range(len(self.neuron_per_layer)):
            print(f"PMC : layer[{i}] : {self.neuron_per_layer[i]}")

        print("PMC: Weights len :", len(self.weights))
        for layer in range(self.layers):
            for i in range(len(self.weights[layer])):
                for j in range(len(self.weights[layer][i])):
                    print(f"-- weights[{layer}][{i}][{j}]: {self.weights[layer][i][j]}")

        # Neurons res
        print(f"PMC: Neuron data len : {len(self.neuron_data)}")
        for i in range(len(self.neuron_data)):
            for j in range(len(self.neuron_data[i])):
                print(f"-- neuronData[{i}][{j}]: {self.neuron_data[i][j]}")

        # Deltas
        print(f"PMC: deltas len : {len(self.deltas)}")
        for i in range(len(self.deltas)):
            for j in range(len(self.deltas[i])):
                print(f"- deltas[{i}][{j}]: {self.deltas[i][j]}")


@jit(nopython=True)
def mean_squared_error(correct: np.ndarray, predict: np.ndarray):
    return np.sum((correct - predict)**2) / len(correct)


@jit(nopython=True)
def cross_entropy_loss(correct, predict):
    epsilon = 1e-15
    return - np.sum(correct * np.log(predict + epsilon))


def categorical_accuracy(predictions: List[float], corrects: List[float], accuracy_data: dict):
    predicted_class = np.argmax(predictions)
    true_class = np.argmax(corrects)

    if predicted_class == true_class:
        accuracy_data['correct_predict'] += 1

    if len(accuracy_data['data']) == 0:
        accuracy_data['data'].append(0)

    accuracy = accuracy_data['correct_predict'] / len(accuracy_data['data'])
    accuracy_data['data'].append(accuracy)
    return accuracy
