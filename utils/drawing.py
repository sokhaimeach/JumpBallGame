import pygame

from settings import BLUE, PANEL, RED, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, YELLOW
from ui.button import Button


def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_background(screen, bg_image, bg_scroll):
    screen.blit(bg_image, (0, bg_scroll))
    screen.blit(bg_image, (0, -800 + bg_scroll))


def draw_score_panel(screen, score, collect_coin, font_small):
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text(screen, "SCORE: " + str(score), font_small, WHITE, 0, 0)
    draw_text(screen, "Coin: " + str(collect_coin), font_small, WHITE, 300, 0)


def draw_total_coins(screen, coin_img, total_coins, font):
    text_str = str(total_coins)
    text_img = font.render(text_str, True, YELLOW)
    text_width = text_img.get_width()
    text_height = text_img.get_height()

    pill_height = 40
    pill_width = 57 + text_width
    pill_x = SCREEN_WIDTH - pill_width - 15
    pill_y = 12

    shadow_rect = pygame.Rect(pill_x, pill_y + 3, pill_width, pill_height)
    pygame.draw.rect(screen, (10, 10, 15), shadow_rect, border_radius=20)

    pill_rect = pygame.Rect(pill_x, pill_y, pill_width, pill_height)
    pygame.draw.rect(screen, (45, 45, 60), pill_rect, border_radius=20)
    pygame.draw.rect(screen, (80, 80, 100), pill_rect, 2, border_radius=20)

    coin = pygame.transform.scale(coin_img, (32, 32))
    screen.blit(coin, (pill_x + 4, pill_y + 4))

    text_y = pill_y + (pill_height - text_height) // 2
    screen.blit(text_img, (pill_x + 42, text_y))


def draw_game_over(screen, font_big, font_small, collect_coin):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    panel_w = 400
    panel_h = 340
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = 120
    panel_rect = (panel_x, panel_y, panel_w, panel_h)

    pygame.draw.rect(screen, (25, 25, 40), panel_rect, border_radius=25)
    pygame.draw.rect(screen, WHITE, panel_rect, 4, border_radius=25)

    draw_text(screen, "GAME OVER", font_big, (255, 70, 70), panel_x + 75, panel_y + 35)
    draw_text(screen, f"Coins : {collect_coin}", font_big, WHITE, panel_x + 100, panel_y + 110)

    play_btn = Button(panel_x + 50, panel_y + 190, 300, 50, "Play Again", font_small, BLUE)
    home_btn = Button(panel_x + 50, panel_y + 255, 300, 50, "Back Home", font_small, RED)
    play_btn.draw(screen)
    home_btn.draw(screen)
    return play_btn, home_btn
