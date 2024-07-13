from .base_character import BaseCharacter


class Berserker(BaseCharacter):

    __statistics: dict = {
        "HP": 1000,
        "Armor": 150,
        "Magic Resistance": 40,
        "Intelligence": 20,
        "Strength": 110,
        "Regeneration Rate": "15HP",
        "MP": 80,
        "Attack Damage": "110HP",
    }
    __name: str = None
    __unlocked_abilities: list = ["Reckless Charge"]

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(name, self.__statistics, sprite_location)
        self.__sprite_location = sprite_location
        self.__name = name

    def upgrade(self) -> None:
        if self.__character_level == 1:
            self.__character_level += 1
            self.__statistics["HP"] += 150
            self.__statistics["Strength"] += 15
        elif self.__character_level == 2:
            self.__character_level += 1
            pass  # Modify Reckless Charge
        elif self.__character_level == 3:
            self.__character_level += 1
            self.__unlocked_abilities.append("Bloodlust")

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append("Berserk")

    def attack(self) -> None:
        pass

    def get_name(self) -> str:
        return self.__name