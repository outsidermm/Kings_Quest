import abc
from ability import Ability
from characters.base_character import BaseCharacter
import copy
from utilities.json_utility import read_json, write_json


class BasePlayer(abc.ABC, BaseCharacter):
    """
    BasePlayer is an abstract base class for player characters in the game.
    It extends BaseCharacter and provides additional functionality specific to player characters.

    Attributes:
        __unlocked_abilities (list[Ability]): List of abilities unlocked by the player.
        __character_level (int): Current level of the player character.

    Methods:
        copy: Creates a deep copy of the player instance.
        upgrade: Abstract method to upgrade the player character.
        unlock_ability: Abstract method to unlock a new ability for the player character.
        get_character_level: Gets the character level.
        get_unlocked_abilities: Gets the list of unlocked abilities.
        set_character_level: Sets the character level and updates the user settings file.
        set_unlocked_abilities: Sets the unlocked abilities and updates the user settings file.
    """

    __unlocked_abilities: list[Ability] = []
    __character_level: int = 1

    def __init__(
        self,
        name: str,
        stats: dict,
        sprite_location: str,
        abilities: list[Ability],
        unlocked_abilities: list[Ability],
        character_level: int = 1,
    ) -> None:
        """
        Initializes the BasePlayer class with the provided attributes.

        :param name: The name of the player character.
        :param stats: Dictionary containing the player's stats.
        :param sprite_location: The file path to the player's sprite image.
        :param abilities: List of abilities the player possesses.
        :param unlocked_abilities: List of abilities unlocked by the player.
        :param character_level: Initial level of the player character.
        """
        super().__init__(name, stats, sprite_location, abilities)
        self.set_character_level(character_level)
        self.set_unlocked_abilities(unlocked_abilities)

    def copy(self) -> "BasePlayer":
        """
        Creates a copy of the current player instance.

        :return: A new instance of BasePlayer with the same attributes.
        """
        return self.__class__(
            self.get_name(),
            copy.deepcopy(self.get_stats()),  # Deep copy the stats dictionary
            self.get_sprite_location(),
            self.get_abilities(),
            self.get_unlocked_abilities(),
            self.get_character_level(),
        )

    @abc.abstractmethod
    def upgrade(self) -> None:
        """
        Abstract method to upgrade the player character.
        Subclasses must implement this method.
        """
        pass

    @abc.abstractmethod
    def unlock_ability(self) -> None:
        """
        Abstract method to unlock a new ability for the player character.
        Subclasses must implement this method.
        """
        pass

    def get_character_level(self) -> int:
        """
        Gets the character level.

        :return: Character level.
        """
        return self.__character_level

    def get_unlocked_abilities(self) -> list[Ability]:
        """
        Gets the list of unlocked abilities.

        :return: List of unlocked abilities.
        """
        return self.__unlocked_abilities

    def set_character_level(self, character_level: int) -> None:
        """
        Sets the character level and updates the user settings file.

        :param character_level: New character level.
        """
        self.__character_level = character_level
        user_data = read_json("settings/user_settings.json")
        user_data["character_level"][self.get_name()] = character_level
        write_json("settings/user_settings.json", user_data)

    def set_unlocked_abilities(self, unlocked_abilities: list[Ability]) -> None:
        """
        Sets the unlocked abilities and updates the user settings file.

        :param unlocked_abilities: List of new unlocked abilities.
        """
        self.__unlocked_abilities = list(set(unlocked_abilities))
        user_data = read_json("settings/user_settings.json")
        user_data["character_abilities"][self.get_name()] = list(
            set([ability.get_name() for ability in unlocked_abilities])
        )
        write_json("settings/user_settings.json", user_data)

    # Methods inherited from BaseCharacter
    def get_name(self) -> str:
        """
        Gets the name of the player character.

        :return: Player name.
        """
        return super().get_name()

    def get_sprite_location(self) -> str:
        """
        Gets the sprite location of the player character.

        :return: Sprite location.
        """
        return super().get_sprite_location()

    def get_stats(self) -> dict[str, int]:
        """
        Gets the stats of the player character.

        :return: Dictionary of stats.
        """
        return super().get_stats()

    def get_abilities(self) -> list[Ability]:
        """
        Gets the abilities of the player character.

        :return: List of abilities.
        """
        return super().get_abilities()

    def set_name(self, name: str) -> None:
        """
        Sets the name of the player character.

        :param name: Player name.
        """
        super().set_name(name)

    def set_sprite_location(self, sprite_location: str) -> None:
        """
        Sets the sprite location of the player character.

        :param sprite_location: Sprite location.
        """
        super().set_sprite_location(sprite_location)

    def set_stats(self, stats: dict[str, int]) -> None:
        """
        Sets the stats for the player character.

        :param stats: Dictionary of stats.
        """
        super().set_stats(stats)

    def set_abilities(self, abilities: list[Ability]) -> None:
        """
        Sets the abilities for the player character.

        :param abilities: List of abilities.
        """
        super().set_abilities(abilities)