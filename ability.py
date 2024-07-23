from typing import Tuple, Dict, List


class Ability:
    """
    Ability class representing a character's ability with various attributes and methods
    to manage and upgrade the ability.
    """

    __name: str = None
    __description: str = None
    __ability_statistics: Dict[str, float] = None
    __cost: List[Tuple[str, float]] = None
    __duration: int = 0
    __upgrades: List[Tuple[str, float]] = None
    __icon_URL: str = None

    def __init__(
        self,
        name: str,
        description: str,
        ability_statistics: Dict[str, float],
        cost: List[Tuple[str, float]],
        duration: int,
        icon_URL: str,
        upgrades: List[Tuple[str, float]] = None,
    ) -> None:
        """
        Initializes the Ability class.

        :param name: Name of the ability.
        :param description: Description of the ability.
        :param ability_statistics: Statistics of the ability.
        :param cost: Cost to use the ability.
        :param duration: Duration of the ability's effect.
        :param icon_URL: URL to the ability's icon.
        :param upgrades: List of possible upgrades for the ability.
        """
        self.set_name(name)
        self.set_description(description)
        self.set_cost(cost)
        self.set_statistics(ability_statistics)
        self.set_upgrades(upgrades if upgrades is not None else [])
        self.set_icon_URL(icon_URL)
        self.set_duration(duration)

    def copy(self) -> "Ability":
        """
        Creates a copy of the ability instance.

        :return: A new instance of Ability with the same attributes.
        """
        return Ability(
            self.get_name(),
            self.get_description(),
            self.get_statistics(),
            self.get_cost(),
            self.get_duration(),
            self.get_icon_URL(),
            self.get_upgrades(),
        )

    def upgrade(self) -> None:
        """
        Upgrades the ability based on its upgrade list.
        """
        for upgrade in self.get_upgrades():
            if upgrade[0] in self.get_statistics().keys():
                self.get_statistics()[upgrade[0]] += upgrade[1]
            else:
                self.get_statistics()[upgrade[0]] = upgrade[1]

    def get_name(self) -> str:
        """
        Gets the name of the ability.

        :return: The name of the ability.
        """
        return self.__name

    def set_name(self, name: str) -> None:
        """
        Sets the name of the ability.

        :param name: The new name of the ability.
        """
        self.__name = name

    def get_description(self) -> str:
        """
        Gets the description of the ability.

        :return: The description of the ability.
        """
        return self.__description

    def set_description(self, description: str) -> None:
        """
        Sets the description of the ability.

        :param description: The new description of the ability.
        """
        self.__description = description

    def get_statistics(self) -> Dict[str, float]:
        """
        Gets the statistics of the ability.

        :return: The statistics of the ability.
        """
        return self.__ability_statistics

    def set_statistics(self, statistics: Dict[str, float]) -> None:
        """
        Sets the statistics of the ability.

        :param statistics: The new statistics of the ability.
        """
        self.__ability_statistics = statistics

    def get_cost(self) -> List[Tuple[str, float]]:
        """
        Gets the cost of the ability.

        :return: The cost of the ability.
        """
        return self.__cost

    def set_cost(self, cost: List[Tuple[str, float]]) -> None:
        """
        Sets the cost of the ability.

        :param cost: The new cost of the ability.
        """
        self.__cost = cost

    def get_duration(self) -> int:
        """
        Gets the duration of the ability.

        :return: The duration of the ability.
        """
        return self.__duration

    def set_duration(self, duration: int) -> None:
        """
        Sets the duration of the ability.

        :param duration: The new duration of the ability.
        """
        self.__duration = duration

    def get_upgrades(self) -> List[Tuple[str, float]]:
        """
        Gets the upgrades of the ability.

        :return: The upgrades of the ability.
        """
        return self.__upgrades

    def set_upgrades(self, upgrades: List[Tuple[str, float]]) -> None:
        """
        Sets the upgrades of the ability.

        :param upgrades: The new upgrades of the ability.
        """
        self.__upgrades = upgrades

    def get_icon_URL(self) -> str:
        """
        Gets the icon URL of the ability.

        :return: The icon URL of the ability.
        """
        return self.__icon_URL

    def set_icon_URL(self, icon_URL: str) -> None:
        """
        Sets the icon URL of the ability.

        :param icon_URL: The new icon URL of the ability.
        """
        self.__icon_URL = icon_URL
        
        
