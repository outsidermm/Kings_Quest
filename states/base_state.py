import abc
from state_manager import GameStateManager
import pygame
import pygame_gui


class State(abc.ABC):
    __screen = None
    __game_state_manager = None
    __ui_manager = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
    ) -> None:
        self.set_screen(screen)
        self.set_ui_manager(ui_manager)
        self.set_game_state_manager(game_state_manager)

    @abc.abstractmethod
    def handle_events(self, event: pygame.Event) -> None:
        pass

    @abc.abstractmethod
    def run(self) -> None:
        pass

    @abc.abstractmethod
    def reset_event_polling(self) -> None:
        pass

    @abc.abstractmethod
    def render(self) -> None:
        pass

    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen

    def get_game_state_manager(self) -> GameStateManager:
        return self.__game_state_manager

    def set_game_state_manager(self, game_state_manager: GameStateManager) -> None:
        self.__game_state_manager = game_state_manager

    def get_ui_manager(self) -> pygame_gui.UIManager:
        return self.__ui_manager

    def set_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        self.__ui_manager = ui_manager
