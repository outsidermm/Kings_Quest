from characters.base_character import BaseCharacter
from ability import Ability
from typing import Tuple
import random
from utilities.math_utility import min_max_bound
from pygame_gui.elements import UIImage


class CombatController:
    __player_statistic: dict[str, int] = {}
    __player_statistic_cap: dict[str, int] = {}
    __debuff_dict: dict[str, Tuple[int, int]] = {}
    __buff_dict: dict[str, Tuple[int, int]] = {}
    __ability_histories: list[Ability] = []
    __cooldown_abilities: dict[str, int] = {}
    __player_sprite: UIImage = None
    __is_stunned: bool = False

    __DEBUFF_STATISTIC_MAPPER = {
        "physical_defense_reduction": "physical_defense",
        "physical_damage_reduction": "physical_damage",
        "bleed": "health_points",
    }

    __POSITIVE_PLAYER_STATISTIC_MODIFERS = [
        "health_regeneration",
        "mana_regeneration",
        "absorption",
        "physical_damage",
        "magical_damage",
        "physical_defense",
        "magical_defense",
        "mana_points",
        "physical_power",
        "spell_power",
    ]

    __NEGATIVE_PLAYER_STATISTIC_MODIFERS = [
        "stun",
        "physical_defense_reduction",
        "physical_damage_reduction",
        "bleed",
    ]

    def __init__(self, player: BaseCharacter, player_sprite: UIImage) -> None:
        self.__player_statistic = self.__player_statistic_cap = player.get_statistics()
        self.__player_sprite = player_sprite

    def is_ability_on_cooldown(self, ability: Ability) -> bool:
        return ability.get_name() in self.__cooldown_abilities.keys()

    def is_stunned(self) -> bool:
        return self.__is_stunned

    def stunned_round(self) -> None:
        # Collect abilities to remove in a separate list
        abilities_to_remove = []

        for player_ability in self.__ability_histories:
            if player_ability.get_duration() > 0:
                player_ability.set_duration(player_ability.get_duration() - 1)
            else:
                # Remove buff effect if duration of the ability has passed
                for modifier, value in player_ability.get_stats().items():
                    if (
                        modifier in self.__POSITIVE_PLAYER_STATISTIC_MODIFERS
                        and modifier in self.__player_statistic.keys()
                    ):
                        self.__player_statistic[modifier] -= value
                        self.__player_statistic[modifier] = max(
                            0, self.__player_statistic[modifier]
                        )
                abilities_to_remove.append(player_ability)

        # Remove abilities from the history after the iteration
        for ability_to_remove in abilities_to_remove:
            self.__ability_histories.remove(ability_to_remove)
        self.__is_stunned = False

    def attack(
        self, hit_height: float, ability: Ability = None
    ) -> Tuple[int, int, dict[str, Tuple[int, int]]]:
        debuff_dict: dict[str, Tuple[int, int]] = {}

        # Collect abilities to remove in a separate list
        cooldown_abilities_to_remove = []

        # Decrease cooldown of abilities
        for cooldown_ability_name, cooldown_count in self.__cooldown_abilities.items():
            if cooldown_count > 1:
                self.__cooldown_abilities[cooldown_ability_name] -= 1
            else:
                cooldown_abilities_to_remove.append(cooldown_ability_name)

        # Remove abilities from the cooldown dictionary after the iteration
        for cooldown_ability_name in cooldown_abilities_to_remove:
            del self.__cooldown_abilities[cooldown_ability_name]

        critical_rate = hit_height / self.__player_sprite.rect.height * 100
        if ability is not None:
            self.__ability_histories.append(ability.copy())
            self.__cooldown_abilities[ability.get_name()] = ability.get_stats()[
                "cooldown"
            ]

            for cost in ability.get_cost():
                self.__player_statistic[cost[0]] -= cost[1]

            for modifer, value in ability.get_stats().items():
                if modifer == "critical":
                    critical_rate += value
                elif modifer in self.__NEGATIVE_PLAYER_STATISTIC_MODIFERS:
                    debuff_dict[modifer] = (value, ability.get_duration())
                elif modifer in self.__POSITIVE_PLAYER_STATISTIC_MODIFERS:
                    # The new ability will modifer the player statistic
                    if modifer in self.__player_statistic.keys():
                        self.__player_statistic[modifer] += value
                    else:
                        self.__player_statistic[modifer] = value

        # Collect abilities to remove in a separate list
        abilities_to_remove = []

        for player_ability in self.__ability_histories:
            if player_ability.get_duration() > 0:
                player_ability.set_duration(player_ability.get_duration() - 1)
            else:
                # Remove buff effect if duration of the ability has passed
                for modifier, value in player_ability.get_stats().items():
                    if (
                        modifier in self.__POSITIVE_PLAYER_STATISTIC_MODIFERS
                        and modifier in self.__player_statistic.keys()
                    ):
                        self.__player_statistic[modifier] -= value
                        self.__player_statistic[modifier] = max(
                            0, self.__player_statistic[modifier]
                        )
                abilities_to_remove.append(player_ability)

        # Remove abilities from the history after the iteration
        for ability_to_remove in abilities_to_remove:
            self.__ability_histories.remove(ability_to_remove)

        critical_dmg_addition = random.randint(0, int(critical_rate))
        physical_dmg = magical_dmg = 0
        if (
            "physical_damage" in self.__player_statistic.keys()
            and "physical_power" in self.__player_statistic.keys()
        ):
            physical_dmg = max(
                0,
                int(
                    self.__player_statistic["physical_damage"]
                    * self.__player_statistic["physical_power"]
                    / 50
                    + critical_dmg_addition
                ),
            )
        if (
            "magical_damage" in self.__player_statistic.keys()
            and "spell_power" in self.__player_statistic.keys()
        ):
            magical_dmg = max(
                0,
                int(
                    self.__player_statistic["magical_damage"]
                    * self.__player_statistic["spell_power"]
                    / 50
                    + critical_dmg_addition
                ),
            )
        return (physical_dmg, magical_dmg, debuff_dict)

    def face_damage(
        self,
        physical_dmg: int,
        magical_damage: int,
        debuff_dict: dict[str, Tuple[int, int]],
    ) -> None:

        # Add debuff to the player's original debuff statistic
        for debuff_name, (debuff_value, debuff_duration) in debuff_dict.items():
            if debuff_name == "stun":
                self.__is_stunned = True
            else:
                self.__debuff_dict[debuff_name] = (debuff_value, debuff_duration)

        # Collect debuffs to remove in a separate list
        debuffs_to_remove = []

        # Decrease debuff modifier duration
        for debuff_name, (debuff_value, debuff_duration) in self.__debuff_dict.items():
            if debuff_duration > 1:
                if (
                    debuff_name in self.__DEBUFF_STATISTIC_MAPPER.keys()
                    and self.__DEBUFF_STATISTIC_MAPPER[debuff_name]
                    in self.__player_statistic.keys()
                ):
                    self.__player_statistic[
                        self.__DEBUFF_STATISTIC_MAPPER[debuff_name]
                    ] -= int(debuff_value)
                    self.__player_statistic[
                        self.__DEBUFF_STATISTIC_MAPPER[debuff_name]
                    ] = max(
                        0,
                        self.__player_statistic[
                            self.__DEBUFF_STATISTIC_MAPPER[debuff_name]
                        ],
                    )
                self.__debuff_dict[debuff_name] = (
                    debuff_value,
                    debuff_duration - 1,
                )
            else:
                # Remove debuff effect if duration of the debuff has passed
                if (
                    debuff_name
                    in [
                        "physical_defense_reduction",
                        "physical_damage_reduction",
                    ]
                    and self.__DEBUFF_STATISTIC_MAPPER[debuff_name]
                    in self.__player_statistic.keys()
                ):
                    self.__player_statistic[
                        self.__DEBUFF_STATISTIC_MAPPER[debuff_name]
                    ] += int(debuff_value)
                debuffs_to_remove.append(debuff_name)

        # Remove debuffs from the dictionary after the iteration
        for debuff_name in debuffs_to_remove:
            del self.__debuff_dict[debuff_name]

        physical_dmg *= 1 - self.__player_statistic["physical_defense"] / 400
        magical_damage *= 1 - self.__player_statistic["magical_defense"] / 400
        physical_dmg = max(0, physical_dmg)
        magical_damage = max(0, magical_damage)
        total_dmg = physical_dmg + magical_damage
        if "absorption" in self.__player_statistic.keys():
            total_dmg = max(0, total_dmg - self.__player_statistic["absorption"])
        self.__player_statistic["health_points"] = max(
            0, self.__player_statistic["health_points"] - int(total_dmg)
        )

    def regenerate(self) -> None:
        if "health_regeneration" in self.__player_statistic.keys():
            self.__player_statistic["health_points"] = min_max_bound(
                0,
                self.__player_statistic_cap["health_points"],
                self.__player_statistic["health_points"]
                + self.__player_statistic["health_regeneration"],
            )
        if "mana_regeneration" in self.__player_statistic.keys():
            self.__player_statistic["mana_points"] = min_max_bound(
                0,
                self.__player_statistic_cap["mana_points"],
                self.__player_statistic["mana_points"]
                + self.__player_statistic["mana_regeneration"],
            )

    def get_cooldown_abilities(self) -> dict[str, int]:
        return self.__cooldown_abilities

    def get_player_statistic(self) -> dict[str, int]:
        return self.__player_statistic
