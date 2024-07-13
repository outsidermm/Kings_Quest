from .base_character import BaseCharacter
from ability import PLAYER_ABILITY_LIST, Ability


class Mage(BaseCharacter):

    __statistics: dict = {
        "health_points": 500,  # Health Points
        "physical_defense": 50,  # Physical Defense
        "magical_defense": 100,  # Magical Defense
        "spell_power": 120,  # Spell Power
        "physical_power": 30,  # Physical Power
        "mana_regeneration": 5,  # Mana Regeneration per second
        "mana_points": 200,  # Mana Points
        "magical_damage": 30,  # Magical Damage per attack
    }
    __name: str = None
    __unlocked_abilities: list[Ability] = [
        PLAYER_ABILITY_LIST["Fireball"],
        PLAYER_ABILITY_LIST["Mana Surge"],
    ]
    __ability_list: list[Ability] = [
        PLAYER_ABILITY_LIST["Fireball"],
        PLAYER_ABILITY_LIST["Arcane Shield"],
        PLAYER_ABILITY_LIST["Mana Surge"],
    ]
    __character_level: int = 2

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
            self.__unlocked_abilities[0].upgrade()
        elif self.__character_level == 3:
            self.__character_level += 1
            self.__unlocked_abilities.append(PLAYER_ABILITY_LIST["Arcane Shield"])

    def unlock_ability(self) -> None:
        self.__unlocked_abilities.append(PLAYER_ABILITY_LIST["Mana Surge"])

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
