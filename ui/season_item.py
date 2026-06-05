from managers.data_manager import unlock_season
from ui.shop_item import ShopItem


class SeasonItem(ShopItem):
    def select(self, save_data, seasons, sound):
        if self.button.clicked():
            return unlock_season(save_data, self.key, seasons, sound)
        return False
