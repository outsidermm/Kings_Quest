from .base_character import BaseCharacter


class Warrior(BaseCharacter):

    __statistics: dict = {
        "HP": 800,
        "Armor": 200,
        "Magic Resistance": 50,
        "Intelligence": 40,
        "Strength": 90,
        "Regeneration Rate": "10HP",
        "MP": 100,
        "Attack Damage": "90HP",
    }
    __name: str = None
    __unlocked_abilities: list = ["Power Slash"]

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(name, self.__statistics, sprite_location)
        self.__sprite_location = sprite_location
        self.__name = name

    def upgrade(self):
        if self.__character_level == 1:
            self.__character_level += 1
            self.__statistics["HP"] += 100
            self.__statistics["Strength"] += 90
        elif self.__character_level == 2:
            self.__character_level += 1
            pass  # Modify ability
        elif self.__character_level == 3:
            self.__character_level += 1
            self.__unlocked_abilities.append("War Cry")

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append("Shield War")

    def attack(self):
        pass

    def get_name(self) -> str:
        return self.__name

    def get_sprite_location(self) -> str:
        return self.__sprite_location
