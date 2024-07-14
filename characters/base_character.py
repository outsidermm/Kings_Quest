import abc


class BaseCharacter(abc.ABC):

    __name: str = None
    __statistics: dict = None
    __abilities: list = None
    __unlocked_abilities: list = []
    __character_level: int = 1
    __sprite_location: str = None

    def __init__(self, name: str, statistics: dict, sprite_location: str) -> None:
        self.__name = name
        self.__statistics = statistics
        self.__sprite_location = sprite_location

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
