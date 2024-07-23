from characters.players.base_player import BasePlayer
from ability import PLAYER_ABILITY_LIST, Ability
import copy
import json_utility


class Mage(BasePlayer):
    __statistics: dict[str, int] = {
        "health_points": 850,
        "physical_defense": 70,
        "magical_defense": 160,
        "spell_power": 140,
        "physical_power": 20,
        "mana_regeneration": 15,
        "mana_points": 300,
        "magical_damage": 70,
    }

    __unlocked_abilities_string: list[str] = []
    __unlocked_abilities: list[Ability] = []

    __abilities: list[Ability] = [
        PLAYER_ABILITY_LIST["Fireball"],
        PLAYER_ABILITY_LIST["Arcane Shield"],
        PLAYER_ABILITY_LIST["Mana Surge"],
    ]

    def __init__(
        self,
        sprite_location: str,
    ) -> None:
        self.__unlocked_abilities_string = json_utility.read_json(
            "settings/user_settings.json"
        )["character_abilities"]["Mage"]
        for unlocked_ability_string in self.__unlocked_abilities_string:
            self.__unlocked_abilities.append(
                PLAYER_ABILITY_LIST[unlocked_ability_string]
            )
        character_level_user_setting = json_utility.read_json(
            "settings/user_settings.json"
        )["character_level"]["Mage"]
        super().__init__(
            "Mage",
            copy.deepcopy(self.__statistics),
            sprite_location,
            self.__abilities,
            self.__unlocked_abilities,
        )
        for _ in range(1, character_level_user_setting):
            self.upgrade()

    def upgrade(self) -> None:
        new_statistic: dict[str, int] = self.get_statistics()
        new_unlocked_abilities: list[Ability] = self.get_unlocked_abilities()
        if self.get_character_level() == 1:
            self.set_character_level(2)
            new_statistic["spell_power"] += 15
            new_statistic["mana_points"] += 50
        elif self.get_character_level() == 2:
            self.set_character_level(3)
            index = next(
                (
                    i
                    for i, ability in enumerate(new_unlocked_abilities)
                    if ability.get_name() == "Fireball"
                ),
                None,
            )
            if index is not None:
                new_unlocked_abilities[index].upgrade()
        elif self.get_character_level() == 3:
            self.set_character_level(4)
            new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Arcane Shield"])
        self.set_statistics(new_statistic)
        self.set_unlocked_abilities(new_unlocked_abilities)

    def unlock_ability(self) -> None:
        new_unlocked_abilities: list[Ability] = self.get_unlocked_abilities()
        new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Mana Surge"])
        self.set_unlocked_abilities(new_unlocked_abilities)

    def copy(self) -> "Mage":
        return Mage(
            self.get_sprite_location(),
        )

    def get_name(self) -> str:
        return super().get_name()

    def get_sprite_location(self) -> str:
        return super().get_sprite_location()

    def get_statistics(self) -> dict:
        return super().get_statistics()

    def get_character_level(self) -> int:
        return super().get_character_level()

    def get_abilities(self) -> list[Ability]:
        return super().get_abilities()

    def get_unlocked_abilities(self) -> list[Ability]:
        return super().get_unlocked_abilities()

    def set_name(self, name: str) -> None:
        super().set_name(name)

    def set_sprite_location(self, sprite_location: str) -> None:
        super().set_sprite_location(sprite_location)

    def set_statistics(self, statistics: dict) -> None:
        super().set_statistics(statistics)

    def set_character_level(self, character_level: int) -> None:
        super().set_character_level(character_level)

    def set_abilities(self, abilities: list[Ability]) -> None:
        super().set_abilities(abilities)

    def set_unlocked_abilities(self, unlocked_abilities: list[Ability]) -> None:
        super().set_unlocked_abilities(unlocked_abilities)
        self.__unlocked_abilities_string = list(
            set([ability.get_name() for ability in unlocked_abilities])
        )
