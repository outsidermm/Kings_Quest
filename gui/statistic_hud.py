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
    __stat_text: UITextBox = None
    __stat_bar: StatisticBar = None
    __stats: dict[str, int] = None
    __max_stat_value: int = None

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        container: UIPanel,
        stats: dict[str, int],
        stat_name: str,
        max_stat_value: int,
        stat_count: int,
    ) -> None:
        self.__stats = stats
        self.__max_stat_value = max_stat_value

        init_text_x = 50
        init_bar_x = 300
        init_y = 108
        gap_per_stats = 50

        self.__stat_text = UITextBox(
            html_text=f'<img src="assets/icons_48/{stat_name}.png"> '
            f"{" ".join(word.capitalize() for word in stat_name.split("_"))}",
            relative_rect=pygame.Rect(
                (init_text_x, init_y + stat_count * gap_per_stats),
                (300, -1),
            ),
            manager=ui_manager,
            container=container,
            object_id=ObjectID(object_id="#character_info"),
        )

        bar_location = pygame.Rect(
            (init_bar_x, init_y + stat_count * gap_per_stats + 12.5),
            (200, 30),
        )
        bar_location.right = -50
        numerical_stat = stats[stat_name] if stat_name in stats.keys() else 0

        self.__stat_bar = StatisticBar(
            relative_rect=bar_location,
            manager=ui_manager,
            anchors=({"right": "right"}),
            percent_method=(lambda stat_name=stat_name,: self.progress_bar(stat_name)),
            container=container,
            object_id=ObjectID(class_id="@statistics_bar"),
            text=f"{numerical_stat}/{max_stat_value}",
        )

    def update(
        self,
        stats: dict[str, int],
        stat_name: str,
        max_stat_value: int,
    ) -> None:
        numerical_stat = stats[stat_name] if stat_name in stats.keys() else 0
        self.__stat_bar.set_text(f"{numerical_stat}/{max_stat_value}")
        self.__stat_bar.redraw()

        self.__stats = stats
        self.__max_stat_value = max_stat_value

    def kill(self) -> None:
        self.__stat_text.kill()
        self.__stat_bar.kill()

    def progress_bar(self, stat_name: str) -> float:
        return (
            self.__stats[stat_name] / self.__max_stat_value
            if stat_name in self.__stats.keys()
            else 0
        )
