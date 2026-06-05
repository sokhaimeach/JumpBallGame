import random

import pygame

from entities.boom import Boom
from entities.coin import Coin
from entities.enemy import Fireball, Laser, Meteor


class EnemyController:
    def __init__(self, enemies):
        self._enemies = self._normalize_enemies(enemies)
        self._air_enemy_factories = {
            "meteor": Meteor,
            "laser": Laser,
            "fireball": Fireball,
        }
        self._next_air_enemy_spawn_time = 0

    @property
    def enemies(self):
        return self._enemies

    def has(self, enemy_name):
        return enemy_name in self._enemies

    def platform_should_move(self, score):
        return self.has("moving_platform") and score > 500 and random.randint(1, 2) == 1

    def maybe_add_platform_item(
        self,
        platform,
        score,
        coin_group,
        boom_group,
        coin_sheet,
        boom_sheet,
    ):
        random_item = random.randint(1, 100)

        if random_item <= 40:
            coin_group.add(self._create_attached_coin(platform, coin_sheet))
            return

        if self.has("boom") and score > 100 and random_item <= 65:
            boom_group.add(self._create_attached_boom(platform, boom_sheet))

    def maybe_spawn_air_enemy(self, hazard_group, score):
        air_enemies = [enemy for enemy in self._air_enemy_factories if self.has(enemy)]
        if not air_enemies or score < 600 or len(hazard_group) >= 2:
            return

        current_time = pygame.time.get_ticks()
        if current_time < self._next_air_enemy_spawn_time:
            return

        # Air hazards are intentionally rate-limited so late-game seasons stay fair.
        cooldown = max(1800, 3200 - score // 3)
        self._next_air_enemy_spawn_time = current_time + cooldown

        chance = min(45, 20 + score // 900 + len(air_enemies) * 3)
        if random.randint(1, 100) <= chance:
            enemy_name = random.choice(air_enemies)
            hazard_group.add(self._air_enemy_factories[enemy_name](score))

    def _create_attached_coin(self, platform, coin_sheet):
        return Coin(
            platform.rect.centerx,
            platform.rect.top - 10,
            platform.moving,
            platform.direction,
            platform.speed,
            platform.move_counter,
            coin_sheet,
            0.5,
        )

    def _create_attached_boom(self, platform, boom_sheet):
        return Boom(
            platform.rect.centerx,
            platform.rect.top - 10,
            platform.moving,
            platform.direction,
            platform.speed,
            platform.move_counter,
            boom_sheet,
            0.75,
        )

    def _normalize_enemies(self, enemies):
        if isinstance(enemies, str):
            return (enemies,)

        if isinstance(enemies, (list, tuple, set)):
            return tuple(enemy for enemy in enemies if isinstance(enemy, str))

        return tuple()
