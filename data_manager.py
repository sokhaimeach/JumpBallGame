import json
import os
from game_functions import resource_path, save_path

SAVE_FILE = save_path("save_data.json")
SEASON_FILE = resource_path("data/seasons.json")
BALLS_FILE = resource_path("data/balls.json")

# function for read json file and return as data
def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)
    
# function for write json file
def write_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    
# function for load save data
def load_save_data():
    if not os.path.exists(SAVE_FILE):
        data = {
            "high_score": 0,
            "coins": 0,
            "selected_season": "sky",
            "unlocked_seasons": ["sky"],
            "selected_ball": "red",
            "unlocked_balls": ["red"]
        }
        write_json(SAVE_FILE, data)
        return data
    
    return load_json(SAVE_FILE)

# function for save game data
def save_game_data(data):
    write_json(SAVE_FILE, data)

# function for load seasons data
def load_seasons():
    return load_json(SEASON_FILE)

# function for load balls data
def load_balls():
    return load_json(BALLS_FILE)

    
def unlock_season(save_data, key, seasons, sound):
    cost = seasons[key]["unlock_cost"]

    if key in save_data["unlocked_seasons"]:
        save_data["selected_season"] = key
        save_game_data(save_data)
        return True

    if save_data["coins"] >= cost:
        save_data["coins"] -= cost
        save_data["unlocked_seasons"].append(key)
        save_data["selected_season"] = key
        save_game_data(save_data)
        sound.play()
        return True

    return False


def unlock_ball(save_data, key, balls, sound):
    cost = balls[key]["unlock_cost"]

    if key in save_data["unlocked_balls"]:
        save_data["selected_ball"] = key
        save_game_data(save_data)
        return True

    if save_data["coins"] >= cost:
        save_data["coins"] -= cost
        save_data["unlocked_balls"].append(key)
        save_data["selected_ball"] = key
        save_game_data(save_data)
        sound.play()
        return True

    return False
