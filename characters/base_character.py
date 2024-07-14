import abc
from ability import Ability


class BaseCharacter(abc.ABC):

    __name: str = ""
    __statistics: dict[str, int] = {}
    __abilities: list[Ability] = []
    __unlocked_abilities: list[Ability] = []
    __character_level: int = None
    __sprite_location: str = ""

    def __init__(
        self,
        name: str,
        statistics: dict,
        sprite_location: str,
        abilities: list[Ability],
        unlocked_abilities: list[Ability],
        character_level: int = 1,
    ) -> None:
        self.__name = name
        self.__statistics = statistics
        self.__sprite_location = sprite_location
        self.__character_level = character_level
        self.__abilities = abilities
        self.__unlocked_abilities = unlocked_abilities

    @abc.abstractmethod
    def upgrade(self) -> None:
        pass

    @abc.abstractmethod
    def attack(self) -> None:
        pass

    @abc.abstractmethod
    def unlock_ability(self) -> None:
        pass

    def get_name(self) -> str:
        return self.__name

    def get_sprite_location(self) -> str:
        return self.__sprite_location

    def get_statistics(self) -> dict[str, int]:
        return self.__statistics

    def get_character_level(self) -> int:
        return self.__character_level

    def get_abilities(self) -> list[Ability]:
        return self.__abilities

    def get_unlocked_abilities(self) -> list[Ability]:
        return self.__unlocked_abilities

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_sprite_location(self, sprite_location: str) -> None:
        self.__sprite_location = sprite_location

    def set_statistics(self, statistics: dict[str, int]) -> None:
        self.__statistics = statistics

    def set_character_level(self, character_level: int) -> None:
        self.__character_level = character_level

    def set_abilities(self, abilities: list[Ability]) -> None:
        self.__abilities = abilities

    def set_unlocked_abilities(self, unlocked_abilities: list[Ability]) -> None:
        self.__unlocked_abilities = unlocked_abilities
