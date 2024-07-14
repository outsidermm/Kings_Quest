from .base_character import BaseCharacter
from ability import PLAYER_ABILITY_LIST, Ability


class Mage(BaseCharacter):

    __statistics: dict[str, int] = {
        "health_points": 500,  # Health Points
        "physical_defense": 50,  # Physical Defense
        "magical_defense": 100,  # Magical Defense
        "spell_power": 120,  # Spell Power
        "physical_power": 30,  # Physical Power
        "mana_regeneration": 5,  # Mana Regeneration per second
        "mana_points": 200,  # Mana Points
        "magical_damage": 30,  # Magical Damage per attack
    }
    __unlocked_abilities: list[Ability] = [
        PLAYER_ABILITY_LIST["Fireball"],
        PLAYER_ABILITY_LIST["Mana Surge"],
    ]
    __abilities: list[Ability] = [
        PLAYER_ABILITY_LIST["Fireball"],
        PLAYER_ABILITY_LIST["Arcane Shield"],
        PLAYER_ABILITY_LIST["Mana Surge"],
    ]
    __character_level: int = 2

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(
            name,
            self.__statistics,
            sprite_location,
            self.__abilities,
            self.__unlocked_abilities,
            self.__character_level,
        )

    def upgrade(self) -> None:

        new_statistic : dict[str,int]= self.get_statistics()
        new_unlocked_abilities :list[Ability]= self.get_unlocked_abilities()
        if self.__character_level == 1:
            self.set_character_level(2)
            new_statistic["spell_power"] += 15
            new_statistic["mana_points"] += 50
        elif self.__character_level == 2:
            self.set_character_level(3)
            new_unlocked_abilities[0].upgrade()
        elif self.__character_level == 3:
            self.set_character_level(4)
            new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Arcane Shield"])
        self.set_statistics(new_statistic)
        self.set_unlocked_abilities(new_unlocked_abilities)

    def unlock_ability(self) -> None:
        new_unlocked_abilities :list[Ability]= self.get_unlocked_abilities()
        new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Mana Surge"])
        self.set_unlocked_abilities(new_unlocked_abilities)

    def attack(self):
        pass

    def get_name(self) -> str:
        return super().get_name()

    def get_sprite_location(self) -> str:
        return super().get_sprite_location()

    def get_statistics(self) -> dict:
        return super().get_statistics()

    def get_character_level(self) -> int:
        return super().get_character_level()

    def get_abilities(self) -> list[Ability]:
        return super().get_abilities()

    def get_unlocked_abilities(self) -> list[Ability]:
        return super().get_unlocked_abilities()
