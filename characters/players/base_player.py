import abc
from ability import Ability
from characters.base_character import BaseCharacter


class BasePlayer(abc.ABC, BaseCharacter):

    __unlocked_abilities: list[Ability] = []
    __character_level: int = None

    def __init__(
        self,
        name: str,
        statistics: dict,
        sprite_location: str,
        abilities: list[Ability],
        unlocked_abilities: list[Ability],
        character_level: int = 1,
    ) -> None:
        super().__init__(name, statistics, sprite_location, abilities)
        self.__character_level = character_level
        self.__unlocked_abilities = unlocked_abilities

    @abc.abstractmethod
    def upgrade(self) -> None:
        pass

    @abc.abstractmethod
    def unlock_ability(self) -> None:
        pass

    def get_name(self)->None:
        return super().get_name()
    
    def get_sprite_location(self)->None:
        return super().get_sprite_location()
    
    def get_statistics(self)->None:
        return super().get_statistics()
    
    def get_abilities(self)->None:
        return super().get_abilities()
    
    def set_name(self, name: str) -> None:
        super().set_name(name)
        
    def set_sprite_location(self, sprite_location: str) -> None:
        super().set_sprite_location(sprite_location)
        
    def set_statistics(self, statistics: dict[str, int]) -> None:
        super().set_statistics(statistics)
        
    def set_abilities(self, abilities: list[Ability]) -> None:
        super().set_abilities(abilities)

    def get_character_level(self) -> int:
        return self.__character_level

    def get_unlocked_abilities(self) -> list[Ability]:
        return self.__unlocked_abilities

    def set_character_level(self, character_level: int) -> None:
        self.__character_level = character_level

    def set_unlocked_abilities(self, unlocked_abilities: list[Ability]) -> None:
        self.__unlocked_abilities = unlocked_abilities
