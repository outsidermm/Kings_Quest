from .base_character import BaseCharacter


class Berserker(BaseCharacter):

    __statistics: dict = {
        "health_points": 1000,  # Health Points
        "physical_defense": 150,  # Physical Defense
        "magical_defense": 40,  # Magical Defense
        "spell_power": 20,  # Spell Power
        "physical_power": 110,  # Physical Power
        "health_regeneration": 15,  # Health Regeneration per second
        "mana_points": 80,  # Mana Points
        "physical_damage": 110,  # Physical Damage per attack
    }

    __name: str = None
    __unlocked_abilities: list = ["Reckless Charge"]
    __character_level: int = 1

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

    def get_sprite_location(self) -> str:
        return self.__sprite_location

    def get_statistics(self) -> dict:
        return self.__statistics

    def get_character_level(self) -> int:
        return self.__character_level
