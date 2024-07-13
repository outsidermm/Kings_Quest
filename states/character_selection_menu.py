from .base_state import BaseState
from characters.base_character import BaseCharacter
import pygame, pygame_gui
from state_manager import GameStateManager
from characters.base_character import BaseCharacter


class CharacterSelectionMenu(BaseState):

    __characters: list[BaseCharacter] = None
    __selected_character: BaseCharacter = None
    __selection_page = 0

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        characters: list[BaseCharacter],
    ):
        super().__init__(screen, ui_manager, game_state_manager)
        self.__characters = characters
        self.__characater_count = len(characters)
        self.__characater_name_list = [character.get_name() for character in characters]

    def start(self) -> None:
        self.__character_picture_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (0, 0), (self.get_screen().height, self.get_screen().width * 0.6)
            ),
            manager=self.get_ui_manager(),
            anchors=({"left": "left"}),
        )

        right_info = pygame.Rect(
            (0, 0), (self.get_screen().width * 0.4, self.get_screen().height)
        )
        right_info.right = -30
        self.__character_info_panel = pygame_gui.elements.UIPanel(
            relative_rect=right_info,
            manager=self.get_ui_manager(),
            anchors=({"right": "right"}),
        )

        self.__character_name = pygame_gui.elements.UITextBox(
            "Character 1",
            relative_rect=pygame.Rect(
                (self.get_screen().height * 0.05, self.get_screen().width * 0.05),
                (150, 150),
            ),
            manager=self.get_ui_manager(),
            anchors=({"left": "left"}),
            container=self.__character_info_panel,
        )

        self.set_left_arrow_select(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (50, self.get_screen().height - 100), (150, 70)
                ),
                text="<-",
                manager=self.get_ui_manager(),
                anchors=({"left": "left"}),
                container=self.__character_picture_panel,
            )
        )

        self.set_right_arrow_select(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (-200, self.get_screen().height - 100), (150, 70)
                ),
                text="->",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                container=self.__character_info_panel,
            )
        )

    def handle_events(self, event: pygame.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.get_left_arrow_select():
                self.__left_switch_character = True
            if event.ui_element == self.get_right_arrow_select():
                self.__right_switch_character = True

    def run(self):
        if self.__left_switch_character:
            self.__selection_page = (
                self.__selection_page - 1
            ) % self.__characater_count
            self.__character_name.set_text(
                self.__characater_name_list[self.__selection_page]
            )
        elif self.__right_switch_character:
            self.__selection_page = (
                self.__selection_page + 1
            ) % self.__characater_count
            self.__character_name.set_text(
                self.__characater_name_list[self.__selection_page]
            )

    def reset_event_polling(self) -> None:
        self.__left_switch_character = False
        self.__right_switch_character = False

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

    def get_characters(self) -> list[BaseCharacter]:
        return self.__characters

    def set_characters(self, characters: list[BaseCharacter]) -> None:
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
