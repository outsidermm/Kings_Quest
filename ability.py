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
        icon_URL: str,
        upgrades: list[Tuple[str, ...]] = None,
    ) -> None:
        self.__name = name
        self.__description = description
        self.__cost = cost
        self.__ability_statistics = ability_statistics
        self.__upgrades = upgrades
        self.__icon_URL = icon_URL

    def use(self) -> None:
        if self.__cooldown > 0:
            self.__cooldown -= 1
            return

        if not self.__active:
            self.__duration = self.__ability_statistics["duration"]
            self.__cooldown = self.__ability_statistics["cooldown"]

        self.__duration -= 1
        self.__active = True if self.__duration > 0 else False

        # TODO Find way to use the ability -> return the modifers

    def upgrade(self) -> None:
        for upgrade in self.__upgrades:
            self.__ability_statistics[upgrade[0]] += upgrade[1]

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


PLAYER_ABILITY_LIST: dict[Ability] = {
    "Power Slash": Ability(
        "Power Slash",
        "Slash the enemy with a powerful strike",
        {"damage": 45, "duration": 1, "cooldown": 2},
        [("MP", 20)],
        "",
        [("damage", 55)],
    ),
    "Shield War": Ability(
        "Shield War",
        "Block incoming damage",
        {"duration": 3, "cooldown": 3, "resistance": 200},
        [("MP", 25)],
        "",
    ),
    "War Cry": Ability(
        "War Cry",
        "Increase attack damage",
        {"damage": 30, "duration": 2, "cooldown": 4, "resistance": 100},
        [("MP", 30)],
        "",
    ),
    "Fireball": Ability(
        "Fireball",
        "Cast a fireball",
        {"damage": 120, "duration": 1, "cooldown": 3},
        [("MP", 20)],
        "",
        [("damage", 150)],
    ),
    "Arcane Shield": Ability(
        "Arcane Shield",
        "Block incoming magic damage",
        {"duration": 1, "cooldown": 2, "absorption": 100},
        [("MP", 25)],
        "",
    ),
    "Mana Surge": Ability(
        "Mana Surge",
        "Increase mana",
        {"mana": 50, "duration": 1, "cooldown": 5},
        [("MP", 15)],
        "",
    ),
    "Arrow Barrage": Ability(
        "Arrow Barrage",
        "Shoot multiple arrows that bleeds 50 damage for 2 turns",
        {"bleed": 50, "duration": 2, "cooldown": 4},
        [("MP", 25)],
        "",
        [("damage", 60)],
    ),
    "Nature's Grace": Ability(
        "Nature's Grace",
        "Increase health regeneration",
        {"HP": 50, "duration": 3, "cooldown": 5},
        [("MP", 20)],
        "",
    ),
    "Fatal shadow": Ability(
        "Fatal shadow",
        "Increase critical hite rate by 20%",
        {"critical": 20, "duration": 1, "cooldown": 3},
        [("MP", 30)],
        "",
    ),
    "Berserk": Ability(
        "Berserk",
        "Increases strength by 50%",
        {"strength": 55, "duration": 3, "cooldown": 3},
        [("MP", 25), ("resistance", 75)],
        "",
    ),
    "Bloodlust": Ability(
        "Bloodlust",
        "Heals for 25 HP for the next 2 turns",
        {"regeneration": 25, "duration": 2, "cooldown": 4},
        [("MP", 30)],
        "",
    ),
    "Reckless Charge": Ability(
        "Reckless Charge",
        "Charge at the enemy",
        {"stun": True, "damage": 20, "duration": 1, "cooldown": 2},
        [("MP", 20)],
        "",
        [("duration", 3)],
    ),
}

ENEMY_ABILITY_LIST: dict[Ability] = {
    "Rending Claws": Ability(
        "Rending Claws",
        "Deals 200 physical damage and causes bleeding (30 damage per turn for 3 turns)",
        {"damage": 10, "duration": 3, "cooldown": 3, "bleed": 30},
        [],
        "",
    ),
    "Savage Roar": Ability(
        "Savage Roar",
        "Reduces the attack damage of all enemies by 20 percent for 2 turns",
        {"duration": 2, "cooldown": 4, "attack_damage_reduction": 20},
        [],
        "",
    ),
    "Dark Bolt": Ability(
        "Dark Bolt",
        "Deals 250 magic damage and reduces target's armor by 50 for 2 turns",
        {"damage": 250, "duration": 2, "cooldown": 3, "armor_reduction": 50},
        [],
        "",
    ),
    "Life Drain": Ability(
        "Life Drain",
        "Deals 150 magic damage and heals Morgath for 100 HP",
        {"damage": 150, "duration": 1, "cooldown": 3, "regeneration": 100},
        [],
        "",
    ),
    "Flame Breath": Ability(
        "Flame Breath",
        "Deals 300 damage to all enemies",
        {"damage": 300, "duration": 1, "cooldown": 4},
        [],
        "",
    ),
    "Tail Swipe": Ability(
        "Tail Swipe",
        "Deals 250 damage to a single target and stuns them for 1 turn",
        {"damage": 250, "duration": 1, "cooldown": 3, "stun": True},
        [],
        "",
    ),
}
