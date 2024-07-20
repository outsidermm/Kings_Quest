from characters.base_character import BaseCharacter
from ability import Ability
from typing import Tuple
import random
from pygame_gui.elements import UIImage


class CombatController:
    __player_statistic: dict[str, int] = None
    __debuff_dict: dict[str, Tuple[int, int]] = {}
    __buff_dict: dict[str, Tuple[int, int]] = {}
    __ability_histories: list[Ability] = []
    __player_sprite: UIImage = None

    def __init__(self, player: BaseCharacter, player_sprite: UIImage) -> None:
        self.__player_statistic = player.get_statistics()
        self.__player_sprite = player_sprite

    def attack(
        self, hit_height: float, ability: Ability = None
    ) -> Tuple[int, int, dict[str, Tuple[int, int]]]:
        debuff_dict: dict[str, Tuple[int, int]] = {}
        if "stun" in self.__debuff_dict.keys() and self.__debuff_dict["stun"] > 0:
            for buff_name, (buff_value, buff_duration) in self.__buff_dict.items():
                if buff_duration > 0:
                    buff_duration -= 1
                else:
                    self.__buff_dict.pop(buff_name)

            return (0, self.__debuff_dict)

        critical_rate = hit_height / self.__player_sprite.rect.height * 100
        if ability is not None:
            self.__ability_histories.append(ability)

            for player_ability in self.__ability_histories:
                if player_ability.get_duration() > 0:
                    player_ability.set_duration(player_ability.get_duration() - 1)
                else:
                    # Remove buff effect if duration of the ability has passed
                    for modifer, value in player_ability.get_statistics().items():
                        if modifer in [
                            "health_regeneration",
                            "mana_regeneration",
                            "absorption",
                            "physical_damage",
                            "magical_damage",
                            "physical_defense",
                            "magical_defense",
                        ]:
                            self.__player_statistic[modifer] -= value
                    self.__ability_histories.remove(player_ability)

            for cost in ability.get_cost():
                self.__player_statistic[cost[0]] -= cost[1]

            for modifer, value in ability.get_statistics().items():
                if modifer == "critical":
                    critical_rate += value
                elif modifer in [
                    "stun",
                    "physical_defense_reduction",
                    "physical_damage_reduction",
                    "bleed",
                ]:
                    debuff_dict[modifer] = (value, ability.get_duration())
                elif modifer in [
                    "health_regeneration",
                    "mana_regeneration",
                    "absorption",
                    "physical_damage",
                    "magical_damage",
                    "physical_defense",
                    "magical_defense",
                ]:
                    # The new ability will modifer the player statistic
                    if modifer in self.__player_statistic.keys():
                        self.__player_statistic[modifer] += value
                    else:
                        self.__player_statistic[modifer] = value

        critical_dmg_addition = random.randint(0, int(critical_rate))
        physical_dmg = magical_dmg = 0
        if (
            "physical_damage" in self.__player_statistic.keys()
            and "physical_power" in self.__player_statistic.keys()
        ):
            print("1")
            physical_dmg = int(
                self.__player_statistic["physical_damage"]
                * self.__player_statistic["physical_power"]
                + critical_dmg_addition
            )
        if (
            "magical_damage" in self.__player_statistic.keys()
            and "spell_power" in self.__player_statistic.keys()
        ):
            magical_dmg = int(
                self.__player_statistic["magical_damage"]
                * self.__player_statistic["spell_power"]
                + critical_dmg_addition
            )
        return (physical_dmg, magical_dmg, debuff_dict)

    def face_damage(
        self,
        physical_dmg: int,
        magical_damage: int,
        debuff_dict: dict[str, Tuple[int, int]],
    ) -> None:
        DEBUFF_STATISTIC_MAPPER = {
            "physical_defense_reduction": "physical_defense",
            "physical_damage_reduction": "physical_damage",
            "bleed": "health_points",
        }
        # Add debuff to the player's original debuff statistic
        for debuff_name, (debuff_value, debuff_duration) in debuff_dict.items():
            self.__debuff_dict[debuff_name] = (debuff_value, debuff_duration)

        # Decrease debuff modifer duration
        for debuff_name, (debuff_value, debuff_duration) in self.__debuff_dict.items():
            if debuff_duration > 0:
                if debuff_name in DEBUFF_STATISTIC_MAPPER.keys():
                    self.__player_statistic[
                        DEBUFF_STATISTIC_MAPPER[debuff_name]
                    ] -= int(debuff_value)
                debuff_duration -= 1
            else:
                # Remove debuff effect if duration of the debuff has passed
                if debuff_name in [
                    "physical_defense_reduction",
                    "physical_damage_reduction",
                ]:
                    self.__player_statistic[
                        DEBUFF_STATISTIC_MAPPER[debuff_name]
                    ] += int(debuff_value)
                self.__debuff_dict.pop(debuff_name)

        physical_dmg *= 1 - self.__player_statistic["physical_defense"] / 200
        magical_damage *= 1 - self.__player_statistic["magical_defense"] / 200
        total_dmg = physical_dmg + magical_damage
        if "absorption" in self.__player_statistic.keys():
            total_dmg -= debuff_dict["absorption"][0]
        self.__player_statistic["health_points"] -= int(total_dmg)

    def regenerate(self) -> None:
        if "health_regeneration" in self.__player_statistic.keys():
            self.__player_statistic["health_points"] += self.__player_statistic[
                "health_regeneration"
            ]
        if "mana_regeneration" in self.__player_statistic.keys():
            self.__player_statistic["mana_points"] += self.__player_statistic[
                "mana_regeneration"
            ]
