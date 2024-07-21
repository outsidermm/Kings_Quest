from .base_character import BaseCharacter
from ability import Ability, ENEMY_ABILITY_LIST


class DreadNought(BaseCharacter):

    __statistics: dict[str, int] = {
        "health_points": 3000,  # High health to sustain long battles
        "physical_defense": 200,  # Strong physical defense
        "magical_defense": 150,  # Strong magical defense
        "spell_power": 120,  # High spell power for powerful magic attacks
        "physical_power": 150,  # High physical power for powerful physical attacks
        "health_regeneration": 20,  # Moderate health regeneration
        "mana_regeneration": 10,  # Moderate mana regeneration for sustained spell casting
        "mana_points": 250,  # Adequate mana pool for various spells
        "physical_damage": 70,  # Moderate physical damage per attack
        "magical_damage": 40,  # Moderate magical damage per attack
    }

    __unlocked_abilities: list[Ability] = [
        ENEMY_ABILITY_LIST["Savage Roar"],
        ENEMY_ABILITY_LIST["Flame Breath"],
        ENEMY_ABILITY_LIST["Tail Swipe"],
    ]

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(
            name,
            self.__statistics,
            sprite_location,
            self.__unlocked_abilities,
            self.__unlocked_abilities,
        )

    def upgrade(self) -> None:
        pass

    def unlock_ability(self) -> None:
        pass

    def get_name(self) -> str:
        return super().get_name()

    def get_sprite_location(self) -> str:
        return super().get_sprite_location()

    def get_statistics(self) -> dict:
        return super().get_statistics()

    def get_abilities(self) -> list[Ability]:
        return super().get_abilities()

    def get_unlocked_abilities(self) -> list[Ability]:
        return super().get_unlocked_abilities()

    def set_name(self, name: str) -> None:
        super().set_name(name)

    def set_sprite_location(self, sprite_location: str) -> None:
        super().set_sprite_location(sprite_location)

    def set_statistics(self, statistics: dict) -> None:
        super().set_statistics(statistics)

    def set_abilities(self, abilities: list[Ability]) -> None:
        super().set_abilities(abilities)

    def set_unlocked_abilities(self, unlocked_abilities: list[Ability]) -> None:
        super().set_unlocked_abilities(unlocked_abilities)
