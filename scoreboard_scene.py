import pygame as pyg
import numpy as np
import csv

from utils import open_file as fileOpen


def write_data(player_data: dict):
    # Initiating variable at function-wide scope
    index = -1
    # Attempt to get last index, if there is no last index, then the index is set to 1
    with open(fileOpen.TABLE_NAME, mode="r") as csvfile:
        try:
            index = ""
            for character in csvfile.readlines()[-1]:
                if character == ",":
                    break
                index += character
            index = int(index) + 1
        except:
            index = 1

    # Formatting the player data to an list
    player_data_row = [index, player_data["name"], player_data["score"]]

    # Writing player data to the scoreboard
    with open(fileOpen.TABLE_NAME, mode="a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, dialect="excel")
        csvwriter.writerow(player_data_row)


def activate_scene(player_data: dict):
    # Check if player data was given
    if player_data:
        write_data(player_data)

    pyg.font.init()

    SCORE_WIDTH, SCORE_HEIGHT = 954, 736
    SCORE_FPS = 60

    SCORE_WIN = pyg.display.set_mode((SCORE_WIDTH, SCORE_HEIGHT))
    pyg.display.set_caption("Tetris - Player Scoreboard")

    text_font = pyg.font.SysFont("monospace", 30)
    WHITE_COLOUR = (255, 255, 255)

    index_column_width = 150
    name_column_width = 400
    row_height = 30

    score_grid_thickness = 2
    score_grid_surf_vert = pyg.Surface((score_grid_thickness, SCORE_HEIGHT))
    score_grid_surf_horiz = pyg.Surface((SCORE_WIDTH, score_grid_thickness))
    score_grid_surf_vert.fill((50, 50, 50))
    score_grid_surf_horiz.fill((50, 50, 50))

    score_grid_lines_vert = [
        pyg.Rect(index_column_width, 0, score_grid_thickness, SCORE_HEIGHT),
        pyg.Rect(
            index_column_width + score_grid_thickness + name_column_width,
            0,
            score_grid_thickness,
            SCORE_HEIGHT,
        ),
    ]
    score_grid_lines_horiz = [
        pyg.Rect(
            0,
            (y + 1) * row_height + y * score_grid_thickness,
            SCORE_WIDTH,
            score_grid_thickness,
        )
        for y in range(SCORE_HEIGHT // (score_grid_thickness + row_height))
    ]

    def draw_scoreboard(
        rows_scrolled: int,
        score_grid_lines_vert: list,
        score_grid_lines_horiz: list,
        sort_type: int,
        scores: list,
    ):
        SCORE_WIN.fill((0, 0, 0))

        for grid_line in score_grid_lines_vert:
            SCORE_WIN.blit(score_grid_surf_vert, (grid_line.x, grid_line.y))
        for grid_line in score_grid_lines_horiz:
            SCORE_WIN.blit(score_grid_surf_horiz, (grid_line.x, grid_line.y))

        reset_index = False

        with open(fileOpen.TABLE_NAME, mode="r") as csvfile:
            csvreader = csv.reader(csvfile, dialect="excel")

            # Blitting the headers
            for headers in csvreader:
                index_text_image = text_font.render(headers[0], True, WHITE_COLOUR)
                SCORE_WIN.blit(index_text_image, (0, 0))

                name_text_image = text_font.render(headers[1], True, WHITE_COLOUR)
                SCORE_WIN.blit(
                    name_text_image, (index_column_width + score_grid_thickness, 0)
                )

                score_text_image = text_font.render(headers[2], True, WHITE_COLOUR)
                SCORE_WIN.blit(
                    score_text_image,
                    (
                        index_column_width
                        + name_column_width
                        + score_grid_thickness * 2,
                        0,
                    ),
                )
                # Breaking because only the first row contains the headers
                break

            # Iterating through each score
            i = 0
            for score_data in scores:
                i += 1
                if not reset_index and i <= rows_scrolled:
                    if i == rows_scrolled:
                        reset_index = True
                        i = 1
                    else:
                        continue

                # Blitting the index number
                index_text_image = text_font.render(
                    f"{score_data[0]}", True, WHITE_COLOUR
                )
                SCORE_WIN.blit(
                    index_text_image, (0, i * (row_height + score_grid_thickness))
                )

                # Blitting the name
                name_text_image = text_font.render(
                    f"{score_data[1]}", True, WHITE_COLOUR
                )
                SCORE_WIN.blit(
                    name_text_image,
                    (
                        index_column_width + score_grid_thickness,
                        i * (row_height + score_grid_thickness),
                    ),
                )

                # Blitting the score
                score_text_image = text_font.render(
                    f"{score_data[2]}", True, WHITE_COLOUR
                )
                SCORE_WIN.blit(
                    score_text_image,
                    (
                        index_column_width
                        + name_column_width
                        + score_grid_thickness * 2,
                        i * (row_height + score_grid_thickness),
                    ),
                )

        pyg.display.update()

    clock = pyg.time.Clock()
    run = True
    scrolled = 0

    with open(fileOpen.TABLE_NAME, mode="r") as csvfile:
        try:
            max_index = ""
            for character in csvfile.readlines()[-1]:
                if character == ",":
                    break
                max_index += character
            max_index = int(max_index) + 1
        except:
            max_index = 1

    sort_type = 0

    # Loading all the scores into a sorted_scores
    with open(fileOpen.TABLE_NAME, mode="r") as csvfile:
        csvreader = csv.reader(csvfile, dialect="excel")

        for sim in csvreader:
            break

        scores = []
        for sim in csvreader:
            scores.append((sim[0], sim[1], sim[2]))

    while run:
        clock.tick(SCORE_FPS)
        mouse_coords = pyg.mouse.get_pos()

        # Event Handler
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 5 and scrolled < max_index - 22:
                    scrolled += 1
                if event.button == 4 and scrolled > 0:
                    scrolled -= 1
                if event.button == 1 and scrolled == 0:
                    if 0 < mouse_coords[1] < 30:
                        if 0 < mouse_coords[0] < index_column_width:
                            sort_type = 0
                        elif mouse_coords[0] < name_column_width:
                            sort_type = 1

                        else:
                            sort_type = 2

        draw_scoreboard(
            rows_scrolled=scrolled,
            score_grid_lines_vert=score_grid_lines_vert,
            score_grid_lines_horiz=score_grid_lines_horiz,
            sort_type=sort_type,
            scores=scores,
        )

    pyg.quit()


if __name__ == "__main__":
    activate_scene({"score": -1, "name": "debug"})
