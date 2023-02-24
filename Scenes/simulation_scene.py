import pygame as pyg
import numpy as np
import os

from AI import simulation
from Game import tetris as tet

pyg.font.init()

current_simulation = simulation.Simulation(gen_size=22,
                                                   n_allowed_to_reproduce=5,
                                                   single_reproductions=2,
                                                   max_mutation=1,
                                                   mutation_chance=20)

GRID_THICKNESS = 2
SQUARE_SIZE = 40

X_SQUARES = 10
Y_SQUARES = 20

NON_GRID_WIDTH_LEFT = 400
NON_GRID_WIDTH_RIGHT = 500

WIDTH, HEIGHT = X_SQUARES * SQUARE_SIZE + GRID_THICKNESS * (X_SQUARES - 1) + NON_GRID_WIDTH_LEFT + NON_GRID_WIDTH_RIGHT, \
                Y_SQUARES * SQUARE_SIZE + GRID_THICKNESS * (Y_SQUARES - 1)

RIGHT_AREA_OFFSET = WIDTH - NON_GRID_WIDTH_RIGHT

WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Tetrisonator-10000")

icon = pyg.image.load(os.path.join('../assets', "Tetris_Logo.png"))
pyg.display.set_icon(icon)

# neuron_image = pyg.image.load(os.path.join('assets', "neuron.png"))
# neuron_image = neuron_image

grid_surf_vert = pyg.Surface((GRID_THICKNESS, HEIGHT))
grid_surf_horiz = pyg.Surface((WIDTH - NON_GRID_WIDTH_LEFT - NON_GRID_WIDTH_RIGHT + 2, GRID_THICKNESS))

grid_surf_vert.fill((50, 50, 50))
grid_surf_horiz.fill((50, 50, 50))

tetromino_surf = pyg.Surface((SQUARE_SIZE, SQUARE_SIZE))
ghost_sprite = pyg.image.load(os.path.join('../assets', 'ghost_square.png'))

colour_by_tetromino_code = {1: (0, 255, 255),
                            2: (0, 25, 200),
                            3: (255, 170, 0),
                            4: (255, 255, 0),
                            5: (0, 255, 0),
                            6: (125, 0, 125),
                            7: (255, 0, 0)}

FONT_SIZE = 50
text_font = pyg.font.SysFont("monospace", FONT_SIZE)

HOLD_LOCATION = 80

NEXT_LOCATION = HOLD_LOCATION + 200
LEVEL_LOCATION = NEXT_LOCATION + 250
LINES_LOCATION = LEVEL_LOCATION + 150

GENERATION_LOCATION = 0
NETWORK_LOCATION = GENERATION_LOCATION + 275

FPS = 720

