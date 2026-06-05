from managers.data_manager import unlock_ball
from ui.shop_item import ShopItem


class BallItem(ShopItem):
    def select(self, save_data, balls, sound):
        if self.button.clicked():
            return unlock_ball(save_data, self.key, balls, sound)
        return False
