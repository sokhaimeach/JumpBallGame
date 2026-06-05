from copy import deepcopy
import json
import os

from utils.paths import resource_path, save_path


DEFAULT_SAVE_DATA = {
    "high_score": 0,
    "coins": 0,
    "selected_season": "sky",
    "unlocked_seasons": ["sky"],
    "selected_ball": "red",
    "unlocked_balls": ["red"],
}

SAVE_FILE = save_path("save_data.json")
SEASON_FILE = resource_path("data/seasons.json")
BALLS_FILE = resource_path("data/balls.json")


class JsonDataStore:
    def __init__(self, save_file=SAVE_FILE, season_file=SEASON_FILE, balls_file=BALLS_FILE):
        self._save_file = save_file
        self._season_file = season_file
        self._balls_file = balls_file

    def load_json(self, filename, default=None):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, OSError) as error:
            print(f"Could not load {filename}: {error}")
            return deepcopy(default) if isinstance(default, dict) else default

    def write_json(self, filename, data):
        try:
            folder = os.path.dirname(filename)
            if folder:
                os.makedirs(folder, exist_ok=True)

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            print(f"Could not save {filename}: {error}")

    def load_save_data(self):
        data = self.load_json(self._save_file, DEFAULT_SAVE_DATA)
        if data is None:
            data = deepcopy(DEFAULT_SAVE_DATA)

        data = self._merge_save_defaults(data)
        self.write_json(self._save_file, data)
        return data

    def save_game_data(self, data):
        self.write_json(self._save_file, data)

    def load_seasons(self):
        return self.load_json(self._season_file, {})

    def load_balls(self):
        return self.load_json(self._balls_file, {})

    def _merge_save_defaults(self, data):
        merged = deepcopy(DEFAULT_SAVE_DATA)
        merged.update(data)

        for key in ("unlocked_seasons", "unlocked_balls"):
            value = merged.get(key)
            if not isinstance(value, list):
                merged[key] = DEFAULT_SAVE_DATA[key].copy()

        return merged


data_store = JsonDataStore()


def load_json(filename, default=None):
    return data_store.load_json(filename, default)


def write_json(filename, data):
    data_store.write_json(filename, data)


def load_save_data():
    return data_store.load_save_data()


def save_game_data(data):
    data_store.save_game_data(data)


def load_seasons():
    return data_store.load_seasons()


def load_balls():
    return data_store.load_balls()


def unlock_item(save_data, key, items, unlock_key, selected_key, sound):
    try:
        item = items[key]
        cost = item["unlock_cost"]
    except KeyError as error:
        print(f"Could not unlock item {key}: missing {error}")
        return False

    unlocked_items = save_data.setdefault(unlock_key, [])

    if key in unlocked_items:
        save_data[selected_key] = key
        save_game_data(save_data)
        return True

    if save_data.get("coins", 0) >= cost:
        save_data["coins"] -= cost
        unlocked_items.append(key)
        save_data[selected_key] = key
        save_game_data(save_data)
        sound.play()
        return True

    return False


def unlock_season(save_data, key, seasons, sound):
    return unlock_item(save_data, key, seasons, "unlocked_seasons", "selected_season", sound)


def unlock_ball(save_data, key, balls, sound):
    return unlock_item(save_data, key, balls, "unlocked_balls", "selected_ball", sound)
