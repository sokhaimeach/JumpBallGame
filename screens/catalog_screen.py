from settings import SCREEN_HEIGHT


class CatalogScreen:
    def _clamp_scroll(self, scroll, item_count, gap, item_height):
        content_bottom = 120 + max(0, item_count - 1) * gap + item_height
        min_scroll = min(0, SCREEN_HEIGHT - content_bottom - 30)
        return max(min(scroll, 0), min_scroll)

    def _position_items(self, items, x, start_y, gap, scroll):
        for index, item in enumerate(items):
            item.set_position(x, start_y + gap * index + scroll)
