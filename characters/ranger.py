from .base_character import BaseCharacter


class Ranger(BaseCharacter):

    __statistics: dict = {
        "HP": 600,
        "Armor": 100,
        "Magic Resistance": 60,
        "Intelligence": 50,
        "Strength": 70,
        "Regeneration Rate": "8HP",
        "MP": 150,
        "Attack Damage": "70HP",
    }
    __name: str = None
    __unlocked_abilities: list = ["Arrow Barrage"]

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(name, self.__statistics,sprite_location)
        self.__sprite_location = sprite_location
        self.__name = name

    def upgrade(self) -> None:
        if self.__character_level == 1:
            self.__character_level += 1
            self.__statistics["HP"] += 100
            self.__statistics["Strength"] += 10
        elif self.__character_level == 2:
            self.__character_level += 1
            pass  # Modify Arrow Barrage
        elif self.__character_level == 3:
            self.__character_level += 1
            self.__unlocked_abilities.append("Nature's Grace")

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append("Camouflage")

    def attack(self) -> None:
        pass

    def get_name(self) -> str:
        return self.__name