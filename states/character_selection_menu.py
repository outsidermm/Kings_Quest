from .base_state import BaseState
from character import Character
import pygame, pygame_gui
from state_manager import GameStateManager


class CharacterSelectionMenu(BaseState):

    __characters: list[Character] = None
    __selected_character: Character = None
    __selection_page = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        characters: list[Character],
    ):
        super().__init__(screen, ui_manager, game_state_manager)
        self.__characters = characters

    def start(self)->None:
        self.set_right_arrow_select(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (-200, self.get_screen().height - 100), (150, 70)
                ),
                text="->",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
            )
        )

        self.set_left_arrow_select(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (50, self.get_screen().height - 100), (150, 70)
                ),
                text="<-",
                manager=self.get_ui_manager(),
                anchors=({"left": "left"}),
            )
        )
        
    def handle_events(self, event: pygame.Event):
        pass

    def run(self):
        pass

    def reset_event_polling(self):
        pass

    def render(self):
        pass

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

    def get_characters(self) -> list[Character]:
        return self.__characters

    def set_characters(self, characters: list[Character]) -> None:
        self.__characters = characters

    def get_right_arrow_select(self) -> pygame_gui.elements.UIButton:
        return self.__right_arrow_select

    def set_right_arrow_select(
        self, right_arrow_select: pygame_gui.elements.UIButton
    ) -> None:
        self.__right_arrow_select = right_arrow_select

    def get_left_arrow_select(self) -> pygame_gui.elements.UIButton:
        return self.__left_arrow_select

    def set_left_arrow_select(
        self, left_arrow_select: pygame_gui.elements.UIButton
    ) -> None:
        self.__left_arrow_select = left_arrow_select
