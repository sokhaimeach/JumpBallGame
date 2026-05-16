import pygame
from settings import SCREEN_WIDTH, SCROLL_THRESH, GRAVITY, WHITE

# player class
class Player():
    def __init__(self, x, y, jump_ball_image, jump_sound):
        self.image = pygame.transform.scale(jump_ball_image, (45, 45))
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.filp = False
        self.jump_sound = jump_sound

    def move(self, platform_group):
        # reset vaiables
        scroll = 0
        dx = 0
        dy = 0

        # process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx = -10
            self.filp = True
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx = 10
            self.filp = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # check collision with platforms
        for platform in platform_group:
            # collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = -20
                        self.jump_sound.play()

        

        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.filp, False), (self.rect.x - 3, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)
