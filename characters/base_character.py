from ability import Ability
import copy


class BaseCharacter:
    """
    BaseCharacter is a base class representing a character in the game.
    It provides basic attributes and methods for character management.

    Attributes:
        __name (str): The name of the character.
        __stats (dict[str, int]): Dictionary holding the character's stats.
        __abilities (list[Ability]): List of abilities the character possesses.
        __sprite_location (str): File path to the character's sprite image.
    """

    __name: str = ""
    __stats: dict[str, int] = {}
    __abilities: list[Ability] = []
    __sprite_location: str = ""

    def __init__(
        self,
        name: str,
        stats: dict[str, int],
        sprite_location: str,
        abilities: list[Ability],
    ) -> None:
        """
        Initializes the BaseCharacter class with the provided attributes.

        :param name: The name of the character.
        :param stats: Dictionary containing the character's stats.
        :param sprite_location: The file path to the character's sprite image.
        :param abilities: List of abilities the character possesses.
        """
        self.set_name(name)
        self.set_stats(stats)
        self.set_sprite_location(sprite_location)
        self.set_abilities(abilities)

    def copy(self) -> "BaseCharacter":
        """
        Creates a copy of the current character instance.

        :return: A new instance of BaseCharacter with the same attributes.
        """
        return BaseCharacter(
            self.get_name(),
            copy.deepcopy(self.get_stats()),
            self.get_sprite_location(),
            self.get_abilities(),
        )

    def get_name(self) -> str:
        """
        Gets the name of the character.

        :return: Character name.
        """
        return self.__name

    def get_sprite_location(self) -> str:
        """
        Gets the sprite location of the character.

        :return: Sprite location.
        """
        return self.__sprite_location

    def get_stats(self) -> dict[str, int]:
        """
        Gets the stats of the character.

        :return: Dictionary of stats.
        """
        return self.__stats

    def get_abilities(self) -> list[Ability]:
        """
        Gets the abilities of the character.

        :return: List of abilities.
        """
        return self.__abilities

    def set_name(self, name: str) -> None:
        """
        Sets the name of the character.

        :param name: Character name.
        """
        self.__name = name

    def set_sprite_location(self, sprite_location: str) -> None:
        """
        Sets the sprite location of the character.

        :param sprite_location: Sprite location.
        """
        self.__sprite_location = sprite_location

    def set_stats(self, stats: dict[str, int]) -> None:
        """
        Sets the stats for the character.

        :param stats: Dictionary of stats.
        """
        self.__stats = stats

    def set_abilities(self, abilities: list[Ability]) -> None:
        """
        Sets the abilities for the character.

        :param abilities: List of abilities.
        """
        self.__abilities = abilities
