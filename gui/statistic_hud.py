import pygame
import pygame_gui
from pygame_gui.elements import UITextBox, UIPanel, UIStatusBar
from pygame_gui.core import ObjectID


class StatisticBar(UIStatusBar):
    def __init__(
        self,
        text: str = None,
        *args,
        **kwargs,
    ) -> None:
        self.__bar_text = text
        super().__init__(*args, **kwargs)

    def status_text(self) -> str:
        return self.__bar_text

    def set_text(self, text: str) -> None:
        self.__bar_text = text


class StatisticHUD:
    __statistic_text: UITextBox = None
    __statistic_bar: StatisticBar = None
    __statistics: dict[str, int] = None
    __max_statistic_value: int = None

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        container: UIPanel,
        statistics: dict[str, int],
        statistic_name: str,
        max_statistic_value: int,
        statistic_count: int,
    ) -> None:
        self.__statistics = statistics
        self.__max_statistic_value = max_statistic_value

        init_text_x = 50
        init_bar_x = 300
        init_y = 108
        gap_per_statistics = 50

        self.__statistic_text = UITextBox(
            html_text=f'<img src="assets/icons_48/{statistic_name}.png"> '
            f"{" ".join(word.capitalize() for word in statistic_name.split("_"))}",
            relative_rect=pygame.Rect(
                (init_text_x, init_y + statistic_count * gap_per_statistics),
                (300, -1),
            ),
            manager=ui_manager,
            container=container,
            object_id=ObjectID(object_id="#character_info"),
        )

        bar_location = pygame.Rect(
            (init_bar_x, init_y + statistic_count * gap_per_statistics + 12.5),
            (200, 30),
        )
        bar_location.right = -50
        numerical_statistic = (
            statistics[statistic_name] if statistic_name in statistics.keys() else 0
        )

        self.__statistic_bar = StatisticBar(
            relative_rect=bar_location,
            manager=ui_manager,
            anchors=({"right": "right"}),
            percent_method=(
                lambda statistic_name=statistic_name,: self.progress_bar(statistic_name)
            ),
            container=container,
            object_id=ObjectID(class_id="@statistics_bar"),
            text=f"{numerical_statistic}/{max_statistic_value}",
        )

    def update(
        self,
        statistics: dict[str, int],
        statistic_name: str,
        max_statistic_value: int,
    ) -> None:
        numerical_statistic = (
            statistics[statistic_name] if statistic_name in statistics.keys() else 0
        )
        self.__statistic_bar.set_text(f"{numerical_statistic}/{max_statistic_value}")
        self.__statistic_bar.redraw()

        self.__statistics = statistics
        self.__max_statistic_value = max_statistic_value

    def kill(self) -> None:
        self.__statistic_text.kill()
        self.__statistic_bar.kill()

    def progress_bar(self, statistic_name: str) -> float:
        return (
            self.__statistics[statistic_name] / self.__max_statistic_value
            if statistic_name in self.__statistics.keys()
            else 0
        )
