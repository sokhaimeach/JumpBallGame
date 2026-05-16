from shop_item import ShopItem
from data_manager import unlock_season

class Season(ShopItem):

    def select(self, save_data, seasons, sound):

        if self.button.clicked():

            is_select = unlock_season(
                save_data,
                self.key,
                seasons,
                sound
            )

            return is_select

        return False