from typing import Optional
import pygame as pyg
import os


from Scenes.basescene import BaseScene

WIDTH = 900
HEIGHT = 600

WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Tetris")

icon = pyg.image.load(os.path.join('../assets', "Tetris_Logo.png"))
pyg.display.set_icon(icon)


class MainmenuScene():

    def __init__(self):
        self.next_scene: Optional[object] = None

    def blit_screen(self):
        pass

    def make_active_scene(self):
        pass


