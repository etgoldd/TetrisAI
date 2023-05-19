from __future__ import annotations
from typing import Union

from Game import tetris
from AI import tet_ai


class Tetting:
    def __init__(
        self,
        parents: Union[None, list[tet_ai.TetAI]],
        max_mutation: float,
        mutation_chance: int,
    ):
        self.board: tetris.TetrisBoard = tetris.TetrisBoard()

        self.brain = tet_ai.TetAI(
            board=self.board,
            parents=parents,
            max_mutation=max_mutation,
            mutation_chance=mutation_chance,
        )
        self.decision = []
        self.next_piece_flag = False

    def act(self, action: int):
        """
        Does a single action
        """
        if 4 > action > 0:
            self.board.rotate_piece(action)
        elif action == 4:
            self.board.hard_drop()
            self.next_piece_flag = True
        elif action == 5:
            self.board.move("left")
        elif action == 6:
            self.board.move("right")
        elif action == 7:
            self.board.hold_piece()

    def decide(self):
        self.brain.fire_up()
        self.decision = self.brain.decision[2]
