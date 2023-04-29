import pygame as pyg
import string


def activate_scene() -> str:
    pyg.font.init()

    FPS = 72

    VALID_LETTERS = string.ascii_letters + string.digits + " "

    WIDTH, HEIGHT = 600, 400

    FONT_SIZE = 50
    TEXT_FONT = pyg.font.SysFont("monospace", FONT_SIZE)

    WHITE_COLOUR = (255, 255, 255)

    NAME_INPUT_TEXT_IMAGE = TEXT_FONT.render("Input Name:", True, WHITE_COLOUR)

    INPUT_TEXT_HEIGHT = 0
    INPUT_TEXT_LOC = (
        (WIDTH - NAME_INPUT_TEXT_IMAGE.get_width()) / 2,
        INPUT_TEXT_HEIGHT,
    )

    # TB - text box
    TB_X, TB_Y = 50, INPUT_TEXT_HEIGHT + 100
    TB_WIDTH, TB_HEIGHT = 500, 50
    TB_BORDER_THICKNESS = 2

    TB_border_surf = pyg.Surface(
        (TB_WIDTH + 2 * TB_BORDER_THICKNESS, TB_HEIGHT + 2 * TB_BORDER_THICKNESS)
    )
    TB_border_surf.fill(WHITE_COLOUR)
    TB_surf = pyg.Surface((TB_WIDTH, TB_HEIGHT))
    TB_surf.fill((0, 0, 0))

    TB_BORDER_LOC = (
        (WIDTH - TB_border_surf.get_width()) / 2,
        TB_Y - TB_BORDER_THICKNESS,
    )

    MAX_USERNAME_LENGTH = 16

    WIN = pyg.display.set_mode((WIDTH, HEIGHT))
    pyg.display.set_caption("Tetris")

    username = ""

    def draw_window():
        WIN.fill((0, 0, 0))

        # Blitting the "input" text
        WIN.blit(NAME_INPUT_TEXT_IMAGE, INPUT_TEXT_LOC)

        # Blitting the textbox
        WIN.blit(TB_border_surf, TB_BORDER_LOC)
        WIN.blit(TB_surf, (TB_X, TB_Y))

        # Blitting the typed text inside the textbox
        TB_username_text_image = TEXT_FONT.render(username, True, (200, 200, 255))
        WIN.blit(
            TB_username_text_image,
            ((WIDTH - TB_username_text_image.get_width()) / 2, TB_Y),
        )

        pyg.display.update()

    clock = pyg.time.Clock()
    run = True

    user_typing = False

    while run:
        clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False

            if user_typing and event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKSPACE and username:
                    username = username[:-1]
                if (
                    event.unicode in VALID_LETTERS
                    and len(username) < MAX_USERNAME_LENGTH
                ):
                    username += event.unicode

        keys_pressed = pyg.key.get_pressed()

        if keys_pressed[pyg.K_RETURN] and username:
            run = False

        if keys_pressed[pyg.K_ESCAPE]:
            run = False

        if pyg.mouse.get_pressed(3)[0]:
            mouse_pos = pyg.mouse.get_pos()

            if (
                TB_X <= mouse_pos[0] <= TB_X + TB_WIDTH
                and TB_Y <= mouse_pos[1] <= TB_Y + TB_HEIGHT
            ):
                user_typing = True
                TB_border_surf.fill((100, 100, 255))
            else:
                user_typing = False
                TB_border_surf.fill(WHITE_COLOUR)

        draw_window()

    pyg.quit()
    return username


if __name__ == "__main__":
    name = activate_scene()
    print(name)
