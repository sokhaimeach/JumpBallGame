import pygame

from settings import BLUE, GREEN, RED, WHITE
from ui.button import Button


class ShopItem(pygame.sprite.Sprite):
    def __init__(self, x, y, width, key, image, name, cost, unlocked, selected=False, button_height=45):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, width))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.key = key
        self.name = name
        self.cost = cost
        self.unlocked = unlocked
        self.selected = selected

        self.button = Button(
            x + width + 15,
            y + 45,
            160,
            button_height,
            f"Unlock {cost}",
            pygame.font.SysFont("arial", 18, bold=True),
        )

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.button.rect.x = x + self.rect.width + 15
        self.button.rect.y = y + 45
        self.button.original_y = self.button.rect.y

    def draw(self, screen, font):
        card_rect = pygame.Rect(self.rect.x - 15, self.rect.y - 15, self.rect.width + 210, self.rect.height + 30)

        shadow_rect = card_rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, (15, 15, 20), shadow_rect, border_radius=20)

        panel_color = (60, 60, 80) if self.selected else (45, 45, 60)
        pygame.draw.rect(screen, panel_color, card_rect, border_radius=20)

        border_color = GREEN if self.selected else (80, 80, 100)
        border_width = 4 if self.selected else 2
        pygame.draw.rect(screen, border_color, card_rect, border_width, border_radius=20)

        screen.blit(self.image, self.rect)
        if not self.unlocked:
            self._draw_locked_overlay(screen)

        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        self._draw_name(screen, font)
        self._update_button_state()
        self.button.draw(screen)

    def _draw_locked_overlay(self, screen):
        overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 180), overlay.get_rect(), border_radius=10)
        screen.blit(overlay, self.rect)

    def _draw_name(self, screen, font):
        name_text = font.render(self.name, True, WHITE)
        screen.blit(name_text, (self.rect.x + self.rect.width + 15, self.rect.y + 5))

    def _update_button_state(self):
        if not self.unlocked:
            self.button.color = RED
            self.button.text = f"Unlock {self.cost}"
        elif self.selected:
            self.button.color = GREEN
            self.button.text = "Selected"
        else:
            self.button.color = BLUE
            self.button.text = "Select"
