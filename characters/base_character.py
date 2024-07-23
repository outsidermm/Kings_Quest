from ability import Ability
import copy


class BaseCharacter:

    __name: str = ""
    __statistics: dict[str, int] = {}
    __abilities: list[Ability] = []
    __sprite_location: str = ""

    def __init__(
        self,
        name: str,
        statistics: dict,
        sprite_location: str,
        abilities: list[Ability],
    ) -> None:
        self.__name = name
        self.__statistics = statistics
        self.__sprite_location = sprite_location
        self.__abilities = abilities

    def copy(self) -> "BaseCharacter":
        return BaseCharacter(
            self.__name,
            copy.deepcopy(self.__statistics),
            self.__sprite_location,
            self.__abilities,
        )

    def get_name(self) -> str:
        return self.__name

    def get_sprite_location(self) -> str:
        return self.__sprite_location

    def get_statistics(self) -> dict[str, int]:
        return self.__statistics

    def get_abilities(self) -> list[Ability]:
        return self.__abilities

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_sprite_location(self, sprite_location: str) -> None:
        self.__sprite_location = sprite_location

    def set_statistics(self, statistics: dict[str, int]) -> None:
        self.__statistics = statistics

    def set_abilities(self, abilities: list[Ability]) -> None:
        self.__abilities = abilities
