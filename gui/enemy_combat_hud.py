import pygame
from pygame_gui.elements import UITextBox, UIPanel
from pygame_gui.core import ObjectID
import pygame_gui
from characters.base_character import BaseCharacter
from gui.health_bar import HealthBar


class EnemyCombatHUD:
    __ui_manager: pygame_gui.UIManager = None
    __player: BaseCharacter = None
    __container = None
    __health_bar: HealthBar = None
    __HUD_text: dict[str, UITextBox] = {}

    __CHARACTER_STAT = [
        "health_points",
        "physical_defense",
        "magical_defense",
        "spell_power",
        "physical_power",
        "health_regeneration",
        "mana_regeneration",
        "mana_points",
        "physical_damage",
        "magical_damage",
    ]

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        player: BaseCharacter,
        container: UIPanel,
        HUD_init_text_y: int = 20,
        HUD_text_x: int = 75,
        HUD_step: int = 30,
    ) -> None:
        self.__ui_manager = ui_manager
        self.__player = player
        self.__container = container

        health_bar_rect = pygame.Rect((0, 20), (225, 30))
        health_bar_rect.right = 240

        self.__health_bar = HealthBar(
            self.__ui_manager,
            self.__container,
            health_bar_rect,
            self.__player.get_stats()["health_points"],
            self.__player.get_stats()["health_points"],
            is_flipped=True,
        )

        for stat_count, stat_name in enumerate(self.__CHARACTER_STAT):
            if stat_name not in self.__player.get_stats().keys():
                self.__player.get_stats()[stat_name] = 0

            if stat_name != "health_points":
                stat_rect = pygame.Rect(
                    (0, HUD_init_text_y + stat_count * HUD_step), (225, 30)
                )
                stat_rect.right = -HUD_text_x

                self.__HUD_text[stat_name] = UITextBox(
                    html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{" ".join(word.capitalize() for word in stat_name.split("_"))}: {self.__player.get_stats()[stat_name]}",
                    relative_rect=stat_rect,
                    manager=self.__ui_manager,
                    anchors=({"right": "right"}),
                    object_id=ObjectID(object_id="#HUD-text"),
                    container=self.__container,
                )

    def update(self):
        self.__health_bar.update(self.__player.get_stats()["health_points"])
        for stat_name in self.__CHARACTER_STAT:
            if stat_name not in self.__player.get_stats().keys():
                self.__player.get_stats()[stat_name] = 0

            if stat_name != "health_points":
                self.__HUD_text[stat_name].set_text(
                    html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{" ".join(word.capitalize() for word in stat_name.split("_"))}: {self.__player.get_stats()[stat_name]}"
                )
