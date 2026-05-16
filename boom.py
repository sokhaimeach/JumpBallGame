from coin import Coin
import pygame

class Boom(Coin):
    def __init__(self, x, y, moving, direction, speed, move_counter, sprite_sheet, scale):
        super().__init__(x, y, moving, direction, speed, move_counter, sprite_sheet, scale)
        self.exploding = False
        self.finished_exploding = False

    
    def update(self, scroll):
        super().update(scroll)
    
        if self.exploding and self.frame_index >= len(self.animation_list) - 1:
            self.finished_exploding = True
            # self.kill()
    
    def explode(self, explosion_sheet):
        self.exploding = True
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        for i in range(9):
            image = explosion_sheet.get_image(i, 50, 50, 1, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        center = self.rect.center
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center