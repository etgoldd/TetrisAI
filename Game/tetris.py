import numpy as np
from typing import Optional

from Game import tetromino as pieces

JLSTZ_WALL_KICKS = {'0-1': [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                    '1-0': [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
                    '1-2': [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
                    '2-1': [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                    '2-3': [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    '3-2': [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                    '3-0': [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                    '0-3': [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]}

L_WALL_KICKS = {'0-1': [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
                '1-0': [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
                '1-2': [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
                '2-1': [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
                '2-3': [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
                '3-2': [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
                '3-0': [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
                '0-3': [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)]}

LINE_POINT_DICT = {1: 100,
                   2: 300,
                   3: 500,
                   4: 800}


class TetrisBoard:

    def __init__(self):
        self.first_bag = np.array([pieces.Tetromino(tetromino_code=code) for code in range(1, 8)],
                                  dtype=pieces.Tetromino)
        self.first_bag = self.random_generator(self.first_bag)
        self.next_bag = self.random_generator(np.array([pieces.Tetromino(tetromino_code=code) for code in range(1, 8)]))

        self.bag = np.append(arr=self.first_bag, values=self.next_bag)
        self.bag_index = 0

        self.active_piece: pieces.Tetromino = self.bag[self.bag_index]
        self.next: pieces.Tetromino = self.bag[self.bag_index + 1]
        self.hold: Optional[pieces.Tetromino] = None
        self.allowed_hold = True

        self.all_pieces = [self.active_piece]
        self.occupied_squares = [(column, 20) for column in range(10)]

        self.level = 1
        self.lines_on_level = 0
        self.score = 0
        self.tetris_streak = False
        self.to_set = False

        self.alive = True

        self.update_ghost()

    def move(self, direction):
        """
        Moves the piece
        :param direction: str => 'right' / 'left'
        """
        if direction == 'right':
            if self.active_piece.coords[0] + self.active_piece.rightmost_edge_relative_to_coords < 9:
                self.active_piece.coords += [1, 0]
                self.active_piece.update_location()
                if self.are_any_inside_list(arr1=self.active_piece.occupying_squares, arr2=self.occupied_squares):
                    self.active_piece.coords += [-1, 0]
        elif direction == 'left':
            if self.active_piece.coords[0] + self.active_piece.leftmost_edge_relative_to_coords > 0:
                self.active_piece.coords += [-1, 0]
                self.active_piece.update_location()
                if self.are_any_inside_list(arr1=self.active_piece.occupying_squares, arr2=self.occupied_squares):
                    self.active_piece.coords += [1, 0]

        self.active_piece.update_location()
        self.update_ghost()

    def set_tetromino(self):
        """
        Sets the active piece
        """
        self.active_piece.update_location()
        for coord in self.active_piece.occupying_squares:
            self.occupied_squares.append(coord)

        """checking for cleared lines, then clearing them if they exist"""
        cleared_lines = self.check_for_cleared_lines()
        if cleared_lines:
            self.clear_lines(lines=cleared_lines)

    def hard_drop(self):
        """
        Drops the active piece downwards and sets it instantly
        """
        add_score = -1
        while not self.are_any_inside_list(arr1=self.occupied_squares, arr2=self.active_piece.occupying_squares):
            add_score += 1
            self.active_piece.coords += [0, 1]
            self.active_piece.update_location()
        self.score += add_score
        self.active_piece.coords += [0, -1]
        self.set_tetromino()
        self.next_piece()

    def update_ghost(self):
        """
        Updates the location of the ghost of the given piece in the parameter
        """
        self.active_piece.ghost.reset_location_to_piece()
        while not self.are_any_inside_list(arr1=self.occupied_squares, arr2=self.active_piece.ghost.occupying_squares):
            self.active_piece.ghost.occupying_squares += [0, 1]
        self.active_piece.ghost.occupying_squares += [0, -1]

    def rotate_piece(self, direction: int):
        """
        Rotates the active piece according to the first test that succeeds, see the different tests at the top of the
        file, in the L_WALL_KICKS/JLSTZ_WALL_KICKS dictionaries. If none of the tests succeed, the piece wont be rotated
        :param direction: int => 1 for clockwise, 3 or -1 for counterclockwise
        """
        rotation_key = f"{self.active_piece.rot_number}-{(self.active_piece.rot_number + direction) % 4}"

        succeeded = False
        # get the wall kick tests according to which piece it is and how its being rotated
        wall_kick_tests: list[tuple]
        if self.active_piece.tetromino_code == 1:
            wall_kick_tests = L_WALL_KICKS.get(rotation_key)
        else:
            wall_kick_tests = JLSTZ_WALL_KICKS.get(rotation_key)

        # rotates the piece
        self.active_piece.rotation_grid = np.rot90(self.active_piece.rotation_grid, k=direction)
        for test in wall_kick_tests:
            # self.run_test moves and rotates the piece on its own, so no need to do that again
            if self.run_test(test=test):
                succeeded = True
                break

        # if the test succeeds:
        if succeeded:
            self.update_ghost()
            self.active_piece.rot_number = (self.active_piece.rot_number + direction) % 4
        else:
            self.active_piece.rotation_grid = np.rot90(self.active_piece.rotation_grid, k=-direction % 4)

    def run_test(self, test: tuple[int, int]):
        """
        attempts to rotate the piece according to the given test in the parameter.
        If the test fails, reverses the test and returns False
        """
        self.active_piece.coords += test
        self.active_piece.update_location()
        self.active_piece.update_edge()

        if self.active_piece.coords[0] + self.active_piece.rightmost_edge_relative_to_coords > 9 or\
                self.active_piece.coords[0] + self.active_piece.leftmost_edge_relative_to_coords < 0 or\
                self.are_any_inside_list(arr1=self.active_piece.occupying_squares, arr2=self.occupied_squares):
            self.active_piece.coords -= test
            self.active_piece.update_location()
            self.active_piece.update_edge()
            return False  # failed the test

        return True  # succeeded the test

    def next_piece(self):
        """
        Changes the active piece to the next piece \n
        If the the first one is done: moves the second bag to the first bags place in the main bag,
        and adds a new randomly permutated version of the 7 bag as the second bag
        """
        self.bag_index += 1

        self.active_piece: pieces.Tetromino = self.bag[self.bag_index]
        self.next: pieces.Tetromino = self.bag[self.bag_index + 1]

        if self.bag_index % 7 == 0:
            self.first_bag = self.next_bag
            self.bag_index -= 7
            self.next_bag = self.random_generator(np.array([pieces.Tetromino(tetromino_code=code) for code in range(1, 8)]))

            self.bag[:7] = self.first_bag
            self.bag[7:] = self.next_bag

        if self.are_any_inside_list(arr1=self.active_piece.occupying_squares, arr2=self.occupied_squares):
            self.active_piece.coords += [0, -2]
            self.active_piece.update_location()
            if self.are_any_inside_list(arr1=self.active_piece.occupying_squares, arr2=self.occupied_squares):
                self.alive = False

        self.all_pieces.append(self.active_piece)
        self.update_ghost()
        self.allowed_hold = True

    def hold_piece(self):
        """
        swaps the held piece and the active piece
        """
        if self.allowed_hold:
            if self.hold is None:
                self.all_pieces.remove(self.active_piece)
                self.hold = self.active_piece
                self.next_piece()

            else:
                self.all_pieces.remove(self.active_piece)
                self.hold, self.active_piece = self.active_piece, self.hold
                self.all_pieces.append(self.active_piece)

                self.active_piece.coords = np.array([3, 0])
                self.active_piece.rotation_grid = np.rot90(self.active_piece.rotation_grid, k=(4 - self.active_piece.rot_number) % 4)
                self.active_piece.rot_number = 0
                self.active_piece.update_location()
                self.active_piece.update_edge()
                self.update_ghost()
            self.allowed_hold = False

    def soft_drop(self):
        """
        Lowers the active piece until it touches a square, doesn't set instantly, unlike self.hard_drop
        """
        self.active_piece.coords += (0, 1)
        self.active_piece.update_location()

        if self.are_any_inside_list(arr1=self.occupied_squares, arr2=self.active_piece.occupying_squares):
            self.active_piece.coords += (0, -1)
            self.active_piece.update_location()

    def clear_lines(self, lines: list[int]):
        """
        removes the cleared lines from the board and the pieces and lowers the rest of the lines to the correct height
        """
        squares_for_removal = []

        # adding the squares in the cleared lines to squares_for_removal
        for index, square in enumerate(self.occupied_squares):
            if square[1] != 20:
                if square[1] in lines:
                    squares_for_removal.append(index)
        squares_for_removal = np.array(squares_for_removal)

        # removing said squares from the board
        for i_adjuster, index in enumerate(squares_for_removal):
            index -= i_adjuster
            self.occupied_squares.pop(index)

        # doing the same process for those same squares in the pieces, but slightly differently
        pieces_for_removal = []
        for piece in self.all_pieces:
            squares_for_removal = []

            for index in range(len(piece.occupying_squares)):
                if piece.occupying_squares[index][1] in lines:
                    squares_for_removal.append(index)

            if len(piece.occupying_squares) == 0:
               pieces_for_removal.append(piece)

            piece.occupying_squares = np.delete(piece.occupying_squares, squares_for_removal, axis=0)

        # deleting empty pieces
        for piece in pieces_for_removal:
            self.all_pieces.remove(piece)

        # setting how much each line has to be lowered by
        add_to_lines = np.array([0 for _ in range(20)])
        for line_num in lines:
            add_to_lines[:line_num] += 1

        # lowering the lines above the cleared lines on the board
        for square in self.occupied_squares:
            if square[1] != 20:
                square[1] += add_to_lines[square[1]]

        # same thing, but for the pieces
        for piece in self.all_pieces:
            for square in piece.occupying_squares:
                square[1] += add_to_lines[square[1]]

        lines_cleared = len(lines)
        self.lines_on_level += lines_cleared
        if self.lines_on_level > 10:
            self.level += 1
            self.lines_on_level %= 10

        points_earned = LINE_POINT_DICT.get(lines_cleared) * self.level
        if lines_cleared == 4:
            if self.tetris_streak:
                points_earned *= 1.5
            self.tetris_streak = True
        else:
            self.tetris_streak = False

        self.score += int(points_earned)

    def check_for_cleared_lines(self) -> list[int]:
        lines_to_check = {coords[1] for coords in self.active_piece.occupying_squares}
        cleared_lines = []
        for line in lines_to_check:
            if self.check_for_cleared_line(line):
                cleared_lines.append(line)
        return cleared_lines

    def check_for_cleared_line(self, line: int) -> bool:
        for x_coord in range(10):
            if not self.is_inside_list((x_coord, line), self.occupied_squares):
                return False
        return True

    def pass_time(self):
        self.active_piece.coords += [0, 1]
        self.active_piece.update_location()
        if self.are_any_inside_list(arr1=self.occupied_squares, arr2=self.active_piece.occupying_squares):
            self.active_piece.coords += [0, -1]
            self.active_piece.update_location()

            if self.to_set:
                self.set_tetromino()
                self.next_piece()
            else:
                self.to_set = True
        else:
            self.to_set = False

    @staticmethod
    def random_generator(bag: np.ndarray) -> np.ndarray:
        """
        Randomizes the bag of pieces out of the 7 tetrominos
        """
        bag = np.random.permutation(bag)
        while bag[0].tetromino_code not in [1, 2, 3, 6]:
            bag = np.random.permutation(bag)
        return bag

    @staticmethod
    def are_any_inside_list(arr1, arr2):
        for value in arr1:
            for value2 in arr2:
                if value[0] == value2[0] and value[1] == value2[1]:
                    return True
        return False

    @staticmethod
    def is_inside_list(value, arr2):
        for value2 in arr2:
            if value[0] == value2[0] and value[1] == value2[1]:
                return True
        return False

    @staticmethod
    def get_index_of_tuple_in_list(value: tuple[int, int], arr2: list[tuple[int, int]]) -> int:
        for index in range(len(arr2)):
            if value[0] == arr2[index][0] and value[1] == arr2[index][1]:
                return index
        return -1
