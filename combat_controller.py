from characters.base_character import BaseCharacter
from ability import Ability
from typing import Tuple
import random
from pygame_gui.elements import UIImage
import copy


class CombatController:
    __player_statistic: dict[str, int] = {}
    __player_statistic_cap: dict[str, int] = {}
    __debuff_dict: dict[str, Tuple[int, int]] = {}
    __buff_dict: dict[str, Tuple[int, int]] = {}
    __ability_histories: list[Ability] = []
    __cooldown_abilities: dict[str, int] = {}
    __player_sprite: UIImage = None

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
        return "stun" in self.__debuff_dict.keys() and self.__debuff_dict["stun"] > 0

    def attack(
        self, hit_height: float, ability: Ability = None
    ) -> Tuple[int, int, dict[str, Tuple[int, int]]]:
        debuff_dict: dict[str, Tuple[int, int]] = {}
        if "stun" in self.__debuff_dict.keys() and self.__debuff_dict["stun"] > 0:
            for buff_name, (
                buff_value,
                buff_duration,
            ) in self.__buff_dict.copy().items():
                if buff_duration > 1:
                    self.__buff_dict[buff_name][1] -= 1
                else:
                    del self.__buff_dict[buff_name]
            return (0, 0, self.__debuff_dict)

        # Decrease cooldown of abilities
        for (
            cooldown_ability_name,
            cooldown_count,
        ) in self.__cooldown_abilities.copy().items():
            if cooldown_count > 1:
                self.__cooldown_abilities[cooldown_ability_name] -= 1
            else:
                del self.__cooldown_abilities[cooldown_ability_name]

        critical_rate = hit_height / self.__player_sprite.rect.height * 100
        if ability is not None:
            self.__ability_histories.append(ability.copy())
            self.__cooldown_abilities[ability.get_name()] = ability.get_statistics()[
                "cooldown"
            ]

            for cost in ability.get_cost():
                self.__player_statistic[cost[0]] -= cost[1]

            for modifer, value in ability.get_statistics().items():
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

        for player_ability in self.__ability_histories:
            if player_ability.get_duration() > 0:
                player_ability.set_duration(player_ability.get_duration() - 1)
            else:
                # Remove buff effect if duration of the ability has passed
                for modifer, value in player_ability.get_statistics().items():
                    if modifer in self.__POSITIVE_PLAYER_STATISTIC_MODIFERS:
                        self.__player_statistic[modifer] -= value
                self.__ability_histories.remove(player_ability)

        print("Critical Rate: ", critical_rate)
        critical_dmg_addition = random.randint(0, int(critical_rate))
        physical_dmg = magical_dmg = 0
        if (
            "physical_damage" in self.__player_statistic.keys()
            and "physical_power" in self.__player_statistic.keys()
        ):
            physical_dmg = int(
                self.__player_statistic["physical_damage"]
                * self.__player_statistic["physical_power"]
                / 50
                + critical_dmg_addition
            )
        if (
            "magical_damage" in self.__player_statistic.keys()
            and "spell_power" in self.__player_statistic.keys()
        ):
            magical_dmg = int(
                self.__player_statistic["magical_damage"]
                * self.__player_statistic["spell_power"]
                / 50
                + critical_dmg_addition
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
            self.__debuff_dict[debuff_name] = (debuff_value, debuff_duration)

        # Decrease debuff modifer duration
        for debuff_name, (
            debuff_value,
            debuff_duration,
        ) in self.__debuff_dict.copy().items():
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
                del self.__debuff_dict[debuff_name]

        physical_dmg *= 1 - self.__player_statistic["physical_defense"] / 400
        magical_damage *= 1 - self.__player_statistic["magical_defense"] / 400
        total_dmg = physical_dmg + magical_damage
        if "absorption" in self.__player_statistic.keys():
            total_dmg -= debuff_dict["absorption"][0]
        self.__player_statistic["health_points"] -= int(total_dmg)
        self.__player_statistic["health_points"] = max(0, self.__player_statistic["health_points"])

    def regenerate(self) -> None:
        if (
            "health_regeneration" in self.__player_statistic.keys()
            and self.__player_statistic["health_points"]
            + self.__player_statistic["health_regeneration"]
            <= self.__player_statistic_cap["health_points"]
        ):
            self.__player_statistic["health_points"] += self.__player_statistic[
                "health_regeneration"
            ]
        if (
            "mana_regeneration" in self.__player_statistic.keys()
            and self.__player_statistic["mana_points"]
            + self.__player_statistic["mana_regeneration"]
            <= self.__player_statistic_cap["mana_points"]
        ):
            self.__player_statistic["mana_points"] += self.__player_statistic[
                "mana_regeneration"
            ]
