from .base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UITextBox
from pygame_gui.core import ObjectID


class StartMenu(BaseState):
    __play_button = None
    __setting_button = None
    __quit_button = None
    __play_button_pressed = False
    __setting_button_pressed = False
    __quit_button_pressed = False
    __game_title = None
    __GUIBackground = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
    ) -> None:
        super().__init__(screen, ui_manager, game_state_manager)
        self.__screen_width = self.get_screen().get_rect().width
        self.__screen_height = self.get_screen().get_rect().height

        self.set_game_title(
            UITextBox(
                "King's Quest",
                pygame.Rect((0, -self.__screen_height * 0.3), (1000, 200)),
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
                relative_rect=pygame.Rect((0, self.__screen_height * 0.15), (500, 70)),
                text="SETTINGS",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
            )
        )

        self.set_quit_button(
            UIButton(
                relative_rect=pygame.Rect((0, self.__screen_height * 0.3), (500, 70)),
                text="QUIT",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
            )
        )

        self.set_GUIBackground(
            pygame.transform.scale(
                pygame.image.load("assets/GUIBackground.png"),
                (self.__screen_width, self.__screen_height),
            )
        )
        pygame.display.set_caption("King's Quest")

    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.get_play_button():
                self.set_play_button_pressed(True)
            if event.ui_element == self.get_setting_button():
                self.set_setting_button_pressed(True)
            if event.ui_element == self.get_quit_button():
                self.set_quit_button_pressed(True)

    def run(self) -> None:
        if self.get_play_button_pressed():
            self.get_screen().fill((0, 0, 0))
            # self.remove_UI()
            self.get_game_state_manager().set_state("character_selection_menu")
        elif self.get_setting_button_pressed():
            # self.get_game_state_manager().set_state("settings")
            self.remove_UI()
        elif self.get_quit_button_pressed():
            pygame.quit()
            quit()

    def reset_event_polling(self) -> None:
        self.set_play_button_pressed(False)
        self.set_setting_button_pressed(False)
        self.set_quit_button_pressed(False)

    def remove_UI(self) -> None:
        self.get_game_title().kill()
        self.get_play_button().kill()
        self.get_setting_button().kill()
        self.get_quit_button().kill()
        self.get_screen().fill((0, 0, 0))

    def render(self, time_delta) -> None:
        self.get_screen().blit(self.__GUIBackground, (0, 0))

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

    def get_quit_button_pressed(self) -> bool:
        return self.__quit_button_pressed

    def set_play_button_pressed(self, play_button_pressed: bool) -> None:
        self.__play_button_pressed = play_button_pressed

    def set_setting_button_pressed(self, setting_button_pressed: bool) -> None:
        self.__setting_button_pressed = setting_button_pressed

    def set_quit_button_pressed(self, quit_button_pressed: bool) -> None:
        self.__quit_button_pressed = quit_button_pressed

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

    def get_GUIBackground(self) -> pygame.Surface:
        return self.__GUIBackground

    def set_GUIBackground(self, GUIBackground: pygame.Surface) -> None:
        self.__GUIBackground = GUIBackground
