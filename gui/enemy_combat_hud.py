import pygame
from pygame_gui.elements import UITextBox, UIPanel
from pygame_gui.core import ObjectID
import pygame_gui
from characters.base_character import BaseCharacter
from gui.health_bar import HealthBar

CHARACTER_STAT = [
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


class EnemyCombatHUD:
    """
    HUD for displaying player combat statistics including health bar and other stats.

    Attributes:
        __ui_manager (pygame_gui.UIManager): Manager for the UI elements.
        __player (BaseCharacter): The player character whose stats are displayed.
        __container (UIPanel): The container panel for the HUD.
        __health_bar (HealthBar): Health bar UI element.
        __HUD_text (dict[str, UITextBox]): Dictionary containing stat text boxes.
        __CHARACTER_STAT (list[str]): List of character stats to display in the HUD.
    """

    __ui_manager: pygame_gui.UIManager = None
    __player: BaseCharacter = None
    __container = None
    __health_bar: HealthBar = None
    __HUD_text: dict[str, UITextBox] = {}

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        player: BaseCharacter,
        container: UIPanel,
        HUD_init_text_y: int = 20,
        HUD_text_x: int = 75,
        HUD_step: int = 30,
    ) -> None:
        """
        Initializes the PlayerCombatHUD with the provided parameters.

        :param ui_manager: Manager for the UI elements.
        :param player: The player character whose stats are displayed.
        :param container: The container panel for the HUD.
        :param HUD_init_text_y: Initial Y position for the HUD text.
        :param HUD_text_x: X position for the HUD text.
        :param HUD_step: Vertical step between each stat text.
        """
        self.set_ui_manager(ui_manager)
        self.set_player(player)
        self.set_container(container)

        health_bar_rect = pygame.Rect((0, 20), (225, 30))
        health_bar_rect.right = 240

        # Initialize the health bar
        self.set_health_bar(
            HealthBar(
                self.get_ui_manager(),
                self.get_container(),
                health_bar_rect,
                self.get_player().get_stats()["health_points"],
                self.get_player().get_stats()["health_points"],
                True,
            )
        )

        # Initialize HUD text for each character stat
        for stat_count, stat_name in enumerate(CHARACTER_STAT):
            if stat_name not in self.get_player().get_stats().keys():
                self.get_player().get_stats()[stat_name] = 0

            if stat_name != "health_points":
                stat_rect = pygame.Rect(
                    (0, HUD_init_text_y + stat_count * HUD_step), (225, 30)
                )
                stat_rect.right = -HUD_text_x
                self.get_HUD_text()[stat_name] = UITextBox(
                    html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{' '.join(word.capitalize() for word in stat_name.split('_'))}: {self.get_player().get_stats()[stat_name]}",
                    relative_rect=stat_rect,
                    manager=self.get_ui_manager(),
                    anchors=({"right": "right"}),
                    object_id=ObjectID(object_id="#HUD-text"),
                    container=self.get_container(),
                )

    def update(self):
        """
        Updates the health bar and other stat texts in the HUD.
        """
        self.get_health_bar().update(self.get_player().get_stats()["health_points"])
        for stat_name in CHARACTER_STAT:
            if stat_name not in self.get_player().get_stats().keys():
                self.get_player().get_stats()[stat_name] = 0

            if stat_name != "health_points":
                self.get_HUD_text()[stat_name].set_text(
                    html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{' '.join(word.capitalize() for word in stat_name.split('_'))}: {self.get_player().get_stats()[stat_name]}"
                )

    def get_ui_manager(self) -> pygame_gui.UIManager:
        """
        Gets the UI manager.

        :return: The UI manager.
        """
        return self.__ui_manager

    def set_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        """
        Sets the UI manager.

        :param ui_manager: The UI manager to set.
        """
        self.__ui_manager = ui_manager

    def get_player(self) -> BaseCharacter:
        """
        Gets the player character.

        :return: The player character.
        """
        return self.__player

    def set_player(self, player: BaseCharacter) -> None:
        """
        Sets the player character.

        :param player: The player character to set.
        """
        self.__player = player

    def get_container(self) -> UIPanel:
        """
        Gets the container panel.

        :return: The container panel.
        """
        return self.__container

    def set_container(self, container: UIPanel) -> None:
        """
        Sets the container panel.

        :param container: The container panel to set.
        """
        self.__container = container

    def get_health_bar(self) -> HealthBar:
        """
        Gets the health bar.

        :return: The health bar.
        """
        return self.__health_bar

    def set_health_bar(self, health_bar: HealthBar) -> None:
        """
        Sets the health bar.

        :param health_bar: The health bar to set.
        """
        self.__health_bar = health_bar

    def get_HUD_text(self) -> dict[str, UITextBox]:
        """
        Gets the HUD text dictionary.

        :return: The HUD text dictionary.
        """
        return self.__HUD_text

    def set_HUD_text(self, HUD_text: dict[str, UITextBox]) -> None:
        """
        Sets the HUD text dictionary.

        :param HUD_text: The HUD text dictionary to set.
        """
        self.__HUD_text = HUD_text
