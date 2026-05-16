import pygame
from button import Button
from settings import BLUE, RED, GREEN, BLACK, WHITE

class ShopItem(pygame.sprite.Sprite):
    def __init__(self, x, y, width, key, image, name, cost, unlocked, selected=False, bth_h=45):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(
            image,
            (width, width)
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.key = key
        self.name = name
        self.cost = cost

        self.unlocked = unlocked
        self.selected = selected

        self.button = Button(
            x + width + 15,
            y + 45,
            160,
            bth_h,
            f"Unlock {cost}",
            pygame.font.SysFont("arial", 18, bold=True)
        )

    def draw(self, screen, font):
        
        # Background card panel
        card_rect = pygame.Rect(self.rect.x - 15, self.rect.y - 15, self.rect.width + 210, self.rect.height + 30)
        
        # Shadow
        shadow_rect = card_rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, (15, 15, 20), shadow_rect, border_radius=20)
        
        # Panel
        panel_color = (60, 60, 80) if self.selected else (45, 45, 60)
        pygame.draw.rect(screen, panel_color, card_rect, border_radius=20)

        # Highlight border
        if self.selected:
            pygame.draw.rect(screen, GREEN, card_rect, 4, border_radius=20)
        else:
            pygame.draw.rect(screen, (80, 80, 100), card_rect, 2, border_radius=20)

        # Draw image
        screen.blit(self.image, self.rect)

        # dark overlay for locked item
        if not self.unlocked:
            overlay = pygame.Surface(
                (self.rect.width, self.rect.height),
                pygame.SRCALPHA
            )
            pygame.draw.rect(overlay, (0, 0, 0, 180), overlay.get_rect(), border_radius=10)
            screen.blit(overlay, self.rect)

        # image border
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        # name text
        name_text = font.render(
            self.name,
            True,
            WHITE
        )
        screen.blit(
            name_text,
            (self.rect.x + self.rect.width + 15, self.rect.y + 5)
        )

        # button logic
        if not self.unlocked:
            self.button.color = RED
            self.button.text = f"Unlock {self.cost}"

        elif self.selected:
            self.button.color = GREEN
            self.button.text = "Selected"

        else:
            self.button.color = BLUE
            self.button.text = "Select"

        self.button.draw(screen)