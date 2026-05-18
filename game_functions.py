import pygame
import random
import sys
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, PANEL, YELLOW, BLUE, RED
from platforms import Platform
from coin import Coin
from boom import Boom
from button import Button

# functons for outputting text onto the screen
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing info panel in playing game
def draw_panel(screen, score, collect_coin, font_small):
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)

    draw_text(screen, "SCORE: " + str(score), font_small, WHITE, 0, 0)
    draw_text(screen, "Coin: " + str(collect_coin), font_small, WHITE, 300, 0)

# function for drawing the background
def draw_bg(screen, bg_image, bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -800 + bg_scroll))

# function for drawing panel for start game
def draw_total_coins(screen, coin_img, total_coins, font):
    # render text to know its width dynamically
    text_str = str(total_coins)
    text_img = font.render(text_str, True, YELLOW)
    text_width = text_img.get_width()
    text_height = text_img.get_height()
    
    # Calculate pill dimensions
    pill_height = 40
    pill_width = 57 + text_width
    pill_x = SCREEN_WIDTH - pill_width - 15
    pill_y = 12

    # Draw pill shadow
    shadow_rect = pygame.Rect(pill_x, pill_y + 3, pill_width, pill_height)
    pygame.draw.rect(screen, (10, 10, 15), shadow_rect, border_radius=20)

    # Draw pill background
    pill_rect = pygame.Rect(pill_x, pill_y, pill_width, pill_height)
    pygame.draw.rect(screen, (45, 45, 60), pill_rect, border_radius=20)
    
    # Draw pill border
    pygame.draw.rect(screen, (80, 80, 100), pill_rect, 2, border_radius=20)

    # Draw coin image
    coin = pygame.transform.scale(coin_img, (32, 32))
    screen.blit(coin, (pill_x + 4, pill_y + 4))

    # Draw text vertically centered
    text_y = pill_y + (pill_height - text_height) // 2
    screen.blit(text_img, (pill_x + 42, text_y))


# functions for draw game over
def draw_game_over(screen, font_big, font_small, collect_coin):
    # OVERLAY
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    # PANEL
    panel_w = 400
    panel_h = 340
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = 120
    pygame.draw.rect(
        screen,
        (25, 25, 40),
        (panel_x, panel_y, panel_w, panel_h),
        border_radius=25
    )
    pygame.draw.rect(
        screen,
        WHITE,
        (panel_x, panel_y, panel_w, panel_h),
        4,
        border_radius=25
    )
    # TITLE
    draw_text(
        screen,
        "GAME OVER",
        font_big,
        (255, 70, 70),
        panel_x + 75,
        panel_y + 35
    )
    # SCORE
    draw_text(
        screen,
        f"Coins : {collect_coin}",
        font_big,
        WHITE,
        panel_x + 100,
        panel_y + 110
    )
    play_btn = Button(panel_x + 50 , panel_y + 190, 300, 50, "Play Again", font_small, BLUE)
    home_btn = Button(panel_x + 50 , panel_y + 255, 300, 50, "Back Home", font_small, RED)
    play_btn.draw(screen)
    home_btn.draw(screen)

    return play_btn, home_btn


def create_platform_with_item(
    platform_group,
    coin_group,
    boom_group,
    platform,
    score,
    platform_image,
    coin_sheet,
    boom_sheet,
    enemy
):
    p_w = random.randint(80, 100)
    p_x = random.randint(0, SCREEN_WIDTH - p_w)
    p_y = platform.rect.y - random.randint(80, 120)

    p_type = random.randint(1, 2)
    p_moving = False
    if enemy == "moving_platform":
        p_moving =  p_type == 1 and score > 500

    new_platform = Platform(p_x, p_y, p_w, p_moving, platform_image)
    platform_group.add(new_platform)

    # generate coins
    random_item = random.randint(1, 100)
    if random_item <= 40:
        coin = Coin(
            platform.rect.centerx, 
            platform.rect.top - 10,
            platform.moving,
            platform.direction,
            platform.speed,
            platform.move_counter,
            coin_sheet, 0.5)
        coin_group.add(coin)
        
    # generate booms
    elif random_item <= 60 and score > 100 and enemy == "boom":
        boom = Boom(
            platform.rect.centerx, 
            platform.rect.top - 10,
            platform.moving,
            platform.direction,
            platform.speed,
            platform.move_counter,
            boom_sheet, 0.75)
        boom_group.add(boom)

    return new_platform


# function for locate file path
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# function for locate save file path
def save_path(filename):
    # for save data
    folder = os.path.join(os.getenv("APPDATA"), "JumpBallGame")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)