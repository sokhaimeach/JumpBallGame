import pygame

from settings import BLUE, GREEN, RED, SCREEN_WIDTH, WHITE, YELLOW
from ui.button import Button
from utils.drawing import draw_text


class StartScreen:
    def render(self, app):
        app.screen.fill((40, 120, 220))
        app.draw_game_panel()

        draw_text(app.screen, "JUMP BALL", app.font_big, WHITE, SCREEN_WIDTH // 2 - 110, 120)

        buttons = [
            (Button(SCREEN_WIDTH // 2 - 110, 250, 220, 55, "PLAY", app.font, GREEN), "play"),
            (Button(SCREEN_WIDTH // 2 - 110, 320, 220, 55, "SEASONS", app.font, BLUE), "season"),
            (Button(SCREEN_WIDTH // 2 - 110, 390, 220, 55, "SHOP", app.font, YELLOW), "shop"),
            (Button(SCREEN_WIDTH // 2 - 110, 460, 220, 55, "QUIT", app.font, RED), "quit"),
        ]

        for button, action in buttons:
            button.draw(app.screen)
            if app.block_click:
                if not pygame.mouse.get_pressed()[0]:
                    app.block_click = False
                return

            if button.clicked():
                app.state = action
