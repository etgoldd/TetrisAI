import pygame as pyg
import os

from utils.pygame_button import Button


def activate_scene():
    pyg.font.init()

    WIDTH, HEIGHT = 600, 900

    WIN = pyg.display.set_mode((WIDTH, HEIGHT))
    pyg.display.set_caption("Tetris - Main menu")

    icon = pyg.image.load(os.path.join("./assets", "Tetris_Logo.png"))
    pyg.display.set_icon(icon)

    FONT_SIZE = 50
    text_font = pyg.font.SysFont("monospace", FONT_SIZE)

    FPS = 72
    WHITE_COLOUR = (255, 255, 255)
    DARK_BLUE_COLOUR = (30, 30, 130)

    TITLE_HEIGHT = 100
    SELECT_HEIGHT = TITLE_HEIGHT + 80
    PLAY_GAME_HEIGHT = SELECT_HEIGHT + 100
    PLAY_GAME_BUTTON_WIDTH_HEGIHT = [300, 90]
    AI_MODE_HEIGHT = PLAY_GAME_HEIGHT + PLAY_GAME_BUTTON_WIDTH_HEGIHT[1] + 80
    AI_MODE_BUTTON_WIDTH_HEIGHT = [300, 90]
    SCOREBOARD_HEIGHT = AI_MODE_HEIGHT + AI_MODE_BUTTON_WIDTH_HEIGHT[1] + 80
    SCOREBOARD_BUTTON_WIDTH_HEIGHT = [300, 90]

    PLAY_GAME_BUTTON = Button(
        ((WIDTH - PLAY_GAME_BUTTON_WIDTH_HEGIHT[0]) / 2, PLAY_GAME_HEIGHT),
        PLAY_GAME_BUTTON_WIDTH_HEGIHT[0],
        PLAY_GAME_BUTTON_WIDTH_HEGIHT[1],
        "PLAY GAME",
        DARK_BLUE_COLOUR,
        WHITE_COLOUR,
    )

    AI_MODE_BUTTON = Button(
        ((WIDTH - AI_MODE_BUTTON_WIDTH_HEIGHT[0]) / 2, AI_MODE_HEIGHT),
        AI_MODE_BUTTON_WIDTH_HEIGHT[0],
        AI_MODE_BUTTON_WIDTH_HEIGHT[1],
        "AI MODE",
        DARK_BLUE_COLOUR,
        WHITE_COLOUR,
    )

    SCOREBOARD_BUTTON = Button(
        ((WIDTH - SCOREBOARD_BUTTON_WIDTH_HEIGHT[0]) / 2, SCOREBOARD_HEIGHT),
        SCOREBOARD_BUTTON_WIDTH_HEIGHT[0],
        SCOREBOARD_BUTTON_WIDTH_HEIGHT[1],
        "SCOREBOARD",
        DARK_BLUE_COLOUR,
        WHITE_COLOUR,
    )

    def draw_window():
        # Wiping the screen
        WIN.fill((0, 0, 0))

        # BLitting the "Tetris" text
        title_text_image = text_font.render("Tetris", True, WHITE_COLOUR)
        WIN.blit(
            title_text_image, ((WIDTH - title_text_image.get_width()) / 2, TITLE_HEIGHT)
        )

        # Blitting the "Select an option" text
        select_text_image = text_font.render("Select an option", True, WHITE_COLOUR)
        WIN.blit(
            select_text_image,
            ((WIDTH - select_text_image.get_width()) / 2, SELECT_HEIGHT),
        )

        # Blitting the play game button
        PLAY_GAME_BUTTON.blit_button(WIN)

        # Blitting the AI mode button
        AI_MODE_BUTTON.blit_button(WIN)

        # blitting the scoreboard button
        SCOREBOARD_BUTTON.blit_button(WIN)

        # Updating the screen
        pyg.display.update()

    clock = pyg.time.Clock()
    return_value = ""
    run = True

    while run:
        clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False

        PLAY_GAME_BUTTON.check_button()

        if PLAY_GAME_BUTTON.pressed:
            return_value = "PLAY_GAME"
            run = False

        AI_MODE_BUTTON.check_button()

        if AI_MODE_BUTTON.pressed:
            return_value = "AI_MODE"
            run = False

        SCOREBOARD_BUTTON.check_button()

        if SCOREBOARD_BUTTON.pressed:
            return_value = "SCOREBOARD"
            run = False

        draw_window()

    pyg.quit()
    return return_value


if __name__ == "__main__":
    activate_scene()
