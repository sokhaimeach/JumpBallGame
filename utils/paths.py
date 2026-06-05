import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def save_path(filename):
    folder = os.path.abspath("data")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)
