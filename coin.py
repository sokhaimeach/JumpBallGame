import pygame
from settings import SCREEN_HEIGHT

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, moving, direction, speed, move_counter, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)

        # define variables 
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.moving = moving
        self.direction = direction
        self.speed = speed
        self.move_counter = move_counter

        # load images from spritesheet
        animation_steps = 9
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 50, 50, scale, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        # select starting image and create rectangle from it
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y

    def update(self, scroll):
        # update animation 
        ANIMATION_COOLDOWN = 100
        # update imate depending current frame
        self.image = self.animation_list[self.frame_index]
        # check if enough has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            # reset animation
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

        # moving platform sid to side if it is a moving platform
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        # change platform direction if it has moved fully
        if self.move_counter >= 100:
            self.direction *= -1
            self.move_counter = 0

        # move coin
        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()