import numpy as np

from Game import tetris, tetromino

LINE_POINT_DICT = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}


class MoveFinder:
    def __init__(self, board_obj: tetris.TetrisBoard):
        self.board_obj = board_obj
        self.board = self.generate_board()
        self.board_temp = self.board

        self.column_heights_temp = self.find_column_heights(self.board_temp)

        self.tetris_streak_from_own_moves = (
            False  # TODO remember to remove this line, or implement next move knowledge
        )

        self.allowed_locations: list[tuple[np.ndarray[int, int], int, list[int]]] = []
        self.active_piece_grid: np.ndarray = board_obj.active_piece.base_rotation_grid
        self.active_piece_squares = np.array(np.nonzero(self.active_piece_grid)).T
        self.active_piece_code = self.board_obj.active_piece.tetromino_code

        self.valued_moves: list[
            tuple[tuple[np.ndarray[int, int], int, list[int]], np.ndarray[float]]
        ] = []

    def find_surface_pieces(self, is_hold: bool):
        self.allowed_locations = []
        right_bottom_edges = np.max(self.active_piece_squares, axis=0)
        max_right_relative = right_bottom_edges[0]
        max_height_relative = right_bottom_edges[1]
        max_left_relative = np.min(self.active_piece_squares, axis=0)[0]

        self.board = self.generate_board()

        column_heights = self.find_column_heights(self.board)
        column_heights.append(20)

        move_path = []
        if is_hold:
            move_path = [7]

        asymmetrical_rotations = 4
        if self.active_piece_code in [1, 5, 7]:
            asymmetrical_rotations = 2
        elif self.active_piece_code == 4:
            asymmetrical_rotations = 1

        for rotation in range(4):
            rotation_commands = [rotation] if rotation != 2 else [1, 1]

            for x in range(-max_left_relative, 10 - max_right_relative):
                coords = np.array(
                    [
                        x,
                        np.min(
                            column_heights[
                                x + max_left_relative : x + max_right_relative + 1
                            ]
                        )
                        - max_height_relative,
                    ]
                )
                # The +1 after max_right_reduction is because indexes arent inclusive at the end
                # ie: arr[0:1] returns one value
                coords += [0, 1]
                while not self.check_collision(
                    squares=coords + self.active_piece_squares
                ):
                    coords += [0, 1]
                coords -= [0, 1]

                move_path = []
                if is_hold:
                    move_path = [7]

                if x < 3:
                    move_path += rotation_commands + [5 for _ in range(3 - x)] + [4]
                else:
                    move_path += rotation_commands + [6 for _ in range(x - 3)] + [4]
                # move_path gives the instruction on how to get to the given coord

                self.allowed_locations.append((coords, rotation, move_path))

            self.active_piece_grid = np.rot90(self.active_piece_grid)
            self.active_piece_squares = np.array(np.nonzero(self.active_piece_grid)).T

            right_bottom_edges = np.max(self.active_piece_squares, axis=0)
            max_right_relative = right_bottom_edges[0]
            max_height_relative = right_bottom_edges[1]
            max_left_relative = np.min(self.active_piece_squares, axis=0)[0]

    def update_piece(self, piece: tetromino.Tetromino):
        self.active_piece_grid: np.ndarray = piece.base_rotation_grid
        self.active_piece_squares = np.array(np.nonzero(self.active_piece_grid)).T
        self.active_piece_code = piece.tetromino_code

    def check_collision(self, squares: np.ndarray):
        """Tests for collision between the given squares and the board, returns true if colliding and false if not"""
        for coords in squares:
            if self.board[coords[0]][coords[1]]:
                return True
        return False

    def generate_board(self):
        grid_board = np.zeros((10, 21), dtype="bool")

        for coord in self.board_obj.occupied_squares:
            grid_board[coord[0]][coord[1]] = True
        return grid_board

    def add_piece_to_board_temp_from_board(self, placement: tuple[np.ndarray, int]):
        self.board_temp = np.copy(self.board)

        # These next two lines are used instead of simply self.active_piece_squares because we want to rotate the piece
        piece_grid = np.rot90(self.active_piece_grid, k=placement[1])
        place_squares = np.array(np.nonzero(piece_grid)).T

        coords = placement[0]
        for relative_coords in place_squares:
            self.board_temp[coords[0] + relative_coords[0]][
                coords[1] + relative_coords[1]
            ] = True

        self.column_heights_temp = self.find_column_heights(self.board_temp)

    def get_points(self, streak: bool):
        board = self.board_temp.T  # Notice this line
        lines = -1

        for row in board:
            if np.all(row):
                lines += 1

        points = LINE_POINT_DICT.get(lines)
        if lines == 4:
            if streak:
                points *= 1.5
            self.tetris_streak_from_own_moves = True  # TODO remember to remove this line, or implement next piece knowledge
        else:
            self.tetris_streak_from_own_moves = False  # TODO remember to remove this line, or implement next piece knowledge

        return points

    def get_bumpiness_and_cliffs(
        self,
    ):  # Cliffs are 3-block tall height differences, no need to make a new function just for them
        bumpiness = 0
        cliffs = 0
        index_adjuster = (
            0.5 if self.column_heights_temp[0] < self.column_heights_temp[9] else -0.5
        )
        start = int(round(0.5 + index_adjuster))
        end = int(round(8.5 + index_adjuster))

        for index in range(start, end):
            difference = (
                self.column_heights_temp[index] - self.column_heights_temp[index + 1]
            )
            bumpiness += difference**2
            if difference >= 3:
                cliffs += difference / 3

        if index_adjuster == 0.5:
            difference = self.column_heights_temp[0] - self.column_heights_temp[1]
            if difference > 0:
                bumpiness += difference**2
                if difference >= 3:
                    cliffs += difference / 3
        else:
            difference = self.column_heights_temp[9] - self.column_heights_temp[8]
            if difference > 0:
                bumpiness += difference**2
                if difference >= 3:
                    cliffs += difference / 3

        return [bumpiness, cliffs]

    def get_maxH(self):
        return np.min(self.column_heights_temp)

    def get_avgH(self):
        return np.sum(self.column_heights_temp) / 10

    def get_holes(self):
        holes = 0

        for layer in range(1, 20):
            for column in range(0, 10):
                if (
                    not self.board_temp[column][layer]
                    and self.board_temp[column][layer - 1]
                ):
                    holes += 1
                    break

        return holes

    def generate_values_for_active_piece(self):
        k = 20  # the smaller k is, the larger the "sensitivity" for bumpiness + cliffs is

        values_part = []

        for position in self.allowed_locations:
            self.add_piece_to_board_temp_from_board(position[0:2])
            bumpiness_and_cliffs = self.get_bumpiness_and_cliffs()

            values = np.array(
                [
                    self.get_points(self.board_obj.tetris_streak) / 800,  # Points
                    np.exp((bumpiness_and_cliffs[0] - k) / k),  # Bumpiness
                    bumpiness_and_cliffs[1] / 10,  # Cliffs
                    (20 - self.get_maxH()) / 20,  # Max Height
                    (20 - self.get_avgH())
                    / 20,  # Average Height TODO Average height doesn't matter
                    self.get_holes(),
                ],
                dtype=float,
            )  # Holes

            values_part.append(values)

        return values_part

    def generate_inputs_from_all_positions(self):
        """Generates the parameters from all the positions. Said parameters will be sent to the as inputs AI to evaluate the position"""
        """
        A few different designs are possible here, one where the function appends the position + evaluations to
        self.valued_moves, you append the position + evaluation and the way to get there, which is incredibly memory expensive.
        And there is a completely different approach in which instead of appending to self.valued_moves, the function
        uses a generator that returns the position + evaluation + the way to get there, and the AI calculates every move
        one at a time, and keeps the best move. Which is more CPU heavy
        """
        self.board = self.generate_board()
        self.update_piece(self.board_obj.active_piece)
        self.find_surface_pieces(is_hold=False)

        allowed_locations = self.allowed_locations

        self.valued_moves = []
        values_part = self.generate_values_for_active_piece()

        if self.board_obj.allowed_hold:
            if self.board_obj.hold:
                alternative_piece = self.board_obj.hold
            else:
                alternative_piece = self.board_obj.next

            self.update_piece(alternative_piece)
            self.find_surface_pieces(is_hold=True)

            # The value of self.allowed_locations is changed by self.find_surface_pieces
            allowed_locations += self.allowed_locations

            values_part += self.generate_values_for_active_piece()

        self.valued_moves = [allowed_locations, values_part]

    @staticmethod
    def find_column_heights(board):
        column_heights = []
        for column in board:
            height = 0
            for square in column:
                if not square:
                    height += 1
                else:
                    break

            # They dont reach height - 1, they reach height, but its simpler to calculate things this way
            column_heights.append(height - 1)
        return column_heights
