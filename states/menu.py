from .base_state import State
from state_manager import GameStateManager
import pygame
import pygame_gui
import os


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
        self.screen_width = self.get_display().get_rect().width
        self.screen_height = self.get_display().get_rect().height

        self.__game_title = pygame_gui.elements.UITextBox("King's Quest", pygame.Rect((0,-self.screen_height*0.3), (1000, 200)), self.get_ui_manager(), anchors=({"center":"center"}), object_id=pygame_gui.core.ObjectID(class_id="@title",object_id="#game_title"))

        self.__play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (500, 70)),
            text="PLAY",
            manager=self.get_ui_manager(),
            anchors=({"center":"center"})
        )
        self.__setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0,self.screen_height*0.15), (500, 70)),
            text="SETTINGS",
            manager=self.get_ui_manager(),
            anchors=({"center":"center"})
        )

        self.__quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0,self.screen_height*0.3), (500, 70)),
            text="QUIT",
            manager=self.get_ui_manager(),
            anchors=({"center":"center"})
        )
        self.__GUIBackground = pygame.transform.scale(pygame.image.load(os.path.join("./assets/GUIBackground.png")).convert(), (self.screen_width, self.screen_height))
        self.get_display().blit(self.__GUIBackground, (0, 0))
    def handle_events(self,event) -> None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.__play_button:
                pass
            if event.ui_element == self.__setting_button:
                pass
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