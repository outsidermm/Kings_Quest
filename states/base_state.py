import abc
from state_manager import GameStateManager
import pygame
import pygame_gui


class BaseState(abc.ABC):
    __screen = None
    __game_state_manager: GameStateManager = None
    __ui_manager = None
    __target_state_name: str = None
    __state_name: str = None
    __outgoing_transition_data = {}
    __incoming_transition_data = {}
    __time_to_quit_app: bool = False
    __time_to_transition: bool = False

    def __init__(
        self,
        state_name: str,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        target_state_name: str,
        game_state_manager: GameStateManager,
    ) -> None:
        self.__state_name = state_name
        self.__target_state_name = target_state_name
        self.set_screen(screen)
        self.set_ui_manager(ui_manager)
        self.set_game_state_manager(game_state_manager)
        self.get_game_state_manager().register_state(self)

    def set_target_state_name(self, target_name):
        self.__target_state_name = target_name

    def trigger_transition(self):
        self.time_to_transition = True

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def handle_events(self) -> None:
        pass

    @abc.abstractmethod
    def run(self) -> None:
        pass

    @abc.abstractmethod
    def render(self, time_delta: int) -> None:
        pass

    @abc.abstractmethod
    def reset_event_polling(self) -> None:
        pass

    @abc.abstractmethod
    def end(self):
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

    def get_state_name(self) -> str:
        return self.__state_name

    def set_state_name(self, state_name: str) -> None:
        self.__state_name = state_name

    def get_target_state_name(self) -> str:
        return self.__target_state_name

    def set_target_state_name(self, target_state_name: str) -> None:
        self.__target_state_name = target_state_name

    def get_outgoing_transition_data(self) -> dict:
        return self.__outgoing_transition_data

    def set_outgoing_transition_data(self, outgoing_transition_data: dict) -> None:
        self.__outgoing_transition_data = outgoing_transition_data

    def get_incoming_transition_data(self) -> dict:
        return self.__incoming_transition_data

    def set_incoming_transition_data(self, incoming_transition_data: dict) -> None:
        self.__incoming_transition_data = incoming_transition_data

    def set_time_to_quit_app(self, time_to_quit_app: bool) -> None:
        self.__time_to_quit_app = time_to_quit_app

    def get_time_to_quit_app(self) -> bool:
        return self.__time_to_quit_app

    def set_time_to_transition(self, time_to_transition: bool) -> None:
        self.__time_to_transition = time_to_transition

    def get_time_to_transition(self) -> bool:
        return self.__time_to_transition
