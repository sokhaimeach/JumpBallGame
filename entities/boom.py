import pygame

from entities.enemy import AttachedEnemy


class Boom(AttachedEnemy):
    def __init__(self, x, y, moving, direction, speed, move_counter, sprite_sheet, scale):
        super().__init__(x, y, moving, direction, speed, move_counter)
        self.load_frames(sprite_sheet, 9, 50, 50, scale)
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.exploding = False
        self.finished_exploding = False

    def update(self, scroll):
        reached_last_frame = self.animate(loop=not self.exploding)
        self.move_with_platform(scroll)

        if self.exploding and reached_last_frame:
            self.finished_exploding = True

    def explode(self, explosion_sheet):
        self.exploding = True
        self.finished_exploding = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.load_frames(explosion_sheet, 9, 50, 50, 1)

        center = self.rect.center
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
