from ability import Ability
import copy


class BaseCharacter:

    __name: str = ""
    __stats: dict[str, int] = {}
    __abilities: list[Ability] = []
    __sprite_location: str = ""

    def __init__(
        self,
        name: str,
        stats: dict,
        sprite_location: str,
        abilities: list[Ability],
    ) -> None:
        self.set_name(name)
        self.set_stats(stats)
        self.set_sprite_location(sprite_location)
        self.set_abilities(abilities)

    def copy(self) -> "BaseCharacter":
        return BaseCharacter(
            self.get_name(),
            copy.deepcopy(self.get_stats()),
            self.get_sprite_location(),
            self.get_abilities(),  
        )

    def get_name(self) -> str:
        return self.__name

    def get_sprite_location(self) -> str:
        return self.__sprite_location

    def get_stats(self) -> dict[str, int]:
        return self.__stats

    def get_abilities(self) -> list[Ability]:
        return self.__abilities

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_sprite_location(self, sprite_location: str) -> None:
        self.__sprite_location = sprite_location

    def set_stats(self, stats: dict[str, int]) -> None:
        self.__stats = stats

    def set_abilities(self, abilities: list[Ability]) -> None:
        self.__abilities = abilities
