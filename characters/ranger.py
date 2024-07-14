from .base_character import BaseCharacter
from ability import PLAYER_ABILITY_LIST, Ability


class Ranger(BaseCharacter):

    __statistics: dict = {
        "health_points": 600,  # Health Points
        "physical_defense": 100,  # Physical Defense
        "magical_defense": 60,  # Magical Defense
        "spell_power": 50,  # Spell Power
        "physical_power": 70,  # Physical Power
        "health_regeneration": 8,  # Health Regeneration per second
        "mana_points": 150,  # Mana Points
        "physical_damage": 70,  # Physical Damage per attack
    }
    __name: str = None
    __unlocked_abilities: list[Ability] = [PLAYER_ABILITY_LIST["Arrow Barrage"]]
    __ability_list: list[Ability] = [
        PLAYER_ABILITY_LIST["Arrow Barrage"],
        PLAYER_ABILITY_LIST["Natural Grace"],
        PLAYER_ABILITY_LIST["Fatal Shadow"],
    ]
    __character_level: int = 4

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(name, self.__statistics, sprite_location)
        self.__sprite_location = sprite_location
        self.__name = name

    def upgrade(self) -> None:
        if self.__character_level == 1:
            self.__character_level += 1
            self.__statistics["health_points"] += 100
            self.__statistics["physical_power"] += 10
        elif self.__character_level == 2:
            self.__character_level += 1
            self.__unlocked_abilities[0].upgrade()
        elif self.__character_level == 3:
            self.__character_level += 1
            self.__unlocked_abilities.append(PLAYER_ABILITY_LIST["Natural Grace"])

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append(PLAYER_ABILITY_LIST["Fatal Shadow"])

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

    def get_ability_list(self) -> list[Ability]:
        return self.__ability_list

    def get_unlocked_abilities(self) -> list[Ability]:
        return self.__unlocked_abilities
