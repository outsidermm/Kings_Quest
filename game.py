import pygame
import pygame_gui
from state_manager import GameStateManager
from states.start_menu import StartMenu
from states.character_selection import CharacterSelectionMenu
from character import Character


class Game:
    __screen = None
    __ui_manager = None
    __game_state_manager = None
    __clock = None
    __states = None
    __characters: list[Character] = []

    __start_menu = None
    __character_selection_menu = None

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # TODO Shift to Setting file
        self.__SCREEN_WIDTH = 1280
        self.__SCREEN_HEIGHT = 720
        self.__FPS = 60

        self.set_screen(
            pygame.display.set_mode((self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))
        )
        self.set_ui_manager(
            pygame_gui.UIManager((self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))
        )

        self.get_ui_manager().get_theme().load_theme("./settings/menu_theme.json")

        self.set_clock(pygame.time.Clock())

        self.set_game_state_manager(GameStateManager("start_menu"))

        self.get_characters().append(
            [Character("i", {}, {}), Character("j", {}, {}), Character("k", {}, {})]
        )

        self.set_start_menu(
            StartMenu(
                self.get_screen(), self.get_ui_manager(), self.get_game_state_manager()
            )
        )

        self.set_character_selection_menu(
            CharacterSelectionMenu(
                self.get_screen(),
                self.get_ui_manager(),
                self.get_game_state_manager(),
                self.get_characters(),
            )
        )

        self.set_states(
            {
                "start_menu": self.get_start_menu(),
                "character_selection_menu": self.get_character_selection_menu(),
            }
        )

    def run(self) -> None:
        while True:
            time_delta = self.get_clock().tick_busy_loop(self.__FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.get_ui_manager().process_events(event)

                self.get_states()[
                    self.get_game_state_manager().get_state()
                ].handle_events(event)

            self.get_states()[self.get_game_state_manager().get_state()].run()
            self.get_states()[
                self.get_game_state_manager().get_state()
            ].reset_event_polling()

            self.get_ui_manager().update(time_delta)

            self.get_states()[self.get_game_state_manager().get_state()].render()
            self.get_screen().blit(
                pygame.Surface((self.__SCREEN_HEIGHT, self.__SCREEN_WIDTH)), (0, 0)
            )
            self.get_ui_manager().draw_ui(self.get_screen())
            pygame.display.update()

    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def get_ui_manager(self) -> pygame_gui.UIManager:
        return self.__ui_manager

    def get_game_state_manager(self) -> GameStateManager:
        return self.__game_state_manager

    def set_screen(self, screen: pygame.Surface) -> None:
        self.__screen = screen

    def set_ui_manager(self, ui_manager: pygame_gui.UIManager) -> None:
        self.__ui_manager = ui_manager

    def set_game_state_manager(self, game_state_manager: GameStateManager) -> None:
        self.__game_state_manager = game_state_manager

    def set_clock(self, clock: pygame.time.Clock) -> None:
        self.__clock = clock

    def get_clock(self) -> pygame.time.Clock:
        return self.__clock

    def set_states(self, states: dict) -> None:
        self.__states = states

    def get_states(self) -> dict:
        return self.__states

    def get_start_menu(self) -> StartMenu:
        return self.__start_menu

    def set_start_menu(self, start_menu: StartMenu) -> None:
        self.__start_menu = start_menu

    def get_characters(self) -> list[Character]:
        return self.__characters

    def set_characters(self, characters: list[Character]) -> None:
        self.__characters = characters

    def set_character_selection_menu(
        self, character_selection_menu: CharacterSelectionMenu
    ) -> None:
        self.__character_selection_menu = character_selection_menu

    def get_character_selection_menu(self) -> CharacterSelectionMenu:
        return self.__character_selection_menu
