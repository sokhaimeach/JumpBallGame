import pygame
from settings import BLUE, WHITE

class Button:
    def __init__(self, x, y, w, h, text, font, color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.original_y = y

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(pos)

        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y = self.original_y + 4
        shadow_color = (max(0, self.color[0]-60), max(0, self.color[1]-60), max(0, self.color[2]-60))
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=15)

        # Draw main button
        draw_rect = self.rect.copy()
        if is_hover:
            draw_rect.y = self.original_y + 2
            color = (min(255, self.color[0]+30), min(255, self.color[1]+30), min(255, self.color[2]+30))
        else:
            draw_rect.y = self.original_y
            color = self.color
            
        # Update actual rect so clicks register correctly
        self.rect.y = draw_rect.y
        
        pygame.draw.rect(screen, color, draw_rect, border_radius=15)
        
        # Inner border
        pygame.draw.rect(screen, WHITE, draw_rect, 2, border_radius=15)

        text_img = self.font.render(self.text, True, WHITE)
        text_rect = text_img.get_rect(center=draw_rect.center)
        screen.blit(text_img, text_rect)

    def clicked(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos)
