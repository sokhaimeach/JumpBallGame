import pygame

from entities.platform import Platform
from entities.player import Player
from managers.asset_manager import AssetManager
from managers.audio_manager import AudioManager
from managers.data_manager import load_balls, load_save_data, load_seasons, save_game_data
from managers.enemy_manager import EnemyController
from models.season_config import SeasonConfig
from screens.game_screen import GameScreen
from screens.season_screen import SeasonScreen
from screens.shop_screen import ShopScreen
from screens.start_screen import StartScreen
from settings import RED, SCREEN_HEIGHT, SCREEN_WIDTH
from ui.ball_item import BallItem
from ui.button import Button
from ui.season_item import SeasonItem
from utils.drawing import draw_total_coins
from utils.spritesheet import SpriteSheet


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont("arial", 48, bold=True)
        self.font = pygame.font.SysFont("arial", 28)
        self.font_small = pygame.font.SysFont("arial", 22)

        self.asset_manager = AssetManager()
        self.audio_manager = AudioManager()
        self.start_screen = StartScreen()
        self.season_screen = SeasonScreen()
        self.shop_screen = ShopScreen()
        self.game_screen = GameScreen()

        self.state = "start"
        self.quit = False
        self.block_click = False
        self.season_scroll = 0
        self.ball_scroll = 0

        self._load_catalog_data()
        self._load_assets()
        self._load_sounds()
        self._build_catalog_items()
        self.reset_gameplay(persist_progress=False)

    def handle_event(self, event):
        if self.state == "season":
            self.season_screen.handle_event(event, self)
        elif self.state == "shop":
            self.shop_screen.handle_event(event, self)

    def run(self):
        if self.state not in ("play", "quit") and pygame.mixer.get_init():
            if not pygame.mixer.get_busy():
                self.intro_sound.set_volume(0.5)
                self.intro_sound.play()

        if self.state == "start":
            self.start_screen.render(self)
        elif self.state == "play":
            self.intro_sound.stop()
            self.game_screen.render(self)
        elif self.state == "season":
            self.season_screen.render(self)
        elif self.state == "shop":
            self.shop_screen.render(self)
        elif self.state == "quit":
            self.quit = True

    def refresh_shop_ui(self):
        self._load_catalog_data()
        self.enemy_controller = EnemyController(self.selected_season.enemies)
        self._load_selected_game_assets()
        self._build_catalog_items()
        self.reset_gameplay(persist_progress=False)

    def reset_gameplay(self, persist_progress=True):
        if persist_progress:
            self._save_run_progress()

        self.game_over = False
        self.score = 0
        self.scroll = 0
        self.bg_scroll = 0
        self.fade_counter = 0
        self.collect_coin = 0
        self.high_score_played = False

        self._reload_save_totals()
        self._create_sprite_groups()
        self._create_player()
        self._create_starting_platform()

    def draw_game_panel(self):
        header_surface = pygame.Surface((SCREEN_WIDTH, 65), pygame.SRCALPHA)
        pygame.draw.rect(header_surface, (20, 20, 35, 220), (0, 0, SCREEN_WIDTH, 65))
        self.screen.blit(header_surface, (0, 0))

        pygame.draw.line(self.screen, (100, 100, 150), (0, 65), (SCREEN_WIDTH, 65), 3)
        draw_total_coins(self.screen, self.coin_img, self.total_coins, self.font)

        back_btn = Button(15, 12, 90, 40, "Back", self.font_small, RED)
        back_btn.draw(self.screen)
        if back_btn.clicked():
            self.state = "start"

    def _load_catalog_data(self):
        self.game_data = load_save_data()
        self.seasons = load_seasons()
        self.balls = load_balls()
        self.selected_season = self._get_selected_season()
        self.selected_ball = self._get_selected_ball()
        self.total_coins = self.game_data["coins"]
        self.high_score = self.game_data["high_score"]
        self.enemy_controller = EnemyController(self.selected_season.enemies)

    def _load_assets(self):
        self._load_selected_game_assets()
        self.coin_sheet_img = self.asset_manager.load_image("assets/coins/coins.png", (450, 50))
        self.coin_sheet = SpriteSheet(self.coin_sheet_img)
        self.boom_sheet_img = self.asset_manager.load_image("assets/enemies/boom/booms.png", (450, 50))
        self.boom_sheet = SpriteSheet(self.boom_sheet_img)
        self.explosion_sheet_img = self.asset_manager.load_image("assets/enemies/boom/explosion.png", (450, 50))
        self.explosion_sheet = SpriteSheet(self.explosion_sheet_img)
        self.coin_img = self.asset_manager.load_image("assets/coins/coin.png", (32, 32))

    def _load_selected_game_assets(self):
        self.jump_ball_image = self.asset_manager.load_image(self.selected_ball["image"], (45, 45))
        self.bg_image = self.asset_manager.load_image(self.selected_season.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.platform_image = self.asset_manager.load_image(self.selected_season.platform, (100, 15))

    def _load_sounds(self):
        self.coin_sound = self.audio_manager.load_sound("assets/audios/coin.mp3")
        self.jump_sound = self.audio_manager.load_sound("assets/audios/jump_sound.mp3")
        self.boom_sound = self.audio_manager.load_sound("assets/audios/boom.mp3")
        self.game_over_sound = self.audio_manager.load_sound("assets/audios/game_over.wav")
        self.reach_high_score_sound = self.audio_manager.load_sound("assets/audios/reach_high_score.wav")
        self.unlock_sound = self.audio_manager.load_sound("assets/audios/unlock.wav")
        self.intro_sound = self.audio_manager.load_sound("assets/audios/intro_game.mp3")

    def _build_catalog_items(self):
        self._build_season_items()
        self._build_ball_items()

    def _build_season_items(self):
        self.season_group = pygame.sprite.Group()
        self.season_items = []

        for index, key in enumerate(self.seasons, start=1):
            season_data = self.seasons[key]
            item = SeasonItem(
                38,
                220 * index - 100,
                180,
                key,
                self.asset_manager.load_image(season_data["background"], (180, 180)),
                season_data["name"],
                season_data["unlock_cost"],
                key in self.game_data["unlocked_seasons"],
                self.game_data["selected_season"] == key,
            )
            self.season_group.add(item)
            self.season_items.append(item)

    def _build_ball_items(self):
        self.ball_group = pygame.sprite.Group()
        self.ball_items = []

        for index, key in enumerate(self.balls, start=1):
            ball_data = self.balls[key]
            item = BallItem(
                80,
                160 * index - 50,
                90,
                key,
                self.asset_manager.load_image(ball_data["image"], (90, 90)),
                ball_data["name"],
                ball_data["unlock_cost"],
                key in self.game_data["unlocked_balls"],
                self.game_data["selected_ball"] == key,
                30,
            )
            self.ball_group.add(item)
            self.ball_items.append(item)

    def _get_selected_season(self):
        key = self.game_data.get("selected_season", "sky")
        if key not in self.seasons:
            key = "sky"
            self.game_data["selected_season"] = key

        return SeasonConfig(key, self.seasons[key])

    def _get_selected_ball(self):
        key = self.game_data.get("selected_ball", "red")
        if key not in self.balls:
            key = "red"
            self.game_data["selected_ball"] = key

        return self.balls[key]

    def _save_run_progress(self):
        if self.collect_coin > 0:
            self.game_data["coins"] += self.collect_coin

        if self.score > self.high_score:
            self.game_data["high_score"] = self.score

        save_game_data(self.game_data)

    def _reload_save_totals(self):
        self.game_data = load_save_data()
        self.total_coins = self.game_data["coins"]
        self.high_score = self.game_data["high_score"]

    def _create_sprite_groups(self):
        self.platform_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.boom_group = pygame.sprite.Group()
        self.hazard_group = pygame.sprite.Group()

    def _create_player(self):
        self.jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, self.jump_ball_image, self.jump_sound)

    def _create_starting_platform(self):
        self.platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, self.platform_image)
        self.platform_group.add(self.platform)
