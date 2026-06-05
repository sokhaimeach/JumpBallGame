import pygame

from settings import BLACK, MAX_PLATFORMS, RED, SCROLL_THRESH, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from ui.button import Button
from utils.drawing import draw_background, draw_game_over, draw_text, draw_total_coins
from utils.platform_factory import create_platform_with_item


class GameScreen:
    def render(self, app):
        if app.game_over:
            self._render_game_over(app)
            return

        self._update_gameplay(app)
        self._draw_gameplay(app)
        self._handle_back_button(app)
        self._check_player_fell(app)

    def _update_gameplay(self, app):
        app.scroll = app.jumpy.move(app.platform_group)

        if len(app.platform_group) < MAX_PLATFORMS:
            app.platform = create_platform_with_item(
                app.platform_group,
                app.coin_group,
                app.boom_group,
                app.platform,
                app.score,
                app.platform_image,
                app.coin_sheet,
                app.boom_sheet,
                app.enemy_controller,
            )

        app.platform_group.update(app.scroll)
        app.coin_group.update(app.scroll)
        app.boom_group.update(app.scroll)
        self._handle_boom_collisions(app)

        app.enemy_controller.maybe_spawn_air_enemy(app.hazard_group, app.score)
        app.hazard_group.update(app.scroll)
        self._handle_hazard_collisions(app)
        self._collect_coins(app)

        if app.scroll > 0:
            app.score += app.scroll

    def _draw_gameplay(self, app):
        draw_background(app.screen, app.bg_image, app.bg_scroll)
        self._draw_high_score_line(app)

        app.platform_group.draw(app.screen)
        app.coin_group.draw(app.screen)
        app.boom_group.draw(app.screen)
        app.hazard_group.draw(app.screen)
        app.jumpy.draw(app.screen)

        draw_total_coins(app.screen, app.coin_img, app.collect_coin, app.font_small)
        draw_text(app.screen, "High: " + str(app.score) + "m", app.font_small, WHITE, SCREEN_WIDTH // 2 - 60, 20)

    def _handle_boom_collisions(self, app):
        for boom in app.boom_group:
            if app.jumpy.rect.colliderect(boom.rect) and not boom.exploding:
                app.boom_sound.set_volume(2)
                app.boom_sound.play()
                boom.explode(app.explosion_sheet)
                app.scroll = 0

            if boom.finished_exploding:
                app.game_over_sound.play()
                app.game_over = True

    def _handle_hazard_collisions(self, app):
        if pygame.sprite.spritecollide(app.jumpy, app.hazard_group, True):
            app.game_over_sound.play()
            app.game_over = True

    def _collect_coins(self, app):
        hit_coin = pygame.sprite.spritecollide(app.jumpy, app.coin_group, True)
        if hit_coin:
            app.collect_coin += 1
            app.coin_sound.play()

    def _draw_high_score_line(self, app):
        if app.high_score <= 0:
            return

        y = app.score - app.high_score + SCROLL_THRESH
        pygame.draw.line(app.screen, WHITE, (0, y), (SCREEN_WIDTH, y), 3)
        draw_text(app.screen, "HIGH SCORE", app.font_small, WHITE, SCREEN_WIDTH - 130, y)

        if app.score >= app.high_score and not app.high_score_played:
            app.reach_high_score_sound.play()
            app.high_score_played = True

    def _handle_back_button(self, app):
        back_btn = Button(15, 12, 90, 40, "Back", app.font_small, RED)
        back_btn.draw(app.screen)
        if back_btn.clicked():
            app.state = "start"
            app.reset_gameplay()

    def _check_player_fell(self, app):
        if app.jumpy.rect.top > SCREEN_HEIGHT:
            app.game_over_sound.play()
            app.game_over = True

    def _render_game_over(self, app):
        if app.fade_counter < SCREEN_WIDTH:
            app.fade_counter += 5
            for y in range(0, 8, 2):
                pygame.draw.rect(app.screen, BLACK, (0, y * 100, app.fade_counter, 100))
                pygame.draw.rect(app.screen, BLACK, (SCREEN_WIDTH - app.fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
            return

        play_btn, home_btn = draw_game_over(app.screen, app.font_big, app.font_small, app.collect_coin)
        if play_btn.clicked():
            app.reset_gameplay()

        if home_btn.clicked():
            app.reset_gameplay()
            app.block_click = True
            app.state = "start"
