import pygame

from screens.catalog_screen import CatalogScreen
from settings import SCREEN_HEIGHT


class ShopScreen(CatalogScreen):
    def handle_event(self, event, app):
        if event.type == pygame.MOUSEWHEEL:
            app.ball_scroll = self._clamp_scroll(app.ball_scroll + event.y * 35, len(app.ball_items), 160, 130)

    def render(self, app):
        app.screen.fill((35, 35, 45))
        app.draw_game_panel()

        needs_refresh = False
        self._position_items(app.ball_items, 80, 110, 160, app.ball_scroll)

        for ball in app.ball_items:
            if ball.rect.bottom < 70 or ball.rect.top > SCREEN_HEIGHT:
                continue

            ball.draw(app.screen, app.font_small)
            if ball.select(app.game_data, app.balls, app.unlock_sound):
                needs_refresh = True

        if needs_refresh:
            app.refresh_shop_ui()
