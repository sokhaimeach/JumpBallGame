import pygame

from settings import SCREEN_HEIGHT


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, moving, direction, speed, move_counter, sprite_sheet, scale):
        super().__init__()
        self.animation_list = self._load_frames(sprite_sheet, scale)
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.moving = moving
        self.direction = direction
        self.speed = speed
        self.move_counter = move_counter

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self, scroll):
        self._animate()
        self._move_with_platform()
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def _load_frames(self, sprite_sheet, scale):
        frames = []
        for frame in range(9):
            image = sprite_sheet.get_image(frame, 50, 50, scale, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            frames.append(image)
        return frames

    def _animate(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time <= animation_cooldown:
            return

        self.update_time = pygame.time.get_ticks()
        self.frame_index = (self.frame_index + 1) % len(self.animation_list)

    def _move_with_platform(self):
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100:
            self.direction *= -1
            self.move_counter = 0