piece_distances = {1: (NON_GRID_WIDTH_LEFT - (4 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
                   2: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
                   3: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
                   4: (NON_GRID_WIDTH_LEFT - (2 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
                   5: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
                   6: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2,
                   7: (NON_GRID_WIDTH_LEFT - (3 * (SQUARE_SIZE + GRID_THICKNESS))) / 2}

RED_TUPLE = (255, 60, 60)


def draw_window(grid_lines_vert: list[pyg.Rect],
                grid_lines_horiz: list[pyg.Rect],
                board: tet.TetrisBoard,
                _simulation: simulation.Simulation):

    # Blitting the ghost
    WIN.fill((0, 0, 0))
    for coord in board.active_piece.ghost.occupying_squares:
        WIN.blit(ghost_sprite,
                 coord * SQUARE_SIZE + coord * GRID_THICKNESS + np.array([NON_GRID_WIDTH_LEFT + GRID_THICKNESS, 0]))

    pieces_to_blit = board.all_pieces
    # Blitting all pieces
    for piece in pieces_to_blit:
        for coord in piece.occupying_squares:
            tetromino_surf.fill(colour_by_tetromino_code.get(piece.tetromino_code))
            WIN.blit(tetromino_surf, coord * SQUARE_SIZE + coord * GRID_THICKNESS + np.array([NON_GRID_WIDTH_LEFT + GRID_THICKNESS, 0]))

    # Blitting the grid
    for grid_line in grid_lines_vert:
        WIN.blit(grid_surf_vert, (grid_line.x, grid_line.y))
    for grid_line in grid_lines_horiz:
        WIN.blit(grid_surf_horiz, (grid_line.x, grid_line.y))

    # BLitting the "hold" text
    hold_text_image = text_font.render("Hold", True, (255, 255, 255))
    WIN.blit(hold_text_image, ((NON_GRID_WIDTH_LEFT - hold_text_image.get_width()) / 2, HOLD_LOCATION))

    # Blitting the held piece
    hold_piece = board.hold
    if hold_piece is not None:
        relative_coords = np.array(np.nonzero(a=hold_piece.base_rotation_grid)).T

        hold_piece_min_distance_from_left = piece_distances.get(hold_piece.tetromino_code)

        tetromino_surf.fill(colour_by_tetromino_code.get(hold_piece.tetromino_code))
        for coord in relative_coords:
            WIN.blit(tetromino_surf, coord * (SQUARE_SIZE + GRID_THICKNESS) + np.array([hold_piece_min_distance_from_left, HOLD_LOCATION + 80]))

    # Blitting the "Next" text
    hold_text_image = text_font.render("Next", True, (255, 255, 255))
    WIN.blit(hold_text_image, ((NON_GRID_WIDTH_LEFT - hold_text_image.get_width()) / 2, NEXT_LOCATION))

    # Blitting the next piece
    next_piece = board.next
    relative_coords = np.array(np.nonzero(a=next_piece.base_rotation_grid)).T

    next_piece_min_distance_from_left = piece_distances.get(next_piece.tetromino_code)

    tetromino_surf.fill(colour_by_tetromino_code.get(next_piece.tetromino_code))
    for coord in relative_coords:
        WIN.blit(tetromino_surf, coord * (SQUARE_SIZE + GRID_THICKNESS) + np.array(
            [next_piece_min_distance_from_left, NEXT_LOCATION + 80]))

    # Blitting the score
    score_image = text_font.render(f"{board.score}", True, (255, 255, 255))
    WIN.blit(score_image, ((NON_GRID_WIDTH_LEFT - score_image.get_width()) / 2, 0))

    # BLitting the level
    level_text_image = text_font.render("level", True, (255, 255, 255))
    WIN.blit(level_text_image, ((NON_GRID_WIDTH_LEFT - level_text_image.get_width()) / 2, LEVEL_LOCATION))

    level_image = text_font.render(f"{board.level}", True, (255, 255, 255))
    WIN.blit(level_image, ((NON_GRID_WIDTH_LEFT - level_image.get_width()) / 2, LEVEL_LOCATION + 50))

    # Blitting the line count
    lines_text_image = text_font.render("lines", True, (255, 255, 255))
    WIN.blit(lines_text_image, ((NON_GRID_WIDTH_LEFT - lines_text_image.get_width()) / 2, LINES_LOCATION))

    lines_count_image = text_font.render(f"{board.lines_on_level + (board.level - 1) * 10}", True, (255, 255, 255))
    WIN.blit(lines_count_image, ((NON_GRID_WIDTH_LEFT - lines_count_image.get_width()) / 2, LINES_LOCATION + 50))

    # Blitting the generation and unit
    generation_text_image = text_font.render("generation", True, (255, 255, 255))
    WIN.blit(generation_text_image, (RIGHT_AREA_OFFSET + (NON_GRID_WIDTH_RIGHT - generation_text_image.get_width()) / 2, GENERATION_LOCATION))

    generation_image = text_font.render(f"{_simulation.generation + 1}", True, (255, 255, 255))
    WIN.blit(generation_image, (RIGHT_AREA_OFFSET + (NON_GRID_WIDTH_RIGHT - generation_image.get_width()) / 2, GENERATION_LOCATION + 50))

    unit_text_image = text_font.render("Player", True, (255, 255, 255))
    WIN.blit(unit_text_image, (RIGHT_AREA_OFFSET + (NON_GRID_WIDTH_RIGHT - unit_text_image.get_width()) / 2, GENERATION_LOCATION + 100))

    unit_image = text_font.render(f"{_simulation.tetting_index + 1}", True, (255, 255, 255))
    WIN.blit(unit_image, (RIGHT_AREA_OFFSET + (NON_GRID_WIDTH_RIGHT - unit_image.get_width()) / 2, GENERATION_LOCATION + 150))

    # Blitting the neural network
    # blit_network(brain=simulation.active_tetting.brain)

    pyg.display.update()


def main():
    clock = pyg.time.Clock()
    run = True

    grid_rects_vert = [pyg.Rect(x, 0, GRID_THICKNESS, HEIGHT) for x in range(NON_GRID_WIDTH_LEFT, WIDTH - NON_GRID_WIDTH_RIGHT + 3, SQUARE_SIZE + GRID_THICKNESS)]
    grid_rects_horiz = [pyg.Rect(NON_GRID_WIDTH_LEFT, y, WIDTH, GRID_THICKNESS) for y in range(SQUARE_SIZE, HEIGHT, SQUARE_SIZE + GRID_THICKNESS)]

    tetris_board = current_simulation.active_tetting.board
    current_simulation.next_piece()
    t = 1

    while run:
        clock.tick(FPS)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False

        current_simulation.update()

        if current_simulation.dead_tetting_flag:
            tetris_board = current_simulation.active_tetting.board

        draw_window(grid_lines_vert=grid_rects_vert,
                    grid_lines_horiz=grid_rects_horiz,
                    board=tetris_board,
                    _simulation=current_simulation)

        t += 1


if __name__ == "__main__":
    main()
