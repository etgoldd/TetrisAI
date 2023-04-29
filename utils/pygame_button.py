import pygame as pyg

pyg.font.init()

FONT_SIZE = 40
text_font = pyg.font.SysFont("monospace", FONT_SIZE)


class Button:
    """
    This class represents and implements a functional button for pygame,
    a button should be created once, in the beginning of the file.
    To use the button, simply blit the rect onto the screen using the blit_button method,
    and call the check_button method in the main event loop.
    """

    def __init__(
        self,
        coordinate: tuple[int, int],
        width: int,
        height: int,
        text: str,
        button_colour: tuple[int, int, int],
        text_colour: tuple[int, int, int],
    ) -> None:
        self.width = width
        self.height = height
        self.coordinate = coordinate
        self.text = text

        self.button_end = (
            self.coordinate[0] + self.width,
            self.coordinate[1] + self.height,
        )

        self.button_surf = pyg.Surface((self.width, self.height))
        self.button_surf.fill(button_colour)

        self.button_text_surface = text_font.render(self.text, True, text_colour)

        relative_loc = (
            (self.width - self.button_text_surface.get_width()) / 2,
            (self.height - self.button_text_surface.get_height()) / 2,
        )
        self.text_loc = (
            self.coordinate[0] + relative_loc[0],
            self.coordinate[1] + relative_loc[1],
        )

        self.pressed = False

    def blit_button(self, display: pyg.Surface):
        """
        This method blits the button onto the screen
        """
        display.blit(self.button_surf, self.coordinate)
        display.blit(self.button_text_surface, self.text_loc)

    def check_button(self):
        """
        This method is to be called inside the event loop.
        """
        mouse_pos = pyg.mouse.get_pos()
        is_pressed = pyg.mouse.get_pressed()[0]

        if (
            self.coordinate[0] < mouse_pos[0] < self.button_end[0]
            and self.coordinate[1] < mouse_pos[1] < self.button_end[1]
            and is_pressed
        ):
            self.pressed = True
        else:
            self.pressed = False
