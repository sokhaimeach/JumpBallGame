from shop_item import ShopItem
from data_manager import unlock_ball

class Ball(ShopItem):

    def select(self, save_data, balls):

        if self.button.clicked():

            is_select = unlock_ball(
                save_data,
                self.key,
                balls
            )

            return is_select

        return False