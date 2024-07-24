from characters.base_character import BaseCharacter
from ability import Ability
import copy


class BaseEnemy(BaseCharacter):
    """
    BaseEnemy is a class representing an enemy character in the game.
    It inherits from the BaseCharacter class and provides specific functionality for enemies.

    Methods:
        copy: Creates a deep copy of the enemy instance.
        get_name: Gets the name of the enemy.
        get_sprite_location: Gets the sprite location of the enemy.
        get_stats: Gets the stats of the enemy.
        get_abilities: Gets the abilities of the enemy.
        set_name: Sets the name of the enemy.
        set_sprite_location: Sets the sprite location of the enemy.
        set_stats: Sets the stats of the enemy.
        set_abilities: Sets the abilities of the enemy.
    """

    def __init__(
        self,
        name: str,
        stats: dict,
        sprite_location: str,
        abilities: list[Ability],
    ) -> None:
        """
        Initializes the BaseEnemy class with the provided attributes.

        :param name: The name of the enemy.
        :param stats: Dictionary containing the enemy's stats.
        :param sprite_location: The file path to the enemy's sprite image.
        :param abilities: List of abilities the enemy possesses.
        """
        super().__init__(name, stats, sprite_location, abilities)

    def copy(self) -> "BaseEnemy":
        """
        Creates a copy of the current enemy instance.

        :return: A new instance of BaseEnemy with the same attributes.
        """
        return BaseEnemy(
            self.get_name(),
            copy.deepcopy(self.get_stats()),
            self.get_sprite_location(),
            self.get_abilities(),
        )

    def get_name(self) -> str:
        """
        Gets the name of the enemy.

        :return: Enemy name.
        """
        return super().get_name()

    def get_sprite_location(self) -> str:
        """
        Gets the sprite location of the enemy.

        :return: Sprite location.
        """
        return super().get_sprite_location()

    def get_stats(self) -> dict:
        """
        Gets the stats of the enemy.

        :return: Dictionary of stats.
        """
        return super().get_stats()

    def get_abilities(self) -> list[Ability]:
        """
        Gets the abilities of the enemy.

        :return: List of abilities.
        """
        return super().get_abilities()

    def set_name(self, name: str) -> None:
        """
        Sets the name of the enemy.

        :param name: Enemy name.
        """
        super().set_name(name)

    def set_sprite_location(self, sprite_location: str) -> None:
        """
        Sets the sprite location of the enemy.

        :param sprite_location: Sprite location.
        """
        super().set_sprite_location(sprite_location)

    def set_stats(self, stats: dict[str, int]) -> None:
        """
        Sets the stats for the enemy.

        :param stats: Dictionary of stats.
        """
        super().set_stats(stats)

    def set_abilities(self, abilities: list[Ability]) -> None:
        """
        Sets the abilities for the enemy.

        :param abilities: List of abilities.
        """
        super().set_abilities(abilities)