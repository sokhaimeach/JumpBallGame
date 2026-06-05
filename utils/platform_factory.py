import random

from entities.platform import Platform
from settings import SCREEN_WIDTH


def create_platform_with_item(
    platform_group,
    coin_group,
    boom_group,
    previous_platform,
    score,
    platform_image,
    coin_sheet,
    boom_sheet,
    enemy_controller,
):
    platform_width = random.randint(80, 100)
    platform_x = random.randint(0, SCREEN_WIDTH - platform_width)
    platform_y = previous_platform.rect.y - random.randint(80, 120)
    moving = enemy_controller.platform_should_move(score)

    platform = Platform(platform_x, platform_y, platform_width, moving, platform_image)
    platform_group.add(platform)
    enemy_controller.maybe_add_platform_item(
        previous_platform,
        score,
        coin_group,
        boom_group,
        coin_sheet,
        boom_sheet,
    )
    return platform
