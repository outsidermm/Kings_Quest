from characters.players.base_player import BasePlayer
from ability import PLAYER_ABILITY_LIST, Ability


class Berserker(BasePlayer):

    __statistics: dict[str, int] = {
    "health_points": 1300,
    "physical_defense": 150,
    "magical_defense": 50,
    "spell_power": 20,
    "physical_power": 120,
    "health_regeneration": 10,
    "mana_points": 100,
    "physical_damage": 80,
}

    __unlocked_abilities: list[Ability] = [PLAYER_ABILITY_LIST["Reckless Charge"]]
    __abilities: list[Ability] = [
        PLAYER_ABILITY_LIST["Reckless Charge"],
        PLAYER_ABILITY_LIST["Bloodlust"],
        PLAYER_ABILITY_LIST["Berserk"],
    ]
    __character_level: int = 1

    def __init__(self, name: str, sprite_location: str) -> None:
        super().__init__(
            name,
            self.__statistics,
            sprite_location,
            self.__abilities,
            self.__unlocked_abilities,
            self.__character_level,
        )

    def upgrade(self) -> None:
        new_statistic: dict[str, int] = self.get_statistics()
        new_unlocked_abilities: list[Ability] = self.get_unlocked_abilities()
        if self.__character_level == 1:
            self.set_character_level(2)
            new_statistic["health_points"] += 150
            new_statistic["physical_power"] += 15
        elif self.__character_level == 2:
            self.set_character_level(3)
            new_unlocked_abilities[0].upgrade()
        elif self.__character_level == 3:
            self.set_character_level(4)
            new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Bloodlust"])
        self.set_statistics(new_statistic)
        self.set_unlocked_abilities(new_unlocked_abilities)

    def unlock_ability(self) -> None:
        new_unlocked_abilities: list[Ability] = self.get_unlocked_abilities()
        new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Berserk"])
        self.set_unlocked_abilities(new_unlocked_abilities)

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
