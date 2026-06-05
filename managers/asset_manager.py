import pygame

from utils.paths import resource_path


class AssetManager:
    def load_image(self, path, fallback_size):
        try:
            return pygame.image.load(resource_path(path)).convert_alpha()
        except (FileNotFoundError, pygame.error) as error:
            print(f"Could not load image {path}: {error}")
            fallback = pygame.Surface(fallback_size, pygame.SRCALPHA)
            fallback.fill((80, 80, 95))
            return fallback
