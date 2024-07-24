import pygame
import pygame_gui
from pygame_gui.elements import UITextBox, UIPanel
from pygame_gui.core import ObjectID
from gui.statistic_bar import StatisticBar


class StatisticHUD:
    """
    HUD component to display character statistics using text and bars.

    Attributes:
        stat_text (UITextBox): The text box displaying the stat name.
        stat_bar (StatisticBar): The bar representing the stat value.
        stats (dict[str, int]): Dictionary of character stats.
        max_stat_value (int): The maximum value for the stat.
    """

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        container: UIPanel,
        stats: dict[str, int],
        stat_name: str,
        max_stat_value: int,
        stat_count: int,
        init_text_x: int = 50,
        init_bar_x: int = 300,
        init_y: int = 108,
        gap_per_stats: int = 50,
    ) -> None:
        """
        Initializes the StatisticHUD with the provided parameters.

        :param ui_manager: The UI manager to manage the HUD components.
        :param container: The container panel for the HUD.
        :param stats: Dictionary of character stats.
        :param stat_name: The name of the stat to display.
        :param max_stat_value: The maximum value of the stat for normalization.
        :param stat_count: The index of the stat to position it correctly.
        :param init_text_x: Initial x-position for the stat text.
        :param init_bar_x: Initial x-position for the stat bar.
        :param init_y: Initial y-position for the stat components.
        :param gap_per_stats: Vertical gap between each stat component.
        """
        self.set_stats(stats)
        self.set_max_stat_value(max_stat_value)

        # Create the text box for the stat name
        self.set_stat_text(
            UITextBox(
                html_text=f'<img src="assets/icons_48/{stat_name}.png"> '
                f"{' '.join(word.capitalize() for word in stat_name.split('_'))}",
                relative_rect=pygame.Rect(
                    (init_text_x, init_y + stat_count * gap_per_stats),
                    (300, -1),
                ),
                manager=ui_manager,
                container=container,
                object_id=ObjectID(object_id="#character_info"),
            )
        )

        bar_location = pygame.Rect(
            (init_bar_x, init_y + stat_count * gap_per_stats + 12.5),
            (200, 30),
        )
        bar_location.right = -50
        numerical_stat = stats.get(stat_name, 0)

        # Create the bar for the stat value
        self.set_stat_bar(
            StatisticBar(
                relative_rect=bar_location,
                manager=ui_manager,
                anchors={"right": "right"},
                percent_method=lambda stat_name=stat_name: self.progress_bar(stat_name),
                container=container,
                object_id=ObjectID(class_id="@statistics_bar"),
                text=f"{numerical_stat}/{max_stat_value}",
            )
        )

    def update(
        self,
        stats: dict[str, int],
        stat_name: str,
        max_stat_value: int,
    ) -> None:
        """
        Updates the HUD to reflect new stat values.

        :param stats: Dictionary of character stats.
        :param stat_name: The name of the stat to update.
        :param max_stat_value: The new maximum value of the stat for normalization.
        """
        numerical_stat = stats.get(stat_name, 0)
        self.get_stat_bar().set_text(f"{numerical_stat}/{max_stat_value}")
        self.get_stat_bar().redraw()

        self.set_stats(stats)
        self.set_max_stat_value(max_stat_value)

    def kill(self) -> None:
        """
        Kills (removes) the HUD components.
        """
        self.get_stat_text().kill()
        self.get_stat_bar().kill()

    def progress_bar(self, stat_name: str) -> float:
        """
        Computes the progress of the stat bar as a percentage of the maximum value.

        :param stat_name: The name of the stat.
        :return: The progress percentage of the stat bar.
        """
        return (
            self.get_stats().get(stat_name, 0) / self.get_max_stat_value()
            if self.get_max_stat_value() > 0
            else 0
        )

    def get_stat_text(self) -> UITextBox:
        """
        Gets the text box for the stat.

        :return: The stat text box.
        """
        return self.__stat_text

    def set_stat_text(self, stat_text: UITextBox) -> None:
        """
        Sets the text box for the stat.

        :param stat_text: The stat text box to set.
        """
        self.__stat_text = stat_text

    def get_stat_bar(self) -> StatisticBar:
        """
        Gets the bar for the stat.

        :return: The stat bar.
        """
        return self.__stat_bar

    def set_stat_bar(self, stat_bar: StatisticBar) -> None:
        """
        Sets the bar for the stat.

        :param stat_bar: The stat bar to set.
        """
        self.__stat_bar = stat_bar

    def get_stats(self) -> dict[str, int]:
        """
        Gets the dictionary of character stats.

        :return: The dictionary of character stats.
        """
        return self.__stats

    def set_stats(self, stats: dict[str, int]) -> None:
        """
        Sets the dictionary of character stats.

        :param stats: The dictionary of character stats to set.
        """
        self.__stats = stats

    def get_max_stat_value(self) -> int:
        """
        Gets the maximum value of the stat for normalization.

        :return: The maximum stat value.
        """
        return self.__max_stat_value

    def set_max_stat_value(self, max_stat_value: int) -> None:
        """
        Sets the maximum value of the stat for normalization.

        :param max_stat_value: The maximum stat value to set.
        """
        self.__max_stat_value = max_stat_value