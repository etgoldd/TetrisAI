import pygame as pyg
import numpy as np
import os

from Game import tetris as tet


def activate_scene():
    level_difficulty_mapping = {
        1: 72,
        2: 64,
        3: 58,
        4: 50,
        5: 44,
        6: 36,
        7: 30,
        8: 26,
        9: 16,
        10: 12,
        11: 10,
        12: 10,
        13: 8,
        14: 8,
        15: 8,
    }

    pyg.font.init()

    GRID_THICKNESS = 2
    SQUARE_SIZE = 40

    X_SQUARES = 10
    Y_SQUARES = 20

    NON_GRID_WIDTH_LEFT = 400
    NON_GRID_WIDTH_RIGHT = 300

    WIDTH, HEIGHT = X_SQUARES * SQUARE_SIZE + GRID_THICKNESS * (
        X_SQUARES - 1
    ) + NON_GRID_WIDTH_LEFT + NON_GRID_WIDTH_RIGHT, Y_SQUARES * SQUARE_SIZE + GRID_THICKNESS * (
        Y_SQUARES - 1
    )

    WIN = pyg.display.set_mode((WIDTH, HEIGHT))
    pyg.display.set_caption("Tetris")

    grid_surf_vert = pyg.Surface((GRID_THICKNESS, HEIGHT))
    grid_surf_horiz = pyg.Surface(
        (WIDTH - NON_GRID_WIDTH_LEFT - NON_GRID_WIDTH_RIGHT + 2, GRID_THICKNESS)
    )

    grid_surf_vert.fill((50, 50, 50))
    grid_surf_horiz.fill((50, 50, 50))

    icon = pyg.image.load(os.path.join("./assets", "Tetris_Logo.png"))
    pyg.display.set_icon(icon)

    tetromino_surf = pyg.Surface((SQUARE_SIZE, SQUARE_SIZE))
    ghost_sprite = pyg.image.load(os.path.join("./assets", "ghost_square.png"))

    colour_by_tetromino_code = {
        1: (0, 255, 255),
        2: (0, 25, 200),
        3: (255, 170, 0),
        4: (255, 255, 0),
        5: (0, 255, 0),
        6: (125, 0, 125),
        7: (255, 0, 0),
    }

    FONT_SIZE = 50
    text_font = pyg.font.SysFont("monospace", FONT_SIZE)

    HOLD_LOCATION = 80

    NEXT_LOCATION = HOLD_LOCATION + 250
    LEVEL_LOCATION = NEXT_LOCATION + 200
    LINES_LOCATION = LEVEL_LOCATION + 150

    FPS = 72

    tetris_board = tet.TetrisBoard()

    piece_distances = {
        1: (NON_GRID_WIDTH_LEFT - (4 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
        2: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
        3: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
        4: (NON_GRID_WIDTH_LEFT - (2 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
        5: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
        6: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
        7: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
    }

    def draw_window(
        grid_lines_vert: list[pyg.Rect],
        grid_lines_horiz: list[pyg.Rect],
        board: tet.TetrisBoard,
        score: int,
        level: int,
        lines: int,
    ):
        # Blitting the ghost
        WIN.fill((0, 0, 0))
        for coord in board.active_piece.ghost.occupying_squares:
            WIN.blit(
                ghost_sprite,
                coord * SQUARE_SIZE
                + coord * GRID_THICKNESS
                + np.array([NON_GRID_WIDTH_LEFT + GRID_THICKNESS, 0]),
            )

        pieces_to_blit = board.all_pieces
        # Blitting all pieces
        for piece in pieces_to_blit:
            for coord in piece.occupying_squares:
                tetromino_surf.fill(colour_by_tetromino_code.get(piece.tetromino_code))
                WIN.blit(
                    tetromino_surf,
                    coord * SQUARE_SIZE
                    + coord * GRID_THICKNESS
                    + np.array([NON_GRID_WIDTH_LEFT + GRID_THICKNESS, 0]),
                )

        # Blitting the grid
        for grid_line in grid_lines_vert:
            WIN.blit(grid_surf_vert, (grid_line.x, grid_line.y))
        for grid_line in grid_lines_horiz:
            WIN.blit(grid_surf_horiz, (grid_line.x, grid_line.y))

        # BLitting the "hold" text
        hold_text_image = text_font.render("Hold", True, (255, 255, 255))
        WIN.blit(
            hold_text_image,
            ((NON_GRID_WIDTH_LEFT - hold_text_image.get_width()) / 2, HOLD_LOCATION),
        )

        # Blitting the held piece
        hold_piece = tetris_board.hold
        if hold_piece is not None:
            relative_coords = np.array(np.nonzero(a=hold_piece.base_rotation_grid)).T

            hold_piece_min_distance_from_left = piece_distances.get(
                hold_piece.tetromino_code
            )

            tetromino_surf.fill(colour_by_tetromino_code.get(hold_piece.tetromino_code))
            for coord in relative_coords:
                WIN.blit(
                    tetromino_surf,
                    coord * (SQUARE_SIZE + GRID_THICKNESS)
                    + np.array([hold_piece_min_distance_from_left, HOLD_LOCATION + 80]),
                )

        # Blitting the "Next" text
        hold_text_image = text_font.render("Next", True, (255, 255, 255))
        WIN.blit(
            hold_text_image,
            ((NON_GRID_WIDTH_LEFT - hold_text_image.get_width()) / 2, NEXT_LOCATION),
        )

        # Blitting the next piece
        next_piece = tetris_board.next
        relative_coords = np.array(np.nonzero(a=next_piece.base_rotation_grid)).T

        next_piece_min_distance_from_left = piece_distances.get(
            next_piece.tetromino_code
        )

        tetromino_surf.fill(colour_by_tetromino_code.get(next_piece.tetromino_code))
        for coord in relative_coords:
            WIN.blit(
                tetromino_surf,
                coord * (SQUARE_SIZE + GRID_THICKNESS)
                + np.array([next_piece_min_distance_from_left, NEXT_LOCATION + 80]),
            )

        # Blitting the score
        score_image = text_font.render(f"{score}", True, (255, 255, 255))
        WIN.blit(score_image, ((NON_GRID_WIDTH_LEFT - score_image.get_width()) / 2, 0))

        # BLitting the level
        level_text_image = text_font.render("level", True, (255, 255, 255))
        WIN.blit(
            level_text_image,
            ((NON_GRID_WIDTH_LEFT - level_text_image.get_width()) / 2, LEVEL_LOCATION),
        )

        level_image = text_font.render(f"{level}", True, (255, 255, 255))
        WIN.blit(
            level_image,
            ((NON_GRID_WIDTH_LEFT - level_image.get_width()) / 2, LEVEL_LOCATION + 50),
        )

        # Blitting the line count
        lines_text_image = text_font.render("lines", True, (255, 255, 255))
        WIN.blit(
            lines_text_image,
            ((NON_GRID_WIDTH_LEFT - lines_text_image.get_width()) / 2, LINES_LOCATION),
        )

        lines_count_image = text_font.render(f"{lines}", True, (255, 255, 255))
        WIN.blit(
            lines_count_image,
            (
                (NON_GRID_WIDTH_LEFT - lines_count_image.get_width()) / 2,
                LINES_LOCATION + 50,
            ),
        )

        pyg.display.update()

    clock = pyg.time.Clock()

    grid_rects_vert = [
        pyg.Rect(x, 0, GRID_THICKNESS, HEIGHT)
        for x in range(
            NON_GRID_WIDTH_LEFT,
            WIDTH - NON_GRID_WIDTH_RIGHT + 3,
            SQUARE_SIZE + GRID_THICKNESS,
        )
    ]
    grid_rects_horiz = [
        pyg.Rect(NON_GRID_WIDTH_LEFT, y, WIDTH, GRID_THICKNESS)
        for y in range(SQUARE_SIZE, HEIGHT, SQUARE_SIZE + GRID_THICKNESS)
    ]

    t = 1
    t_hard_drop_cooldown = 0
    t_held_right = 0
    t_held_left = 0

    held_rotate_clockwise = 0
    held_rotate_counterclockwise = 0

    run = True
    while run:
        clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False

        keys_pressed = pyg.key.get_pressed()

        if keys_pressed[pyg.K_LEFT]:
            if t_held_left == 0 or t_held_left > FPS / 8 and t_held_left % 2 == 0:
                tetris_board.move(direction="left")
            t_held_left += 1
        elif t_held_left > 0:
            t_held_left = 0

        if keys_pressed[pyg.K_RIGHT]:
            if t_held_right == 0 or t_held_right > FPS / 8 and t_held_right % 2 == 0:
                tetris_board.move(direction="right")
            t_held_right += 1
        elif t_held_right > 0:
            t_held_right = 0

        if keys_pressed[pyg.K_DOWN]:
            tetris_board.soft_drop()

        if keys_pressed[pyg.K_UP]:
            if held_rotate_clockwise == 0:
                tetris_board.rotate_piece(direction=1)
            held_rotate_clockwise = 1
        elif held_rotate_clockwise == 1:
            held_rotate_clockwise = 0

        if keys_pressed[pyg.K_z]:
            if held_rotate_counterclockwise == 0:
                tetris_board.rotate_piece(direction=3)
            held_rotate_counterclockwise = 1
        elif held_rotate_counterclockwise == 1:
            held_rotate_counterclockwise = 0

        if keys_pressed[pyg.K_SPACE]:
            if t_hard_drop_cooldown == 0:
                tetris_board.hard_drop()
            t_hard_drop_cooldown = 1
        elif t_hard_drop_cooldown == 1:
            t_hard_drop_cooldown = 0

        if keys_pressed[pyg.K_c]:
            tetris_board.hold_piece()

        draw_window(
            grid_lines_vert=grid_rects_vert,
            grid_lines_horiz=grid_rects_horiz,
            board=tetris_board,
            score=tetris_board.score,
            level=tetris_board.level,
            lines=tetris_board.lines_on_level + (tetris_board.level - 1) * 10,
        )
        if tetris_board.level < 15:
            if t % level_difficulty_mapping.get(tetris_board.level) == 0:
                tetris_board.pass_time()
                t = 0
        else:
            if t % 6 == 0:
                tetris_board.pass_time()
                t = 0
        if not tetris_board.alive:
            run = False

        t += 1

    pyg.quit()
    return tetris_board.score


if __name__ == "__main__":
    activate_scene()
