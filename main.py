import mainmenu_scene
import manual_game_scene
import simulation_scene
import name_scene
import scoreboard_scene


def main():
    selected_mode = mainmenu_scene.activate_scene()

    if selected_mode == "":
        return
    elif selected_mode == "PLAY_GAME":
        player_data = {}
        score = manual_game_scene.activate_scene()
        player_data["score"] = score

        name = name_scene.activate_scene()
        player_data["name"] = name

        scoreboard_scene.activate_scene(player_data=player_data)
    elif selected_mode == "AI_MODE":
        simulation_scene.activate_scene()
    elif selected_mode == "SCOREBOARD":
        scoreboard_scene.activate_scene(player_data={})


if __name__ == "__main__":
    main()

# main screen to choose between simulmain and main
# add csv to track main high scores from the manual game
# present the high score to the user
