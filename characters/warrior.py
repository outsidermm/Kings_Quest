from .base_character import BaseCharacter
from ability import PLAYER_ABILITY_LIST, Ability


class Warrior(BaseCharacter):

    __statistics: dict = {
        "health_points": 800,  # Health Points
        "physical_defense": 200,  # Physical Defense
        "magical_defense": 50,  # Magical Defense
        "spell_power": 40,  # Spell Power
        "physical_power": 90,  # Physical Power
        "health_regeneration": 10,  # Health Regeneration per second
        "mana_points": 100,  # Mana Points
        "physical_damage": 90,  # Physical Damage per attack
    }
    __name: str = None
    __unlocked_abilities: list[Ability] = [PLAYER_ABILITY_LIST["Power Slash"]]
    __ability_list: list[Ability] = [
        PLAYER_ABILITY_LIST["Power Slash"],
        PLAYER_ABILITY_LIST["War Cry"],
        PLAYER_ABILITY_LIST["Shield War"],
    ]
    __character_level: int = 1

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
            self.__unlocked_abilities.append(PLAYER_ABILITY_LIST["War Cry"])

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append(PLAYER_ABILITY_LIST["Shield War"])

    def attack(self):
        pass

    def get_name(self) -> str:
        return self.__name

    def get_sprite_location(self) -> str:
        return self.__sprite_location

    def get_statistics(self) -> dict:
        return self.__statistics

    def get_character_level(self) -> int:
        return self.__character_level

    def get_ability_list(self) -> list[Ability]:
        return self.__ability_list

    def get_unlocked_abilities(self) -> list[Ability]:
        return self.__unlocked_abilities
