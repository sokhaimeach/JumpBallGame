import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, PANEL, YELLOW
from platforms import Platform
from coin import Coin
from boom import Boom

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
    coin = pygame.transform.scale(coin_img, (40, 40))

    screen.blit(coin, (SCREEN_WIDTH - 130, 15))

    draw_text(screen, str(total_coins), font, YELLOW, SCREEN_WIDTH - 85, 15)

def back_button(screen, btn_img):
    back_btn = pygame.transform.flip(btn_img, True, False)
    btn_rect = back_btn.get_rect(topleft=(10, 15))
    screen.blit(back_btn, btn_rect)

    pos = pygame.mouse.get_pos()

    return pygame.mouse.get_pressed()[0] and btn_rect.collidepoint(pos)

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