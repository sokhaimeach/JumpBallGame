import pygame

from settings import BLUE, WHITE


class Button:
    def __init__(self, x, y, width, height, text, font, color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.original_y = y

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        shadow_rect = self.rect.copy()
        shadow_rect.y = self.original_y + 4
        shadow_color = tuple(max(0, value - 60) for value in self.color)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=15)

        draw_rect = self.rect.copy()
        if is_hovered:
            draw_rect.y = self.original_y + 2
            color = tuple(min(255, value + 30) for value in self.color)
        else:
            draw_rect.y = self.original_y
            color = self.color

        self.rect.y = draw_rect.y

        pygame.draw.rect(screen, color, draw_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, draw_rect, 2, border_radius=15)

        text_img = self.font.render(self.text, True, WHITE)
        text_rect = text_img.get_rect(center=draw_rect.center)
        screen.blit(text_img, text_rect)

    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mouse_pos)
