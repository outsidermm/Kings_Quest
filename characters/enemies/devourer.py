from characters.enemies.base_enemy import BaseEnemy
from ability import Ability, ENEMY_ABILITY_LIST
import copy


class Devourer(BaseEnemy):

    __statistics: dict[str, int] = {
        "health_points": 1700,
        "physical_defense": 200,
        "magical_defense": 150,
        "spell_power": 150,
        "physical_power": 120,
        "health_regeneration": 15,
        "mana_regeneration": 15,
        "mana_points": 250,
        "physical_damage": 60,
        "magical_damage": 40,
    }

    __abilities: list[Ability] = [
        ENEMY_ABILITY_LIST["Savage Roar"],
        ENEMY_ABILITY_LIST["Flame Breath"],
        ENEMY_ABILITY_LIST["Tail Swipe"],
    ]

    def __init__(self, sprite_location: str) -> None:
        super().__init__(
            "Devourer",
            copy.deepcopy(self.__statistics),
            sprite_location,
            self.__abilities,
        )

    def copy(self) -> "Devourer":
        return Devourer(self.get_sprite_location())

    def get_name(self) -> str:
        return super().get_name()

    def get_sprite_location(self) -> str:
        return super().get_sprite_location()

    def get_statistics(self) -> dict:
        return super().get_statistics()

    def get_abilities(self) -> list[Ability]:
        return super().get_abilities()

    def set_name(self, name: str) -> None:
        super().set_name(name)

    def set_sprite_location(self, sprite_location: str) -> None:
        super().set_sprite_location(sprite_location)

    def set_statistics(self, statistics: dict) -> None:
        super().set_statistics(statistics)

    def set_abilities(self, abilities: list[Ability]) -> None:
        super().set_abilities(abilities)