PLAYER_ABILITY_LIST: dict[str, Ability] = {
    "Power Slash": Ability(
        "Power Slash",
        "Deals 45 physical damage to the enemy. Duration: 1 turn, Cooldown: 2 turns",
        {"physical_damage": 45, "cooldown": 2},
        [("mana_points", 20)],
        1,  # Duration
        "assets/abilities/Power Slash.webp",
        [("physical_damage", 10)],
    ),
    "Shield War": Ability(
        "Shield War",
        "Increases physical defense by 200 for 3 turns. Cooldown: 3 turns",
        {"cooldown": 3, "physical_defense": 200},
        [("mana_points", 25)],
        3,  # Duration
        "assets/abilities/Shield War.webp",
    ),
    "War Cry": Ability(
        "War Cry",
        "Increases physical damage by 30 for 2 turns and physical defense by 100 for 2 turns. Cooldown: 4 turns",
        {"physical_damage": 30, "cooldown": 4, "physical_defense": 100},
        [("mana_points", 30)],
        2,  # Duration
        "assets/abilities/War Cry.webp",
    ),
    "Fireball": Ability(
        "Fireball",
        "Deals 120 magical damage to the enemy. Duration: 1 turn, Cooldown: 3 turns",
        {"magical_damage": 120, "cooldown": 3},
        [("mana_points", 20)],
        1,  # Duration
        "assets/abilities/Fireball.webp",
        [("magical_damage", 30)],
    ),
    "Arcane Shield": Ability(
        "Arcane Shield",
        "Blocks 100 incoming damage for 1 turn. Cooldown: 2 turns",
        {"cooldown": 2, "absorption": 100},
        [("mana_points", 25)],
        1,  # Duration
        "assets/abilities/Arcane Shield.webp",
    ),
    "Mana Surge": Ability(
        "Mana Surge",
        "Increases mana by 50. Duration: 1 turn, Cooldown: 5 turns",
        {"mana_points": 50, "cooldown": 5},
        [("mana_points", 15)],
        1,  # Duration
        "assets/abilities/Mana Surge.webp",
    ),
    "Arrow Barrage": Ability(
        "Arrow Barrage",
        "Shoots multiple arrows that cause 50 bleed damage for 2 turns. Cooldown: 4 turns",
        {"bleed": 50, "cooldown": 4},
        [("mana_points", 25)],
        2,  # Duration
        "assets/abilities/Arrow Barrage.webp",
        [("physical_damage", 10)],
    ),
    "Natural Grace": Ability(
        "Natural Grace",
        "Increases health regeneration by 50 HP for 3 turns. Cooldown: 5 turns",
        {"health_regeneration": 50, "cooldown": 5},
        [("mana_points", 20)],
        3,  # Duration
        "assets/abilities/Natural Grace.webp",
    ),
    "Fatal Shadow": Ability(
        "Fatal Shadow",
        "Increases critical hit rate by 20 percent for 1 turn. Cooldown: 3 turns",
        {"critical": 20, "cooldown": 3},
        [("mana_points", 30)],
        1,  # Duration
        "assets/abilities/Fatal Shadow.webp",
    ),
    "Berserk": Ability(
        "Berserk",
        "Increases physical power by 50 percent for 3 turns, but reduces physical defense by 75. Cooldown: 3 turns",
        {"physical_power": 55, "cooldown": 3, "physical_defense_reduction": 75},
        [("mana_points", 25)],
        3,  # Duration
        "assets/abilities/Berserk.webp",
    ),
    "Bloodlust": Ability(
        "Bloodlust",
        "Heals for 25 HP for the next 2 turns. Cooldown: 4 turns",
        {"health_regeneration": 25, "cooldown": 4},
        [("mana_points", 30)],
        2,  # Duration
        "assets/abilities/Bloodlust.webp",
    ),
    "Reckless Charge": Ability(
        "Reckless Charge",
        "Charges at the enemy, dealing 20 physical damage and stunning them for 1 turn. Cooldown: 2 turns",
        {"stun": 1, "physical_damage": 20, "cooldown": 2},
        [("mana_points", 20)],
        1,  # Duration
        "assets/abilities/Reckless Charge.webp",
        [("duration", 2)],
    ),
}

ENEMY_ABILITY_LIST: dict[str, Ability] = {
    "Savage Roar": Ability(
        "Savage Roar",
        "Reduces the attack damage of all enemies by 15 percent for 2 turns. Cooldown: 4 turns",
        {"cooldown": 4, "physical_damage_reduction": -15},
        [],
        2,  # Duration
        "assets/abilities/Savage Roar.webp",
    ),
    "Flame Breath": Ability(
        "Flame Breath",
        "Deals 50 more magical damage to all enemies. Cooldown: 4 turns",
        {"magical_damage": 50, "cooldown": 4},
        [],
        1,  # Duration
        "assets/abilities/Flame Breath.webp",
    ),
    "Tail Swipe": Ability(
        "Tail Swipe",
        "Deals 70 more physical damage and stuns them for 1 turn. Cooldown: 3 turns",
        {"physical_damage": 70, "cooldown": 3, "stun": 1},
        [],
        1,  # Duration
        "assets/abilities/Tail Swipe.webp",
    ),
}
