from characters.base_character import BaseCharacter
from ability import Ability
import copy


class BaseEnemy(BaseCharacter):

    def __init__(
        self,
        name: str,
        statistics: dict,
        sprite_location: str,
        abilities: list[Ability],
    ) -> None:
        super().__init__(name, statistics, sprite_location, abilities)

    def copy(self) -> "BaseEnemy":
        return BaseEnemy(
            self.get_name(),
            copy.deepcopy(self.get_statistics()),
            self.get_sprite_location(),
            copy.deepcopy(self.get_abilities()),
        )

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

    def set_statistics(self, statistics: dict[str, int]) -> None:
        super().set_statistics(statistics)

    def set_abilities(self, abilities: list[Ability]) -> None:
        super().set_abilities(abilities)
