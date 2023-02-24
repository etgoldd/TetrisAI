import pygame as pyg
import os

from Scenes.basescene import BaseScene


class EndGameBaseScene(BaseScene):

    def __init__(self):
        self.width = 900
        self.height = 600

        super().__init__()

