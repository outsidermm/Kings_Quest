import pygame
from typing import Tuple, Any
from pygame_gui.elements import UIPanel, UITextBox
from pygame_gui.core import ObjectID
import pygame_gui


class HealthBar:
    """
    HealthBar is a class that manages and displays a health bar with animated changes in value.

    Attributes:
        __target_value (float): The target value of the health bar.
        __current_value (float): The current value of the health bar.
        __max_value (float): The maximum value of the health bar.
        __delta_animation_speed (float): The speed of the animation when the health bar changes.
        __value_ratio (float): The ratio of the max value to the width of the bar.
        __position (pygame.Rect): The position and size of the health bar.
        __ui_manager (pygame_gui.UIManager): The UI manager for managing UI elements.
        __container (Any): The container for the health bar UI elements.
        __is_flipped (bool): Indicates if the health bar is flipped horizontally.
        __current_value_bar (UIPanel): Panel representing the current health value.
        __transition_bar (UIPanel): Panel representing the transition animation of health value.
        __hp_text (UITextBox): Text box displaying the current health as text.
    """

    __target_value: float = None
    __max_value: float = None
    __delta_animation_speed: float = 5
    __value_ratio: float = None
    __position: pygame.Rect = None
    __ui_manager: pygame_gui.UIManager = None
    __container = None
    __is_flipped: bool = False
    __current_value_bar: UIPanel = None
    __transition_bar: UIPanel = None
    __hp_text: UITextBox = None

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        container: Any,
        position: pygame.Rect,
        init_value: int,
        max_value: int,
        delta_animation_speed: float = 5,
        is_flipped: bool = False,
    ) -> None:
        """
        Initializes the HealthBar with the provided parameters.

        :param ui_manager: The UI manager for managing UI elements.
        :param container: The container for the health bar UI elements.
        :param position: The position and size of the health bar.
        :param init_value: The initial value of the health bar.
        :param max_value: The maximum value of the health bar.
        :param delta_animation_speed: The speed of the animation when the health bar changes.
        :param is_flipped: Indicates if the health bar is flipped horizontally.
        """
        # Initialize all attributes using the provided parameters
        self.set_target_value(init_value)
        self.set_current_value(init_value)
        self.set_max_value(max_value)
        self.set_delta_animation_speed(delta_animation_speed)
        self.set_value_ratio(max_value / position.width)
        self.set_position(position)
        self.set_ui_manager(ui_manager)
        self.set_container(container)
        self.set_is_flipped(is_flipped)

        # Calculate the initial sizes of the health bar panels
        init_current_value_rect, init_transition_value_rect = (
            self.compute_health_bar_rect_size(
                self.get_target_value(), self.get_current_value()
            )
        )

        # Create the full bar panel
        UIPanel(
            relative_rect=position,
            container=self.get_container(),
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#full-bar"),
        )

        # Create the current value panel
        self.set_current_value_bar(
            UIPanel(
                relative_rect=init_current_value_rect,
                container=self.get_container(),
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#current_value-bar"),
            )
        )

        # Create the transition value panel
        self.set_transition_bar(
            UIPanel(
                relative_rect=init_transition_value_rect,
                container=self.get_container(),
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#transition-bar"),
            )
        )

        # Create the health text box
        self.set_hp_text(
            UITextBox(
                relative_rect=pygame.Rect(
                    (position.left, position.top),
                    (position.width, position.height),
                ),
                html_text=f"HP: {self.get_current_value()} / {max_value}",
                manager=self.get_ui_manager(),
                container=self.get_container(),
                object_id=ObjectID(object_id="#HUD-text"),
            )
        )

    def update(self, target_value: int) -> None:
        """
        Updates the health bar with a new target value and animates the change.

        :param target_value: The new target value of the health bar.
        """
        # Update the target value
        self.set_target_value(target_value)

        # Update the health text box
        self.get_hp_text().set_text(
            f"HP: {self.get_target_value()} / {self.get_max_value()}"
        )

        # Animate the transition of the current value towards the target value
        if (
            abs(self.get_target_value() - self.get_current_value())
            < self.get_delta_animation_speed()
        ):
            self.set_current_value(self.get_target_value())
        elif self.get_current_value() < self.get_target_value():
            self.set_current_value(
                self.get_current_value() + self.get_delta_animation_speed()
            )
        elif self.get_current_value() > self.get_target_value():
            self.set_current_value(
                self.get_current_value() - self.get_delta_animation_speed()
            )

        # Calculate the sizes of the current value and transition bars
        current_value_rect, transition_value_rect = self.compute_health_bar_rect_size(
            self.get_target_value(), self.get_current_value()
        )

        # Update the dimensions of the current value and transition bars
        self.get_current_value_bar().set_dimensions(
            (current_value_rect.width, current_value_rect.height)
        )
        self.get_transition_bar().set_dimensions(
            (transition_value_rect.width, transition_value_rect.height)
        )

        # If the health bar is flipped, adjust the positions accordingly
        if self.get_is_flipped():
            self.get_current_value_bar().set_relative_position(
                (
                    self.get_position().left
                    + self.get_position().width
                    - current_value_rect.width,
                    self.get_position().top,
                )
            )
            self.get_transition_bar().set_relative_position(
                (
                    self.get_position().left
                    + self.get_position().width
                    - transition_value_rect.width,
                    self.get_position().top,
                )
            )

    def compute_health_bar_rect_size(
        self, target_value: int, current_value: int
    ) -> Tuple[pygame.Rect, pygame.Rect]:
        """
        Computes the sizes of the current value and transition bars.

        :param target_value: The target value of the health bar.
        :param current_value: The current value of the health bar.
        :return: The rect sizes for the current value and transition bars.
        """
        # Calculate the widths of the transition and current value bars
        transition_width = int((target_value - current_value) / self.get_value_ratio())
        current_value_width = int(current_value / self.get_value_ratio())

        # Define the rect for the current value bar
        current_value_rect = pygame.Rect(
            (self.get_position().left, self.get_position().top),
            (current_value_width, self.get_position().height),
        )

        # Define the rect for the transition bar
        transition_value_rect = pygame.Rect(
            (self.get_position().left, self.get_position().top),
            (transition_width + current_value_width, self.get_position().height),
        )
        return current_value_rect, transition_value_rect

    # Getters and setters for all attributes
    def get_target_value(self) -> float:
        return self.__target_value

    def set_target_value(self, target_value: float) -> None:
        self.__target_value = target_value

    def get_current_value(self) -> float:
        return self.__current_value

    def set_current_value(self, current_value: float) -> None:
        self.__current_value = current_value

    def get_max_value(self) -> float:
        return self.__max_value

    def set_max_value(self, max_value: float) -> None:
        self.__max_value = max_value

    def get_delta_animation_speed(self) -> float:
        return self.__delta_animation_speed

    def set_delta_animation_speed(self, delta_animation_speed: float) -> None:
        self.__delta_animation_speed = delta_animation_speed

    def get_value_ratio(self) -> float:
        return self.__value_ratio

    def set_value_ratio(self, value_ratio: float) -> None:
        self.__value_ratio = value_ratio

    def get_position(self) -> pygame.Rect:
        return self.__position

    def set_position(self, position: pygame.Rect) -> None:
        self.__position = position

    def get_ui_manager(self) -> pygame_gui.UIManager:
        return self.__ui_manager

    def set_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        self.__ui_manager = ui_manager

    def get_container(self) -> Any:
        return self.__container

    def set_container(self, container: Any) -> None:
        self.__container = container

    def get_is_flipped(self) -> bool:
        return self.__is_flipped

    def set_is_flipped(self, is_flipped: bool) -> None:
        self.__is_flipped = is_flipped

    def get_current_value_bar(self) -> UIPanel:
        return self.__current_value_bar

    def set_current_value_bar(self, current_value_bar: UIPanel) -> None:
        self.__current_value_bar = current_value_bar

    def get_transition_bar(self) -> UIPanel:
        return self.__transition_bar

    def set_transition_bar(self, transition_bar: UIPanel) -> None:
        self.__transition_bar = transition_bar

    def get_hp_text(self) -> UITextBox:
        return self.__hp_text

    def set_hp_text(self, hp_text: UITextBox) -> None:
        self.__hp_text = hp_text
