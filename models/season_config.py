class SeasonConfig:
    def __init__(self, key, data):
        self.key = key
        self.name = data.get("name", key.title())
        self.background = data.get("background", "")
        self.platform = data.get("platform", "")
        self.enemies = self._read_enemies(data.get("enemy", []))
        self.unlock_cost = data.get("unlock_cost", 0)

    def has_enemy(self, enemy_name):
        return enemy_name in self.enemies

    def to_dict(self):
        return {
            "name": self.name,
            "background": self.background,
            "platform": self.platform,
            "enemy": list(self.enemies),
            "unlock_cost": self.unlock_cost,
        }

    def _read_enemies(self, enemies):
        if isinstance(enemies, str):
            return (enemies,)

        if isinstance(enemies, (list, tuple, set)):
            return tuple(enemy for enemy in enemies if isinstance(enemy, str))

        return tuple()
