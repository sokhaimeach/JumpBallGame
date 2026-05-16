import pygame
from button import Button
from settings import BLUE, RED, GREEN, BLACK, WHITE

class ShopItem(pygame.sprite.Sprite):
    def __init__(self, x, y, width, key, image, name, cost, unlocked, selected=False, bth_h=50):

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
            x + width + 10,
            y + 50,
            170,
            bth_h,
            f"Unlock {cost}",
            pygame.font.SysFont("arial", 20)
        )

    def draw(self, screen, font):

        screen.blit(self.image, self.rect)

        # dark overlay
        if not self.unlocked:
            overlay = pygame.Surface(
                (self.rect.width, self.rect.height)
            )

            overlay.set_alpha(180)
            overlay.fill(BLACK)

            screen.blit(overlay, self.rect)

        # border
        if self.selected:
            pygame.draw.rect(
                screen,
                GREEN,
                self.rect,
                5,
                border_radius=10
            )
        else:
            pygame.draw.rect(
                screen,
                WHITE,
                self.rect,
                3,
                border_radius=10
            )

        # name
        name_text = font.render(
            self.name,
            True,
            WHITE
        )

        screen.blit(
            name_text,
            (self.rect.x + self.rect.width + 10, self.rect.y + 8)
        )

        # button
        if not self.unlocked:
            self.button.color = RED
            self.button.text = f"Unlock {self.cost}"

        elif self.selected:
            self.button.color = GREEN
            self.button.text = "Selected"

        else:
            self.button.color = BLUE
            self.button.text = "Click to Select"

        self.button.draw(screen)