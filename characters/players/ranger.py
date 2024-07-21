from characters.players.base_player import BasePlayer
from ability import PLAYER_ABILITY_LIST, Ability


class Ranger(BasePlayer):

    __statistics: dict = {
    "health_points": 950,
    "physical_defense": 110,
    "magical_defense": 90,
    "spell_power": 60,
    "physical_power": 80,
    "health_regeneration": 12,
    "mana_points": 200,
    "physical_damage": 70,
}
    __unlocked_abilities: list[Ability] = [PLAYER_ABILITY_LIST["Arrow Barrage"]]
    __abilities: list[Ability] = [
        PLAYER_ABILITY_LIST["Arrow Barrage"],
        PLAYER_ABILITY_LIST["Natural Grace"],
        PLAYER_ABILITY_LIST["Fatal Shadow"],
    ]
    __character_level: int = 4

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
            new_statistic["health_points"] += 100
            new_statistic["physical_power"] += 10
        elif self.__character_level == 2:
            self.set_character_level(3)
            new_unlocked_abilities[0].upgrade()
        elif self.__character_level == 3:
            self.set_character_level(4)
            new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Natural Grace"])
        self.set_statistics(new_statistic)
        self.set_unlocked_abilities(new_unlocked_abilities)

    def unlock_ability(self) -> None:
        new_unlocked_abilities: list[Ability] = self.get_unlocked_abilities()
        new_unlocked_abilities.append(PLAYER_ABILITY_LIST["Fatal Shadow"])
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
