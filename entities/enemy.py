import random

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from utils.paths import resource_path
from utils.spritesheet import SpriteSheet


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def destroy_if_off_screen(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class AnimatedEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def animate(self, loop=True):
        if not self.animation_list:
            return False

        animation_cooldown = 100
        self.image = self.animation_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time <= animation_cooldown:
            return False

        self.update_time = pygame.time.get_ticks()
        self.frame_index += 1

        if self.frame_index < len(self.animation_list):
            return False

        if loop:
            self.frame_index = 0
            return False

        self.frame_index = len(self.animation_list) - 1
        return True

    def load_frames(self, sprite_sheet, frame_count, width, height, scale):
        self.animation_list = []
        for frame in range(frame_count):
            image = sprite_sheet.get_image(frame, width, height, scale, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)


class AttachedEnemy(AnimatedEnemy):
    def __init__(self, x, y, moving, direction, speed, move_counter):
        super().__init__()
        self.moving = moving
        self.direction = direction
        self.speed = speed
        self.move_counter = move_counter

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def move_with_platform(self, scroll):
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100:
            self.direction *= -1
            self.move_counter = 0

        self.rect.y += scroll
        self.destroy_if_off_screen()

    def update(self, scroll):
        self.animate()
        self.move_with_platform(scroll)


class FallingEnemy(AnimatedEnemy):
    def __init__(self, enemy_type, score):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-140, -40)
        self.speed_y = random.randint(4, 7) + min(4, score // 1500)
        self.speed_x = random.choice([-1, 0, 1])

    def update(self, scroll):
        self.animate()
        self.rect.y += self.speed_y + scroll
        self.rect.x += self.speed_x

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1

        self.destroy_if_off_screen()


class Fireball(FallingEnemy):
    def __init__(self, score):
        super().__init__("fireball", score)
        self.load_frames_from_asset()
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect(center=self.rect.center)

    def load_frames_from_asset(self):
        try:
            image = pygame.image.load(resource_path("assets/enemies/fireball_frames.png")).convert_alpha()
            self.load_frames(SpriteSheet(image), 9, 50, 50, 0.85)
        except (FileNotFoundError, pygame.error) as error:
            print(f"Could not load fireball enemy: {error}")
            self.animation_list = [self.create_fallback_image()]

    def create_fallback_image(self):
        image = pygame.Surface((38, 38), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 100, 35), (19, 19), 18)
        pygame.draw.circle(image, (255, 230, 60), (13, 13), 7)
        return image


class Meteor(FallingEnemy):
    def __init__(self, score):
        super().__init__("meteor", score)
        self.image = self.load_image()
        self.rect = self.image.get_rect(center=self.rect.center)

    def load_image(self):
        try:
            image = pygame.image.load(resource_path("assets/enemies/meteor.png")).convert_alpha()
            return pygame.transform.scale(image, (46, 46))
        except (FileNotFoundError, pygame.error) as error:
            print(f"Could not load meteor enemy: {error}")
            return self.create_fallback_image()

    def create_fallback_image(self):
        image = pygame.Surface((42, 42), pygame.SRCALPHA)
        pygame.draw.circle(image, (95, 95, 105), (21, 21), 20)
        pygame.draw.circle(image, (255, 120, 35), (15, 15), 7)
        return image


class Laser(FallingEnemy):
    def __init__(self, score):
        super().__init__("laser", score)
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.rect.center)

    def create_image(self):
        image = pygame.Surface((12, 80), pygame.SRCALPHA)
        pygame.draw.rect(image, (255, 30, 80), (3, 0, 6, 80), border_radius=3)
        pygame.draw.rect(image, (255, 200, 215), (5, 0, 2, 80), border_radius=2)
        return image
