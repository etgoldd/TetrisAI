import numpy as np


class Tetromino:

    def __init__(self, tetromino_code: int):
        self.tetromino_code = tetromino_code
        self.coords = np.array([3, 0])
        base_rotation_grid_mappings = \
            {1: np.array([
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]).T,
             2: np.array([
                 [2, 0, 0],
                 [2, 2, 2],
                 [0, 0, 0]]).T,

             3: np.array([
                 [0, 0, 3],
                 [3, 3, 3],
                 [0, 0, 0]]).T,

             4: np.array([
                 [4, 4],
                 [4, 4]]),

             5: np.array([
                 [0, 5, 5],
                 [5, 5, 0],
                 [0, 0, 0]]).T,

             6: np.array([
                 [0, 6, 0],
                 [6, 6, 6],
                 [0, 0, 0]]).T,

             7: np.array([
                 [7, 7, 0],
                 [0, 7, 7],
                 [0, 0, 0]]).T}

        self.base_rotation_grid = np.copy(base_rotation_grid_mappings.get(self.tetromino_code))

        self.rotation_grid = base_rotation_grid_mappings.get(self.tetromino_code)
        self.rot_number = 0

        self.occupying_squares: np.ndarray = self.coords + np.array(np.nonzero(a=self.rotation_grid)).T
        """
        the relative location of the different squares that make up the tetromino are found using the first part,
        and is then offset by the coords
        """
        self.rightmost_edge_relative_to_coords = np.max(self.occupying_squares, axis=0)[0] - self.coords[0]
        self.leftmost_edge_relative_to_coords = np.min(self.occupying_squares, axis=0)[0] - self.coords[0]

        self.base_rotation_left_edge = self.leftmost_edge_relative_to_coords
        self.base_rotation_right_edge = self.rightmost_edge_relative_to_coords

        self.ghost = Ghost(self)

    def update_location(self):
        self.occupying_squares = self.coords + np.array(np.nonzero(a=self.rotation_grid)).T

    def update_edge(self):
        self.rightmost_edge_relative_to_coords = np.max(self.occupying_squares, axis=0)[0] - self.coords[0]
        self.leftmost_edge_relative_to_coords = np.min(self.occupying_squares, axis=0)[0] - self.coords[0]


class Ghost:

    def __init__(self, piece: Tetromino):
        self.piece = piece
        self.occupying_squares = self.piece.occupying_squares

    def reset_location_to_piece(self):
        self.occupying_squares = np.copy(self.piece.occupying_squares)
