from shop_item import ShopItem
from data_manager import unlock_ball

class Ball(ShopItem):

    def select(self, save_data, balls, sound):

        if self.button.clicked():

            is_select = unlock_ball(
                save_data,
                self.key,
                balls,
                sound
            )

            return is_select

        return False