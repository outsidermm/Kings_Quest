import pygame
import pygame_gui
from state_manager import GameStateManager
from states.start_menu import StartMenu
from states.turn_based_fight_state import TurnBasedFight
from states.character_selection_menu import CharacterSelectionMenu
from characters.players.mage import Mage
from characters.players.ranger import Ranger
from characters.players.warrior import Warrior
from characters.players.berserker import Berserker
from characters.enemies.dreadnought import DreadNought
from characters.base_character import BaseCharacter


class Game:
    __screen = None
    __ui_manager = None
    __game_state_manager = None
    __clock = None
    __states = None
    __characters: list[BaseCharacter] = None

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

        self.get_ui_manager().get_theme().load_theme("settings/general.json")
        self.get_ui_manager().get_theme().load_theme(
            "settings/character_selection_theme.json"
        )
        self.get_ui_manager().get_theme().load_theme("settings/combat_theme.json")
        self.get_ui_manager().get_theme().load_theme("settings/health_bar.json")

        self.set_clock(pygame.time.Clock())

        self.set_game_state_manager(GameStateManager("start_menu"))

        self.set_characters(
            [
                Warrior("Aric", "assets/characters/aric/idle/0.png"),
                Mage("Lyra", "assets/characters/lyra/idle/0.png"),
                Berserker("Berserker", "assets/characters/berserker/idle/0.png"),
                Ranger("Ranger", "assets/characters/ranger/idle/0.png"),
            ]
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

        self.__turn_based_fight_state = TurnBasedFight(
            self.get_screen(),
            self.get_ui_manager(),
            self.get_game_state_manager(),
            self.get_characters()[0],
            DreadNought("DreadNought", "assets/characters/dreadnought/idle/0000.png"),
        )

        self.set_states(
            {
                "start_menu": self.get_start_menu(),
                "character_selection_menu": self.get_character_selection_menu(),
                "turn_based_fight": self.__turn_based_fight_state,
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
                    self.get_game_state_manager().get_state()[0]
                ].handle_events(event)

            self.get_states()[self.get_game_state_manager().get_state()[0]].run()
            if self.get_game_state_manager().get_state()[1]:
                self.get_ui_manager().clear_and_reset()
                self.get_states()[self.get_game_state_manager().get_state()[0]].start()
            self.get_states()[
                self.get_game_state_manager().get_state()[0]
            ].reset_event_polling()

            self.get_ui_manager().update(time_delta)

            self.get_states()[self.get_game_state_manager().get_state()[0]].render(
                time_delta
            )
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

    def get_characters(self) -> list[BaseCharacter]:
        return self.__characters

    def set_characters(self, characters: list[BaseCharacter]) -> None:
        self.__characters = characters

    def set_character_selection_menu(
        self, character_selection_menu: CharacterSelectionMenu
    ) -> None:
        self.__character_selection_menu = character_selection_menu

    def get_character_selection_menu(self) -> CharacterSelectionMenu:
        return self.__character_selection_menu
