# menu.py
import pygame
from settings import BLUE, WHITE, RED, YELLOW, GREEN, GRAY, SCREEN_WIDTH, SCREEN_HEIGHT
from button import Button
from game_functions import draw_text, draw_total_coins, back_button, draw_bg, create_platform_with_item, draw_panel
from season import Season
from spritesheet import SpriteSheet
from platforms import Platform
from player import Player
from settings import *
from data_manager import *
from ball import Ball

class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.font_big = pygame.font.SysFont("arial", 48, bold=True)
        self.font = pygame.font.SysFont("arial", 28)
        self.font_small = pygame.font.SysFont("arial", 22)

        # load data
        self.game_data = load_save_data()
        self.seasons = load_seasons()
        self.balls = load_balls()

        # play game variables
        self.scroll = 0
        self.bg_scroll = 0
        self.game_over = False
        self.quit = False
        self.score = 0
        self.fade_counter = 0
        self.block_click = False
        self.collect_coin = 0
        self.total_coins = self.game_data["coins"]
        self.high_score = self.game_data["high_score"]
        self.selected_season = self.seasons[self.game_data["selected_season"]]
        self.selected_ball = self.balls[self.game_data["selected_ball"]]

        # load images
        jump_ball_image = pygame.image.load(self.selected_ball["image"])
        self.bg_image = pygame.image.load(self.selected_season["background"]).convert_alpha()
        self.platform_image = pygame.image.load(self.selected_season["platform"]).convert_alpha()
        # coin image
        self.coin_sheet_img = pygame.image.load('assets/coins/coins.png').convert_alpha()
        self.coin_sheet = SpriteSheet(self.coin_sheet_img)
        # boom images
        self.boom_sheet_img = pygame.image.load('assets/boom/booms.png').convert_alpha()
        self.boom_sheet = SpriteSheet(self.boom_sheet_img)
        self.explosion_sheet_img = pygame.image.load('assets/boom/explosion.png').convert_alpha()
        self.explosion_sheet = SpriteSheet(self.explosion_sheet_img)
        self.back_btn_img = pygame.image.load("assets/backgrounds/back_btn.png").convert_alpha()
        self.coin_img = pygame.image.load("assets/coins/coin.png").convert_alpha()

        # load sound
        self.coin_sound = pygame.mixer.Sound("assets/audios/coin.mp3")
        self.jump_sound = pygame.mixer.Sound("assets/audios/jump_sound.mp3")
        self.boom_sound = pygame.mixer.Sound("assets/audios/boom.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/audios/game_over.wav")
        self.reach_high_score_sound = pygame.mixer.Sound("assets/audios/reach_high_score.wav")

        self.state = "start"
        self.season_group = pygame.sprite.Group()
        i = 1
        for key in self.seasons:
            self.season_group.add(
                Season(
                    20,
                    220 * i - 100, 
                    200,
                    key,
                    pygame.image.load(self.seasons[key]["background"]).convert_alpha(), 
                    self.seasons[key]["name"], 
                    self.seasons[key]["unlock_cost"],
                    True if key in self.game_data["unlocked_seasons"] else False,
                    True if self.game_data["selected_season"] == key else False
                )
            )
            i += 1

        self.ball_group = pygame.sprite.Group()
        i = 1
        for key in self.balls:
            self.ball_group.add(
                Ball(
                    20,
                    160 * i - 80,
                    90,
                    key,
                    pygame.image.load(self.balls[key]["image"]).convert_alpha(),
                    self.balls[key]["name"],
                    self.balls[key]["unlock_cost"],
                    key in self.game_data["unlocked_balls"],
                    self.game_data["selected_ball"] == key,
                    30
                )
            )
            i += 1


        # initialise for play game
        # player instance
        self.jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, jump_ball_image, self.jump_sound)

        # create sprite groups
        self.platform_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.boom_group = pygame.sprite.Group()

        # create starting platform
        self.platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, self.platform_image)
        self.platform_group.add(self.platform)

    # method use for refresh game ui when buy season or ball
    def refresh_shop_ui(self):
        self.game_data = load_save_data()

        self.total_coins = self.game_data["coins"]
        self.selected_season = self.seasons[self.game_data["selected_season"]]
        self.selected_ball = self.balls[self.game_data["selected_ball"]]

        jump_ball_image = pygame.image.load(self.selected_ball["image"])
        self.bg_image = pygame.image.load(self.selected_season["background"]).convert_alpha()
        self.platform_image = pygame.image.load(self.selected_season["platform"]).convert_alpha()
        
        self.jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, jump_ball_image, self.jump_sound)

        self.season_group.empty()
        self.ball_group.empty()

        # refresh seasons
        i = 1
        for key in self.seasons:
            self.season_group.add(
                Season(
                    20,
                    220 * i - 100,
                    200,
                    key,
                    pygame.image.load(self.seasons[key]["background"]).convert_alpha(),
                    self.seasons[key]["name"],
                    self.seasons[key]["unlock_cost"],
                    key in self.game_data["unlocked_seasons"],
                    self.game_data["selected_season"] == key
                )
            )
            i += 1

        # refresh balls
        i = 1
        for key in self.balls:
            self.ball_group.add(
                Ball(
                    20,
                    160 * i - 80,
                    90,
                    key,
                    pygame.image.load(self.balls[key]["image"]).convert_alpha(),
                    self.balls[key]["name"],
                    self.balls[key]["unlock_cost"],
                    key in self.game_data["unlocked_balls"],
                    self.game_data["selected_ball"] == key,
                    30
                )
            )
            i += 1

    def game_panel(self):
        draw_total_coins(self.screen, self.coin_img, self.total_coins, self.font)
        is_back = back_button(self.screen, self.back_btn_img)

        if is_back:
            self.state = "start"

    def start_screen(self):
        self.screen.fill((40, 120, 220))
        # draw game panel
        self.game_panel()

        draw_text(self.screen, "Walcome", self.font_big, WHITE, SCREEN_WIDTH // 2 - 85, 120)

        play_btn = Button(SCREEN_WIDTH // 2 - 110, 250, 220, 55, "PLAY", self.font, GREEN)
        season_btn = Button(SCREEN_WIDTH // 2 - 110, 320, 220, 55, "SEASONS", self.font, BLUE)
        shop_btn = Button(SCREEN_WIDTH // 2 - 110, 390, 220, 55, "SHOP", self.font, YELLOW)
        quit_btn = Button(SCREEN_WIDTH // 2 - 110, 460, 220, 55, "QUIT", self.font, RED)

        buttons = [
            (play_btn, "play"),
            (season_btn, "season"),
            (shop_btn, "shop"),
            (quit_btn, "quit")
        ]

        for btn, action in buttons:
            btn.draw(self.screen)
            if self.block_click:
                if not pygame.mouse.get_pressed()[0]:
                    self.block_click = False
                return
            else:
                if btn.clicked():
                    self.state = action


        # return buttons

    def season_screen(self):
        self.screen.fill((30, 30, 45))

        self.game_panel()

        need_refresh = False

        for season in self.season_group:
            season.draw(self.screen, self.font)

            if season.select(self.game_data, self.seasons):
                need_refresh = True

        if need_refresh:
            self.refresh_shop_ui()

    def shop_screen(self):
        self.screen.fill((35, 35, 45))

        self.game_panel()

        need_refresh = False

        for ball in self.ball_group:
            ball.draw(self.screen, self.font_small)

            if ball.select(self.game_data, self.balls):
                need_refresh = True

        if need_refresh:
            self.refresh_shop_ui()

    def reset(self):
        # update high score and coins
        if self.collect_coin > 0:
            self.game_data["coins"] += self.collect_coin
            self.collect_coin = 0

        if self.score > self.high_score:
            self.game_data["high_score"] = self.score
        save_game_data(self.game_data)

        # reset variagles
        self.game_over = False
        self.score = 0
        self.scroll = 0
        self.fade_counter = 0
        self.collect_coin = 0
        # reposition jumpy
        self.jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        # reset platforms and coins
        self.platform_group.empty()
        self.coin_group.empty()
        self.boom_group.empty()
        # create starting platform
        self.platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, self.platform_image)
        self.platform_group.add(self.platform)
        self.game_data = load_save_data()

        self.total_coins = self.game_data["coins"]

    def play(self):
        if not self.game_over:     
            self.scroll = self.jumpy.move(self.platform_group)
             

            # draw background
            # bg_scroll += scroll
            # if bg_scroll >= 800:
            #     bg_scroll = 0
            draw_bg(self.screen, self.bg_image, self.bg_scroll)

            # generate platforms
            if len(self.platform_group) < MAX_PLATFORMS:
                self.platform = create_platform_with_item(
                    self.platform_group,
                    self.coin_group,
                    self.boom_group,
                    self.platform,
                    self.score,
                    self.platform_image,
                    self.coin_sheet,
                    self.boom_sheet,
                    self.selected_season["enemy"]
                )

            # update platform positions
            self.platform_group.update(self.scroll)

            # update coin
            self.coin_group.update(self.scroll)

            # update boom
            if self.selected_season["enemy"] == "boom":
                self.boom_group.update(self.scroll)

                # check if player hit boom
                for boom in self.boom_group:
                    if self.jumpy.rect.colliderect(boom.rect) and boom.exploding == False:
                        self.boom_sound.play()
                        boom.explode(self.explosion_sheet)
                        self.scroll = 0

                    if boom.finished_exploding:
                        self.game_over_sound.play()
                        self.game_over = True

            # player hit the coin then count the collection
            hit_coin = pygame.sprite.spritecollide(self.jumpy, self.coin_group, True)
            if hit_coin:
                self.collect_coin += 1
                self.coin_sound.play()

            # update score
            if self.scroll > 0:
                self.score += self.scroll

            # draw line at previous high score
            pygame.draw.line(self.screen, WHITE, (0, self.score - self.high_score + SCROLL_THRESH), (SCREEN_WIDTH, self.score - self.high_score + SCROLL_THRESH), 3)
            draw_text(self.screen, "HIGH SCORE", self.font_small, WHITE, SCREEN_WIDTH - 130, self.score - self.high_score + SCROLL_THRESH)
            if self.scroll == self.high_score:
                self.reach_high_score_sound.play()

            # draw sprites
            self.platform_group.draw(self.screen)
            self.coin_group.draw(self.screen)
            self.boom_group.draw(self.screen)
            self.jumpy.draw(self.screen)

            # draw panel
            draw_panel(self.screen, self.score, self.collect_coin, self.font_small)

            # check game over
            if self.jumpy.rect.top > SCREEN_HEIGHT:
                self.game_over_sound.play()
                self.game_over = True



        else:
            if self.fade_counter < SCREEN_WIDTH:
                self.fade_counter += 5
                for y in range(0, 8, 2):
                    pygame.draw.rect(self.screen, BLACK, (0, y * 100, self.fade_counter, 100))
                    pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - self.fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
            else:
                # OVERLAY
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))

                # PANEL
                panel_w = 400
                panel_h = 320
                panel_x = (SCREEN_WIDTH - panel_w) // 2
                panel_y = 120

                pygame.draw.rect(
                    self.screen,
                    (25, 25, 40),
                    (panel_x, panel_y, panel_w, panel_h),
                    border_radius=25
                )

                pygame.draw.rect(
                    self.screen,
                    WHITE,
                    (panel_x, panel_y, panel_w, panel_h),
                    4,
                    border_radius=25
                )

                # TITLE
                draw_text(
                    self.screen,
                    "GAME OVER",
                    self.font_big,
                    (255, 70, 70),
                    panel_x + 75,
                    panel_y + 35
                )

                # ================= SCORE =================
                draw_text(
                    self.screen,
                    f"Coins : {self.collect_coin}",
                    self.font_big,
                    WHITE,
                    panel_x + 100,
                    panel_y + 110
                )

                play_btn = Button(panel_x + 50 , panel_y + 190, 300, 50, "Play Again", self.font_small, BLUE)
                home_btn = Button(panel_x + 50 , panel_y + 255, 300, 50, "Back Home", self.font_small, RED)

                play_btn.draw(self.screen)
                home_btn.draw(self.screen)

                if play_btn.clicked():
                    self.reset()

                if home_btn.clicked():
                    self.reset()
                    self.block_click = True
                    self.state = "start"
                  


    def run(self):
        if self.state == "start":
            self.start_screen()
            return
        
        if self.state == "play":
            self.play()
            return

        if self.state == "season":
            self.season_screen()
            return

        if self.state == "shop":
            self.shop_screen()
            return

        if self.state == "quit":
            self.quit = True