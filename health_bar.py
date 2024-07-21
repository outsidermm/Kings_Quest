import pygame
from typing import Tuple
from pygame_gui.elements import UIPanel
from pygame_gui.core import ObjectID
import pygame_gui


class HealthBar:
    __target_value: float = None
    __max_value: float = None
    __delta_animation_speed: float = 5
    __value_ratio: float = None
    __position: pygame.Rect = None
    __ui_manager: pygame_gui.UIManager = None
    __container = None
    __flip: bool = False

    def __init__(
        self,
        ui_manager: pygame_gui.UIManager,
        container,
        position: pygame.Rect,
        init_value: int,
        max_value: int,
        delta_animation_speed: float = 2,
        icon_sprite: pygame.Surface = None,
        icon_size: Tuple[int, int] = (64,64),
        icon_sprite_gap: float = 75,
        flip: bool = False,
    ) -> None:
        self.__target_value: int = init_value
        self.__current_value: int = init_value
        self.__max_value :int = max_value
        self.__delta_animation_speed = delta_animation_speed
        self.__value_ratio = max_value / position.width
        self.__position = position
        self.__ui_manager = ui_manager
        self.__container = container
        self.__flip = flip


        init_current_value_rect, init_transition_value_rect = (
            self.compute_health_bar_rect_size(self.__target_value, self.__current_value)
        )

        icon_rect = (
            pygame.Rect(
                (position.right + icon_sprite_gap-icon_size[0],
                position.top),
                icon_size
            )
            if self.__flip
            else pygame.Rect(
                (position.left - icon_sprite_gap,
                position.top),
                icon_size
            )
        )


        icon_sprite = pygame.transform.scale(icon_sprite, icon_size)
        UIPanel(
            relative_rect=icon_rect,
            container=self.__container,
            manager=self.__ui_manager,
            object_id=ObjectID(object_id="#icon"),
        ).image = icon_sprite

        UIPanel(
            relative_rect=position,
            container=self.__container,
            manager=self.__ui_manager,
            object_id=ObjectID(object_id="#full-bar"),
        )

        self.__current_value_bar = UIPanel(
            relative_rect=init_current_value_rect,
            container=self.__container,
            manager=self.__ui_manager,
            object_id=ObjectID(object_id="#current_value-bar"),
        )

        self.__transition_bar = UIPanel(
            relative_rect=init_transition_value_rect,
            container=self.__container,
            manager=self.__ui_manager,
            object_id=ObjectID(object_id="#transition-bar"),
        )
        
        self.__hp_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (position.left, position.top),
                (position.width, position.height),
            ),
            text=f"HP: {self.__current_value} / {max_value}",
            manager=self.__ui_manager,
            container=self.__container,
            object_id=ObjectID(object_id="#hp_text"),
        )

    def update(self, target_value: int) -> None:
        self.__target_value = target_value
        self.__hp_text.set_text(f"HP: {self.__target_value} / {self.__max_value}")
        if (
            abs(self.__target_value - self.__current_value)
            < self.__delta_animation_speed
        ):
            self.__current_value = self.__target_value
        elif self.__current_value < self.__target_value:
            self.__current_value += self.__delta_animation_speed
        elif self.__current_value > self.__target_value:
            self.__current_value -= self.__delta_animation_speed

        current_value_rect, transition_value_rect = self.compute_health_bar_rect_size(
            self.__target_value, self.__current_value
        )
        self.__current_value_bar.set_dimensions(
            (current_value_rect.width, current_value_rect.height)
        )
        self.__transition_bar.set_dimensions(
            (transition_value_rect.width, transition_value_rect.height)
        )
        if self.__flip:
            self.__current_value_bar.set_relative_position(
                (
                    self.__position.left
                    + self.__position.width
                    - current_value_rect.width,
                    self.__position.top,
                )
            )
            self.__transition_bar.set_relative_position(
                (
                    self.__position.left
                    + self.__position.width
                    - transition_value_rect.width,
                    self.__position.top,
                )
            )

    def compute_health_bar_rect_size(
        self, target_value: int, current_value: int
    ) -> Tuple[pygame.Rect, pygame.Rect]:
        transition_width = int((target_value - current_value) / self.__value_ratio)
        current_value_width = int(current_value / self.__value_ratio)

        current_value_rect = pygame.Rect(
            (self.__position.left, self.__position.top),
            (current_value_width, self.__position.height),
        )

        transition_value_rect = pygame.Rect(
            (self.__position.left, self.__position.top),
            (transition_width + current_value_width, self.__position.height),
        )
        return current_value_rect, transition_value_rect
