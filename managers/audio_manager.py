import pygame

from utils.paths import resource_path


class SilentSound:
    def play(self):
        return None

    def stop(self):
        return None

    def set_volume(self, volume):
        return None


class AudioManager:
    def load_sound(self, path):
        if not pygame.mixer.get_init():
            return SilentSound()

        try:
            return pygame.mixer.Sound(resource_path(path))
        except (FileNotFoundError, pygame.error) as error:
            print(f"Could not load sound {path}: {error}")
            return SilentSound()
