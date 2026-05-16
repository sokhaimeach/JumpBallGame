import pygame
from settings import BLUE, WHITE

class Button:
    def __init__(self, x, y, w, h, text, font, color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        text_img = self.font.render(self.text, True, WHITE)
        text_rect = text_img.get_rect(center=self.rect.center)
        screen.blit(text_img, text_rect)

    def clicked(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos)
