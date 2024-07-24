from characters.base_character import BaseCharacter
from ability import Ability
from typing import Tuple, Dict, List
import random
from utilities.general_utility import min_max_bound
from pygame_gui.elements import UIImage


class CombatController:
    """
    CombatController class to manage combat-related mechanics for a player character,
    including handling abilities, buffs, debuffs, and damage calculations.
    """

    # Mapping debuff effects to player statistics
    __DEBUFF_STAT_MAPPER = {
        "physical_defense_reduction": "physical_defense",
        "physical_damage_reduction": "physical_damage",
        "bleed": "health_points",
    }

    # List of positive player statistic modifiers
    __POSITIVE_PLAYER_STAT_MODIFIERS = [
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

    # List of negative player statistic modifiers
    __NEGATIVE_PLAYER_STAT_MODIFIERS = [
        "stun",
        "physical_defense_reduction",
        "physical_damage_reduction",
        "bleed",
    ]
    __player_stat: Dict[str, int] = {}
    __player_stat_cap: Dict[str, int] = {}
    __debuff_dict: Dict[str, Tuple[int, int]] = {}
    __ability_histories: List[Ability] = []
    __cooldown_abilities: Dict[str, int] = {}
    __player_sprite: UIImage = None
    __is_stunned: bool = False

    def __init__(self, player: BaseCharacter, player_sprite: UIImage) -> None:
        """
        Initializes the CombatController class.

        :param player: The player character.
        :param player_sprite: The player sprite.
        """
        # Initialize player statistics and sprite
        self.set_player_stat(player.get_stats())
        self.set_player_stat_cap(player.get_stats())
        self.set_player_sprite(player_sprite)
        self.set_debuff_dict({})
        self.set_ability_histories([])
        self.set_cooldown_abilities({})
        self.set_is_stunned(False)

    def is_ability_on_cooldown(self, ability: Ability) -> bool:
        """
        Checks if an ability is on cooldown.

        :param ability: The ability to check.
        :return: True if the ability is on cooldown, False otherwise.
        """
        return ability.get_name() in self.get_cooldown_abilities().keys()

    def stunned_round(self) -> None:
        """
        Handles the actions to be taken when the player is stunned, including
        decrementing ability durations and removing expired abilities.
        """
        self.handle_ability_durations()  # Handle ability durations
        self.set_is_stunned(False)  # Reset stun status

    def handle_ability_cooldowns(self) -> None:
        """
        Handles the cooldowns of abilities, decrementing their cooldown counters and
        removing them from the cooldown dictionary when the cooldown expires.
        """
        cooldown_abilities_to_remove = []

        # Iterate through cooldown abilities
        for (
            cooldown_ability_name,
            cooldown_count,
        ) in self.get_cooldown_abilities().items():
            if cooldown_count > 1:
                self.get_cooldown_abilities()[cooldown_ability_name] -= 1
            else:
                cooldown_abilities_to_remove.append(cooldown_ability_name)

        # Remove abilities that are no longer on cooldown
        for cooldown_ability_name in cooldown_abilities_to_remove:
            del self.get_cooldown_abilities()[cooldown_ability_name]

    def handle_ability_durations(self) -> None:
        """
        Handles the durations of abilities, decrementing their duration counters and
        removing expired abilities from the history.
        """
        abilities_to_remove = []

        # Iterate through ability histories
        for player_ability in self.get_ability_histories():
            if player_ability.get_duration() > 0:
                player_ability.set_duration(player_ability.get_duration() - 1)
            else:
                # Remove buff effect if duration of the ability has passed
                for modifier, value in player_ability.get_stats().items():
                    if (
                        modifier in self.__POSITIVE_PLAYER_STAT_MODIFIERS
                        and modifier in self.get_player_stat().keys()
                    ):
                        self.get_player_stat()[modifier] -= value
                        self.get_player_stat()[modifier] = max(
                            0, self.get_player_stat()[modifier]
                        )
                abilities_to_remove.append(player_ability)

        # Remove expired abilities from history
        for ability_to_remove in abilities_to_remove:
            self.get_ability_histories().remove(ability_to_remove)

    def attack(
        self, hit_height: float, ability: Ability = None
    ) -> Tuple[int, int, Dict[str, Tuple[int, int]]]:
        """
        Calculates the physical and magical damage dealt in an attack, applying any ability effects.

        :param hit_height: The height of the hit for calculating critical rate.
        :param ability: The ability used in the attack (optional).
        :return: A tuple containing the physical damage, magical damage, and any debuffs applied.
        """
        debuff_dict: Dict[str, Tuple[int, int]] = {}
        self.handle_ability_cooldowns()  # Handle ability cooldowns

        # Calculate critical rate
        critical_rate = hit_height / self.get_player_sprite().rect.height * 100
        if ability is not None:
            self.get_ability_histories().append(ability.copy())
            self.get_cooldown_abilities()[ability.get_name()] = ability.get_stats()[
                "cooldown"
            ]

            # Deduct ability cost from player stats
            for cost in ability.get_cost():
                self.get_player_stat()[cost[0]] -= cost[1]

            # Apply ability modifiers to player stats
            for modifier, value in ability.get_stats().items():
                if modifier == "critical":
                    critical_rate += value
                elif modifier in self.__NEGATIVE_PLAYER_STAT_MODIFIERS:
                    debuff_dict[modifier] = (value, ability.get_duration())
                elif modifier in self.__POSITIVE_PLAYER_STAT_MODIFIERS:
                    if modifier in self.get_player_stat().keys():
                        self.get_player_stat()[modifier] += value
                    else:
                        self.get_player_stat()[modifier] = value

        self.handle_ability_durations()  # Handle ability durations

        # Calculate physical and magical damage with critical rate
        critical_dmg_addition = random.randint(0, int(critical_rate))
        physical_dmg = magical_dmg = 0
        if (
            "physical_damage" in self.get_player_stat().keys()
            and "physical_power" in self.get_player_stat().keys()
        ):
            physical_dmg = max(
                0,
                int(
                    self.get_player_stat()["physical_damage"]
                    * self.get_player_stat()["physical_power"]
                    / 50
                    + critical_dmg_addition
                ),
            )
        if (
            "magical_damage" in self.get_player_stat().keys()
            and "spell_power" in self.get_player_stat().keys()
        ):
            magical_dmg = max(
                0,
                int(
                    self.get_player_stat()["magical_damage"]
                    * self.get_player_stat()["spell_power"]
                    / 50
                    + critical_dmg_addition
                ),
            )
        return (physical_dmg, magical_dmg, debuff_dict)

    def face_damage(
        self,
        physical_dmg: int,
        magical_damage: int,
        debuff_dict: Dict[str, Tuple[int, int]],
    ) -> None:
        """
        Applies damage to the player and handles debuffs.

        :param physical_dmg: The physical damage to be applied.
        :param magical_damage: The magical damage to be applied.
        :param debuff_dict: Dictionary of debuffs to be applied.
        """
        # Apply debuffs to the player
        for debuff_name, (debuff_value, debuff_duration) in debuff_dict.items():
            if debuff_name == "stun":
                self.set_is_stunned(True)
            else:
                self.get_debuff_dict()[debuff_name] = (debuff_value, debuff_duration)

        debuffs_to_remove = []

        # Handle existing debuffs and their durations
        for debuff_name, (
            debuff_value,
            debuff_duration,
        ) in self.get_debuff_dict().items():
            if debuff_duration > 1:
                if (
                    debuff_name in self.__DEBUFF_STAT_MAPPER.keys()
                    and self.__DEBUFF_STAT_MAPPER[debuff_name]
                    in self.get_player_stat().keys()
                ):
                    self.get_player_stat()[
                        self.__DEBUFF_STAT_MAPPER[debuff_name]
                    ] -= int(debuff_value)
                    self.get_player_stat()[self.__DEBUFF_STAT_MAPPER[debuff_name]] = (
                        max(
                            0,
                            self.get_player_stat()[
                                self.__DEBUFF_STAT_MAPPER[debuff_name]
                            ],
                        )
                    )
                self.get_debuff_dict()[debuff_name] = (
                    debuff_value,
                    debuff_duration - 1,
                )
            else:
                if (
                    debuff_name
                    in [
                        "physical_defense_reduction",
                        "physical_damage_reduction",
                    ]
                    and self.__DEBUFF_STAT_MAPPER[debuff_name]
                    in self.get_player_stat().keys()
                ):
                    self.get_player_stat()[
                        self.__DEBUFF_STAT_MAPPER[debuff_name]
                    ] += int(debuff_value)
                debuffs_to_remove.append(debuff_name)

        # Remove debuffs from the dictionary after the iteration
        for debuff_name in debuffs_to_remove:
            del self.get_debuff_dict()[debuff_name]

        # Calculate damage with defense modifiers
        physical_dmg *= 1 - self.get_player_stat()["physical_defense"] / 400
        magical_damage *= 1 - self.get_player_stat()["magical_defense"] / 400
        physical_dmg = max(0, physical_dmg)
        magical_damage = max(0, magical_damage)
        total_dmg = physical_dmg + magical_damage

        # Apply absorption if available
        if "absorption" in self.get_player_stat().keys():
            total_dmg = max(0, total_dmg - self.get_player_stat()["absorption"])

        # Reduce health points by total damage
        self.get_player_stat()["health_points"] = max(
            0, self.get_player_stat()["health_points"] - int(total_dmg)
        )

    def regenerate(self) -> None:
        """
        Regenerates health and mana points for the player based on their regeneration rates.
        """
        # Regenerate health points
        if "health_regeneration" in self.get_player_stat().keys():
            self.get_player_stat()["health_points"] = min_max_bound(
                0,
                self.get_player_stat_cap()["health_points"],
                self.get_player_stat()["health_points"]
                + self.get_player_stat()["health_regeneration"],
            )
        # Regenerate mana points
        if "mana_regeneration" in self.get_player_stat().keys():
            self.get_player_stat()["mana_points"] = min_max_bound(
                0,
                self.get_player_stat_cap()["mana_points"],
                self.get_player_stat()["mana_points"]
                + self.get_player_stat()["mana_regeneration"],
            )

    # Getters and setters with docstrings

    def get_player_stat(self) -> Dict[str, int]:
        """
        Gets the player's current stats.

        :return: A dictionary of the player's current stats.
        """
        return self.__player_stat

    def set_player_stat(self, stats: Dict[str, int]) -> None:
        """
        Sets the player's current stats.

        :param stats: A dictionary of the player's new stats.
        """
        self.__player_stat = stats

    def get_player_stat_cap(self) -> Dict[str, int]:
        """
        Gets the player's stats cap.

        :return: A dictionary of the player's stats cap.
        """
        return self.__player_stat_cap

    def set_player_stat_cap(self, stats_cap: Dict[str, int]) -> None:
        """
        Sets the player's stats cap.

        :param stats_cap: A dictionary of the player's new stats cap.
        """
        self.__player_stat_cap = stats_cap

    def get_debuff_dict(self) -> Dict[str, Tuple[int, int]]:
        """
        Gets the player's debuff dictionary.

        :return: A dictionary of the player's debuffs.
        """
        return self.__debuff_dict

    def set_debuff_dict(self, debuff_dict: Dict[str, Tuple[int, int]]) -> None:
        """
        Sets the player's debuff dictionary.

        :param debuff_dict: A dictionary of the player's new debuffs.
        """
        self.__debuff_dict = debuff_dict

    def get_ability_histories(self) -> List[Ability]:
        """
        Gets the player's ability history.

        :return: A list of the player's ability history.
        """
        return self.__ability_histories

    def set_ability_histories(self, ability_histories: List[Ability]) -> None:
        """
        Sets the player's ability history.

        :param ability_histories: A list of the player's new ability history.
        """
        self.__ability_histories = ability_histories

    def get_cooldown_abilities(self) -> Dict[str, int]:
        """
        Gets the player's cooldown abilities.

        :return: A dictionary of the player's cooldown abilities.
        """
        return self.__cooldown_abilities

    def set_cooldown_abilities(self, cooldown_abilities: Dict[str, int]) -> None:
        """
        Sets the player's cooldown abilities.

        :param cooldown_abilities: A dictionary of the player's new cooldown abilities.
        """
        self.__cooldown_abilities = cooldown_abilities

    def get_player_sprite(self) -> UIImage:
        """
        Gets the player's sprite.

        :return: The player's sprite.
        """
        return self.__player_sprite

    def set_player_sprite(self, player_sprite: UIImage) -> None:
        """
        Sets the player's sprite.

        :param player_sprite: The new player's sprite.
        """
        self.__player_sprite = player_sprite

    def get_is_stunned(self) -> bool:
        """
        Gets the player's stunned status.

        :return: True if the player is stunned, False otherwise.
        """
        return self.__is_stunned

    def set_is_stunned(self, is_stunned: bool) -> None:
        """
        Sets the player's stunned status.

        :param is_stunned: The new stunned status.
        """
        self.__is_stunned = is_stunned
