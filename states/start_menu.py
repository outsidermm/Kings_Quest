from .base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UITextBox
from pygame_gui.core import ObjectID
from utilities.json_utility import write_default_if_not_exist
import os
import sys


class StartMenu(BaseState):
    __play_button = None
    __setting_button = None
    __quit_button = None
    __play_button_pressed = False
    __setting_button_pressed = False
    __game_title = None
    __background_image = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
    ) -> None:
        super().__init__(
            "start_menu",
            screen,
            ui_manager,
            "character_selection_menu",
            game_state_manager,
        )

    def start(self) -> None:
        self.set_game_title(
            UITextBox(
                "King's Quest",
                pygame.Rect((0, -self.get_screen().height * 0.3), (1000, 200)),
                self.get_ui_manager(),
                anchors=({"center": "center"}),
                object_id=ObjectID(class_id="@title", object_id="#game_title"),
            )
        )

        self.set_play_button(
            UIButton(
                relative_rect=pygame.Rect((0, 0), (500, 70)),
                text="PLAY",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
            )
        )

        self.set_setting_button(
            UIButton(
                relative_rect=pygame.Rect(
                    (0, self.get_screen().height * 0.15), (500, 70)
                ),
                text="RESET GAME",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
            )
        )

        self.set_quit_button(
            UIButton(
                relative_rect=pygame.Rect(
                    (0, self.get_screen().height * 0.3), (500, 70)
                ),
                text="QUIT",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
            )
        )

        self.set_background_image(
            pygame.transform.scale(
                pygame.image.load("assets/background_image.png"),
                (self.get_screen().width, self.get_screen().height),
            )
        )
        pygame.display.set_caption("King's Quest")

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_time_to_quit_app(True)
            self.get_ui_manager().process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.get_play_button():
                    self.set_play_button_pressed(True)
                if event.ui_element == self.get_setting_button():
                    self.set_setting_button_pressed(True)
                if event.ui_element == self.get_quit_button():
                    self.set_time_to_quit_app(True)

    def run(self) -> None:
        if self.get_play_button_pressed():
            self.set_time_to_transition(True)
        elif self.get_setting_button_pressed():
            os.remove("settings/user_settings.json")
            # Default user data
            default_user_data = {
                "xp": 5000,
                "quest_progress": {
                    "Fireball": 0,
                    "Kill DreadNoughts": 0,
                },
                "quest_claimed": {
                    "Fireball": False,
                    "Kill DreadNoughts": False,
                },
                "character_level": {
                    "Warrior": 1,
                    "Mage": 1,
                    "Berserker": 1,
                    "Ranger": 1,
                },
                "character_abilities": {
                    "Warrior": ["Power Slash"],
                    "Mage": ["Fireball"],
                    "Berserker": ["Reckless Charge"],
                    "Ranger": ["Arrow Barrage"],
                },
            }
            write_default_if_not_exist(
                "settings/user_settings.json", default_data=default_user_data
            )
            os.execl(sys.executable, sys.executable, *sys.argv)

    def render(self, time_delta: int) -> None:
        self.get_ui_manager().update(time_delta)

        self.get_screen().blit(self.__background_image, (0, 0))
        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        self.set_play_button_pressed(False)
        self.set_setting_button_pressed(False)

    def end(self) -> None:
        self.get_game_title().kill()
        self.get_play_button().kill()
        self.get_setting_button().kill()
        self.get_quit_button().kill()
        self.get_screen().fill((0, 0, 0))

    def get_screen(self) -> pygame.Surface:
        return super().get_screen()

    def set_screen(self, screen: pygame.Surface) -> None:
        super().set_screen(screen)

    def get_ui_manager(self) -> pygame_gui.UIManager:
        return super().get_ui_manager()

    def set_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        super().set_ui_manager(ui_manager)

    def get_game_state_manager(self) -> GameStateManager:
        return super().get_game_state_manager()

    def set_game_state_manager(self, game_state_manager: GameStateManager) -> None:
        super().set_game_state_manager(game_state_manager)

    def get_play_button_pressed(self) -> bool:
        return self.__play_button_pressed

    def get_setting_button_pressed(self) -> bool:
        return self.__setting_button_pressed

    def set_play_button_pressed(self, play_button_pressed: bool) -> None:
        self.__play_button_pressed = play_button_pressed

    def set_setting_button_pressed(self, setting_button_pressed: bool) -> None:
        self.__setting_button_pressed = setting_button_pressed

    def get_play_button(self) -> UIButton:
        return self.__play_button

    def get_setting_button(self) -> UIButton:
        return self.__setting_button

    def get_quit_button(self) -> UIButton:
        return self.__quit_button

    def set_play_button(self, play_button: UIButton) -> None:
        self.__play_button = play_button

    def set_setting_button(self, setting_button: UIButton) -> None:
        self.__setting_button = setting_button

    def set_quit_button(self, quit_button: UIButton) -> None:
        self.__quit_button = quit_button

    def get_game_title(self) -> UITextBox:
        return self.__game_title

    def set_game_title(self, game_title: UITextBox) -> None:
        self.__game_title = game_title

    def get_background_image(self) -> pygame.Surface:
        return self.__background_image

    def set_background_image(self, background_image: pygame.Surface) -> None:
        self.__background_image = background_image

    def set_time_to_quit_app(self, time_to_quit_app: bool) -> None:
        super().set_time_to_quit_app(time_to_quit_app)

    def get_time_to_quit_app(self) -> bool:
        return super().get_time_to_quit_app()

    def set_time_to_transition(self, time_to_transition: bool) -> None:
        super().set_time_to_transition(time_to_transition)

    def get_time_to_transition(self) -> bool:
        return super().get_time_to_transition()

    def set_target_state_name(self, target_state_name: str) -> None:
        super().set_target_state_name(target_state_name)

    def get_target_state_name(self) -> str:
        return super().get_target_state_name()
