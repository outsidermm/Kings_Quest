from typing import Tuple


class Ability:
    __name: str = None
    __description: str = None
    __ability_statistics: dict = None
    __cost: list[Tuple[str, float]] = None
    __duration: int = 0
    __active: bool = False
    __upgrades: list[Tuple[str, ...]] = None
    __cooldown: int = 0
    __icon_URL: str = None

    def __init__(
        self,
        name: str,
        description: str,
        ability_statistics: dict,
        cost: list[Tuple[str, float]],
        duration: int,
        icon_URL: str,
        upgrades: list[Tuple[str, ...]] = None,
    ) -> None:
        self.__name = name
        self.__description = description
        self.__cost = cost
        self.__ability_statistics = ability_statistics
        self.__upgrades = upgrades
        self.__icon_URL = icon_URL
        self.__duration = duration

    def copy(self) -> "Ability":
        return Ability(
            self.__name,
            self.__description,
            self.__ability_statistics,
            self.__cost,
            self.__duration,
            self.__icon_URL,
            self.__upgrades,
        )

    def upgrade(self) -> None:
        for upgrade in self.__upgrades:
            if upgrade[0] in self.__ability_statistics.keys():
                self.__ability_statistics[upgrade[0]] += upgrade[1]
            else:
                self.__ability_statistics[upgrade[0]] = upgrade[1]

    def get_name(self) -> str:
        return self.__name

    def get_description(self) -> str:
        return self.__description

    def get_modifer(self) -> list[Tuple[float, str]]:
        return self.__modifer

    def get_cooldown(self) -> int:
        return self.__cooldown

    def get_cost(self) -> list[Tuple[str, float]]:
        return self.__cost

    def get_duration(self) -> int:
        return self.__duration

    def get_active(self) -> bool:
        return self.__active

    def get_icon_URL(self) -> str:
        return self.__icon_URL

    def set_active(self, active: bool) -> None:
        self.__active = active

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_description(self, description: str) -> None:
        self.__description = description

    def set_modifer(self, modifer: list[Tuple[float, str]]) -> None:
        self.__modifer = modifer

    def set_cooldown(self, cooldown: int) -> None:
        self.__cooldown = cooldown

    def set_cost(self, cost: list[Tuple[str, float]]) -> None:
        self.__cost = cost

    def set_duration(self, duration: int) -> None:
        self.__duration = duration

    def set_active(self, active: bool) -> None:
        self.__active = active

    def get_statistics(self) -> dict:
        return self.__ability_statistics

    def set_statistics(self, statistics: dict) -> None:
        self.__ability_statistics = statistics


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
        {"stun": True, "physical_damage": 20, "cooldown": 2},
        [("mana_points", 20)],
        1,  # Duration
        "assets/abilities/Reckless Charge.webp",
        [("duration", 2)],
    ),
}

ENEMY_ABILITY_LIST: dict[str, Ability] = {
    "Rending Claws": Ability(
        "Rending Claws",
        "Deals 200 physical damage and causes bleeding (30 damage per turn for 3 turns). Cooldown: 3 turns",
        {"physical_damage": 200, "cooldown": 3, "bleed": 30},
        [],
        3,  # Duration
        "assets/abilities/Rending Claws.webp",
    ),
    "Savage Roar": Ability(
        "Savage Roar",
        "Reduces the attack damage of all enemies by 20 percent for 2 turns. Cooldown: 4 turns",
        {"cooldown": 4, "physical_damage_reduction": -20},
        [],
        2,  # Duration
        "assets/abilities/Savage Roar.webp",
    ),
    "Dark Bolt": Ability(
        "Dark Bolt",
        "Deals 250 magical damage and reduces target's physical defense by 50 for 2 turns. Cooldown: 3 turns",
        {"magical_damage": 250, "cooldown": 3, "physical_defense": -50},
        [],
        2,  # Duration
        "assets/abilities/Dark Bolt.webp",
    ),
    "Life Drain": Ability(
        "Life Drain",
        "Deals 150 magical damage and heals caster for 100 HP. Cooldown: 3 turns",
        {"magical_damage": 150, "cooldown": 3, "health_regeneration": 100},
        [],
        1,  # Duration
        "assets/abilities/Life Drain.webp",
    ),
    "Flame Breath": Ability(
        "Flame Breath",
        "Deals 300 magical damage to all enemies. Cooldown: 4 turns",
        {"magical_damage": 300, "cooldown": 4},
        [],
        1,  # Duration
        "assets/abilities/Flame Breath.webp",
    ),
    "Tail Swipe": Ability(
        "Tail Swipe",
        "Deals 250 physical damage to a single target and stuns them for 1 turn. Cooldown: 3 turns",
        {"physical_damage": 250, "cooldown": 3, "stun": True},
        [],
        1,  # Duration
        "assets/abilities/Tail Swipe.webp",
    ),
}
