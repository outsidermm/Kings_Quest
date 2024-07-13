from .base_character import BaseCharacter


class Mage(BaseCharacter):

    __statistics: dict = {
        "HP": 500,
        "Armor": 50,
        "Magic Resistance": 100,
        "Intelligence": 120,
        "Strength": 30,
        "Regeneration Rate": "5MP",
        "MP": 200,
        "Attack Damage": "30MP",
    }
    __name: str = None
    __unlocked_abilities: list = ["Fireball"]

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(name, self.__statistics, sprite_location)
        self.__sprite_location = sprite_location
        self.__name = name

    def upgrade(self) -> None:
        if self.__character_level == 1:
            self.__character_level += 1
            self.__statistics["Intelligence"] += 15
            self.__statistics["MP"] += 50
        elif self.__character_level == 2:
            self.__character_level += 1
            pass  # Modify Fireball
        elif self.__character_level == 3:
            self.__character_level += 1
            self.__unlocked_abilities.append("Arcane Shield")

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append("Mana Surge")

    def attack(self):
        pass

    def get_name(self) -> str:
        return self.__name

    def get_sprite_location(self) -> str:
        return self.__sprite_location
