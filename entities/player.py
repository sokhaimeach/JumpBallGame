import pygame

from settings import GRAVITY, SCREEN_WIDTH, SCROLL_THRESH


class Player:
    def __init__(self, x, y, ball_image, jump_sound):
        self.image = pygame.transform.scale(ball_image, (45, 45))
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        self.jump_sound = jump_sound

    def move(self, platform_group):
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False

        self.vel_y += GRAVITY
        dy += self.vel_y

        dx = self._keep_inside_screen(dx)
        self._bounce_on_platform(platform_group, dy)

        if self.rect.top <= SCROLL_THRESH and self.vel_y < 0:
            scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll
        return scroll

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 3, self.rect.y - 5))

    def _keep_inside_screen(self, dx):
        if self.rect.left + dx < 0:
            return -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            return SCREEN_WIDTH - self.rect.right
        return dx

    def _bounce_on_platform(self, platform_group, dy):
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = -20
                    self.jump_sound.play()
