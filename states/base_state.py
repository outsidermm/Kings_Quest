import abc
from state_manager import GameStateManager
import pygame
import pygame_gui


class BaseState(abc.ABC):
    """
    Abstract base class for game states. Provides a template for managing different states
    in the game, such as the main menu, in-game state, etc.

    Attributes:
        screen (pygame.Surface): The screen surface for rendering.
        game_state_manager (GameStateManager): Manages the transitions and state of the game.
        ui_manager (pygame_gui.UIManager): Manages UI elements for the state.
        target_state_name (str): The name of the target state to transition to.
        state_name (str): The name of the current state.
        outgoing_transition_data (dict): Data to pass to the next state during transition.
        incoming_transition_data (dict): Data received from the previous state during transition.
        time_to_quit_app (bool): Flag to indicate if it's time to quit the application.
        time_to_transition (bool): Flag to indicate if it's time to transition to another state.
    """

    def __init__(
        self,
        state_name: str,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        target_state_name: str,
        game_state_manager: GameStateManager,
    ) -> None:
        """
        Initializes the BaseState with necessary parameters and registers the state
        with the game state manager.

        :param state_name: The name of the current state.
        :param screen: The screen surface for rendering.
        :param ui_manager: The UI manager for handling UI elements.
        :param target_state_name: The name of the target state for transitions.
        :param game_state_manager: The manager for game states.
        """
        self.set_state_name(state_name)
        self.set_target_state_name(target_state_name)
        self.set_screen(screen)
        self.set_ui_manager(ui_manager)
        self.set_game_state_manager(game_state_manager)
        self.get_game_state_manager().register_state(self)

    def trigger_transition(self) -> None:
        """
        Triggers a transition to the target state.
        """
        self.set_time_to_transition(True)

    @abc.abstractmethod
    def start(self):
        """
        Abstract method to start the state. Must be implemented by subclasses.
        """
        pass

    @abc.abstractmethod
    def handle_events(self) -> None:
        """
        Abstract method to handle events. Must be implemented by subclasses.
        """
        pass

    @abc.abstractmethod
    def run(self) -> None:
        """
        Abstract method to run the state logic. Must be implemented by subclasses.
        """
        pass

    @abc.abstractmethod
    def render(self, time_delta: int) -> None:
        """
        Abstract method to render the state. Must be implemented by subclasses.

        :param time_delta: The time delta since the last frame.
        """
        pass

    @abc.abstractmethod
    def reset_event_polling(self) -> None:
        """
        Abstract method to reset event polling. Must be implemented by subclasses.
        """
        pass

    @abc.abstractmethod
    def end(self):
        """
        Abstract method to end the state. Must be implemented by subclasses.
        """
        pass

    def get_screen(self) -> pygame.Surface:
        """
        Gets the screen surface for rendering.

        :return: The screen surface.
        """
        return self.__screen

    def set_screen(self, screen: pygame.Surface) -> None:
        """
        Sets the screen surface for rendering.

        :param screen: The screen surface to set.
        """
        self.__screen = screen

    def get_game_state_manager(self) -> GameStateManager:
        """
        Gets the game state manager.

        :return: The game state manager.
        """
        return self.__game_state_manager

    def set_game_state_manager(self, game_state_manager: GameStateManager) -> None:
        """
        Sets the game state manager.

        :param game_state_manager: The game state manager to set.
        """
        self.__game_state_manager = game_state_manager

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

    def get_state_name(self) -> str:
        """
        Gets the name of the current state.

        :return: The name of the current state.
        """
        return self.__state_name

    def set_state_name(self, state_name: str) -> None:
        """
        Sets the name of the current state.

        :param state_name: The name of the current state to set.
        """
        self.__state_name = state_name

    def get_target_state_name(self) -> str:
        """
        Gets the name of the target state.

        :return: The name of the target state.
        """
        return self.__target_state_name

    def set_target_state_name(self, target_state_name: str) -> None:
        """
        Sets the name of the target state.

        :param target_state_name: The name of the target state to set.
        """
        self.__target_state_name = target_state_name

    def get_outgoing_transition_data(self) -> dict:
        """
        Gets the outgoing transition data.

        :return: The outgoing transition data.
        """
        return self.__outgoing_transition_data

    def set_outgoing_transition_data(self, outgoing_transition_data: dict) -> None:
        """
        Sets the outgoing transition data.

        :param outgoing_transition_data: The outgoing transition data to set.
        """
        self.__outgoing_transition_data = outgoing_transition_data

    def get_incoming_transition_data(self) -> dict:
        """
        Gets the incoming transition data.

        :return: The incoming transition data.
        """
        return self.__incoming_transition_data

    def set_incoming_transition_data(self, incoming_transition_data: dict) -> None:
        """
        Sets the incoming transition data.

        :param incoming_transition_data: The incoming transition data to set.
        """
        self.__incoming_transition_data = incoming_transition_data

    def set_time_to_quit_app(self, time_to_quit_app: bool) -> None:
        """
        Sets the flag indicating it's time to quit the application.

        :param time_to_quit_app: The flag to set.
        """
        self.__time_to_quit_app = time_to_quit_app

    def get_time_to_quit_app(self) -> bool:
        """
        Gets the flag indicating it's time to quit the application.

        :return: The flag indicating it's time to quit the application.
        """
        return self.__time_to_quit_app

    def set_time_to_transition(self, time_to_transition: bool) -> None:
        """
        Sets the flag indicating it's time to transition to another state.

        :param time_to_transition: The flag to set.
        """
        self.__time_to_transition = time_to_transition

    def get_time_to_transition(self) -> bool:
        """
        Gets the flag indicating it's time to transition to another state.

        :return: The flag indicating it's time to transition to another state.
        """
        return self.__time_to_transition