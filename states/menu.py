from .base_state import State
from state_manager import GameStateManager
import pygame
import pygame_gui


class Menu(State):
    __display = None
    __game_state_manager = None
    __ui_manager = None

    def __init__(
        self,
        display: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
    ) -> None:
        super().__init__(display, ui_manager, game_state_manager)
        self.__play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text="PLAY",
            manager=self.get_ui_manager(),
        )
        self.__setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((600, 275), (100, 50)),
            text="SETTINGS",
            manager=self.get_ui_manager(),
        )

        self.__quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((800, 275), (100, 50)),
            text="QUIT",
            manager=self.get_ui_manager(),
        )

    def handle_events(self,event) -> None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.__play_button:
                print("hello")
            if event.ui_element == self.__setting_button:
                print("hello")
            if event.ui_element == self.__quit_button:
                pygame.quit()
                quit()

    def run(self) -> None:
        pass

    def render(self) -> None:
        pass

    def get_screen(self) -> pygame.Surface:
        return super().get_display()
    
    def set_screen(self, screen: pygame.Surface) -> None:
        super().set_display(screen)
    
    def get_ui_manager(self) -> pygame_gui.UIManager:
        return super().get_ui_manager()
    
    def set_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        super().set_ui_manager(ui_manager)

    def get_game_state_manager(self) -> GameStateManager:
        return super().get_game_state_manager()

    def set_game_state_manager(self, game_state_manager: GameStateManager) -> None:
        super().set_game_state_manager(game_state_manager)