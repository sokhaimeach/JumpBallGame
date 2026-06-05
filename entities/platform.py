import random

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving, platform_image):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (width, 15))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, scroll):
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
