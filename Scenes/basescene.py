import os
import pygame as pyg
import abc


class BaseScene:
    width: int
    height: int
    fps: int

    def __init__(self):
        self.WIN = pyg.display.set_mode(self.width, self.height)

        icon = pyg.image.load(os.path.join('../assets', "Tetris_Logo.png"))
        pyg.display.set_icon(icon)

    @abc.abstractmethod
    def draw_window(self):
        pass

    @abc.abstractmethod
    def make_active_scene(self):
        pass
