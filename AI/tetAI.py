from __future__ import annotations
from typing import Union
import numpy as np

from AI import moveFinder

N_INPUTS = 6
LAYER1_NEURONS = 10


class TetAI:
    def __init__(
        self,
        board,
        parents: Union[None, list[TetAI]],
        max_mutation: float,
        mutation_chance: int,
    ):
        self.max_mutation = max_mutation
        self.gene_stability = 100 - mutation_chance

        self.input_generator = moveFinder.MoveFinder(board_obj=board)

        self.valued_moves: np.ndarray[
            tuple[
                tuple[np.ndarray[int, int], int],
                np.ndarray[float, float, float, float, float, float],
            ]
        ]

        self.possible_moves: np.ndarray[tuple[np.ndarray[int, int], int]]
        self.inputs: np.ndarray[list[float, float, float, float, float, float]]

        self.decision: tuple[np.ndarray[int, int], int]

        self.layer1 = Layer(
            n_inputs=N_INPUTS, n_neurons=LAYER1_NEURONS, activation_function="ReLU"
        )
        self.output_layer = Layer(
            n_inputs=LAYER1_NEURONS, n_neurons=1, activation_function="None"
        )

        if parents is not None:
            self.parents: list[TetAI] = parents
            if len(parents) == 2:
                parent0 = self.parents[0]
                parent1 = self.parents[1]

                self.layer1.weights = self.combine_wirings(
                    [parent0.layer1.weights, parent1.layer1.weights]
                )
                self.layer1.biases = self.combine_wirings(
                    [parent0.layer1.biases, parent1.layer1.biases]
                )

                self.output_layer.weights = self.combine_wirings(
                    [parent0.output_layer.weights, parent1.output_layer.weights]
                )
                self.output_layer.biases = self.combine_wirings(
                    [parent0.output_layer.biases, parent1.output_layer.biases]
                )
            else:
                self.layer1.weights = self.parents[
                    0
                ].layer1.weights + self.randomize_mutation(self.layer1.weights.shape)
                self.layer1.biases = self.parents[
                    0
                ].layer1.biases + self.randomize_mutation(self.layer1.biases.shape)

                self.output_layer.weights = self.parents[
                    0
                ].output_layer.weights + self.randomize_mutation(
                    self.output_layer.weights.shape
                )
                self.output_layer.biases = self.parents[
                    0
                ].output_layer.biases + self.randomize_mutation(
                    self.output_layer.biases.shape
                )

    def fire_up(self):
        """
        Forms a decision based on the current state of the board and the
        active piece.
        """
        self.input_generator.generate_inputs_from_all_positions()

        self.valued_moves = self.input_generator.valued_moves

        self.possible_moves = np.array(self.valued_moves[0], dtype=object)
        self.inputs = np.array(self.valued_moves[1], dtype=float)

        self.layer1.forward(inputs=self.inputs)

        self.output_layer.forward(self.layer1.output)

        self.decision = self.possible_moves[np.argmax(self.output_layer.output)]

    def randomize_mutation(self, shape: Union[tuple, list, np.ndarray]):
        adjusted_stability = self.gene_stability * 2
        mutation = np.zeros(shape)
        shape_d = len(shape)

        if shape_d == 2:
            for row in range(len(mutation)):
                for column in range(len(mutation[0])):
                    randomizer = np.random.randint(1, 200)

                    if randomizer > adjusted_stability:
                        mutation[row][column] = (
                            2 * self.max_mutation * np.random.random()
                            - self.max_mutation
                        )
        else:
            for index in range(shape_d):
                randomizer = np.random.randint(1, 200)

                if randomizer > adjusted_stability:
                    mutation[index] = (
                        2 * self.max_mutation * np.random.random() - self.max_mutation
                    )

        return mutation

    @staticmethod
    def combine_wirings(parents_layer_matrices: list[np.ndarray, np.ndarray]):
        shape = parents_layer_matrices[0].shape

        randomizer = np.random.randint(low=0, high=2, size=shape)
        new_wiring = np.zeros(shape)

        if len(shape) == 2:
            for row in range(shape[0]):
                for column in range(shape[1]):
                    new_wiring[row][column] = parents_layer_matrices[
                        randomizer[row][column]
                    ][row][column]
        else:
            for index in range(shape[0]):
                new_wiring[index] = parents_layer_matrices[randomizer[index]][index]

        return new_wiring


class Layer:
    def __init__(self, n_inputs: int, n_neurons: int, activation_function: str):
        self.weights: np.ndarray = np.maximum(
            np.minimum(0.3 * np.random.randn(n_inputs, n_neurons), 1), -1
        )
        self.biases = np.zeros(n_neurons)
        self.activation_function_type = activation_function

    def forward(self, inputs: np.ndarray):
        self.output = np.dot(a=inputs, b=self.weights) + self.biases

        if self.activation_function_type == "ReLU":
            self.output = np.maximum(self.output, 0)

        elif self.activation_function_type == "softmax":
            exp_values = np.exp(self.output - np.max(self.output))
            probabilities = exp_values / np.sum(exp_values)
            self.output = probabilities

        elif (
            self.activation_function_type == "None"
        ):  # Not needed at all, but here just to make things more orderly
            pass
