import pygame

from screens.catalog_screen import CatalogScreen
from settings import SCREEN_HEIGHT


class SeasonScreen(CatalogScreen):
    def handle_event(self, event, app):
        if event.type == pygame.MOUSEWHEEL:
            app.season_scroll = self._clamp_scroll(app.season_scroll + event.y * 35, len(app.season_items), 220, 210)

    def render(self, app):
        app.screen.fill((30, 30, 45))
        app.draw_game_panel()

        needs_refresh = False
        self._position_items(app.season_items, 38, 120, 220, app.season_scroll)

        for season in app.season_items:
            if season.rect.bottom < 70 or season.rect.top > SCREEN_HEIGHT:
                continue

            season.draw(app.screen, app.font)
            if season.select(app.game_data, app.seasons, app.unlock_sound):
                needs_refresh = True

        if needs_refresh:
            app.refresh_shop_ui()
