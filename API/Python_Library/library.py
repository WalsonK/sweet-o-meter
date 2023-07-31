from typing import List
import numpy as np
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

    def predict(self, inputs: List[float], is_classification: bool):
        self.propagate(inputs, is_classification)
        return self.neuron_data[self.layers][1:]

    def fit(self, all_inputs: List[List[float]], expected_outputs: List[List[float]],
            is_classification: bool, iteration: int, learning_rate: float):
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
