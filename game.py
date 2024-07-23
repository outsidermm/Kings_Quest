import pygame
import pygame_gui
from state_manager import GameStateManager
from states.start_menu import StartMenu
from states.turn_based_fight_state import TurnBasedFight
from states.character_selection_menu import CharacterSelectionMenu
from states.level_selection_menu import LevelSelectionMenu
from states.quest_menu import QuestMenu
from states.end_menu import EndMenu
from characters.players.mage import Mage
from characters.players.ranger import Ranger
from characters.players.warrior import Warrior
from characters.players.berserker import Berserker
from characters.enemies.dreadnought import DreadNought
from characters.enemies.devourer import Devourer
from characters.enemies.enigma import Enigma
from characters.base_character import BaseCharacter
from characters.enemies.base_enemy import BaseEnemy
from xp import XP
from quest import Quest
import json_utility


class Game:
    __screen = None
    __ui_manager = None
    __game_state_manager = None
    __clock = None
    __states = None
    __characters: list[BaseCharacter] = None
    __enemies: list[BaseEnemy] = None

    __start_menu = None
    __character_selection_menu = None
    __running: bool = True

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
        self.get_ui_manager().get_theme().load_theme(
            "settings/level_selection_theme.json"
        )
        self.get_ui_manager().get_theme().load_theme("settings/combat_theme.json")
        self.get_ui_manager().get_theme().load_theme("settings/health_bar.json")

        default_user_data = {
            "xp": 5000,
            "quest_progress": {
                "Fireball": 0,
                "Kill DreadNoughts": 0,
            },
            "quest_claimed": {
                "Fireball": False,
                "Kill DreadNoughts": False,
            },
            "character_level": {
                "Warrior": 1,
                "Mage": 1,
                "Berserker": 1,
                "Ranger": 1,
            },
            "character_abilities": {
                "Warrior": ["Power Slash"],
                "Mage": ["Fireball"],
                "Berserker": ["Reckless Charge"],
                "Ranger": ["Arrow Barrage"],
            },
        }
        json_utility.write_default_if_not_exist(
            "settings/user_settings.json", default_data=default_user_data
        )

        self.set_clock(pygame.time.Clock())

        self.set_game_state_manager(GameStateManager())

        self.set_characters(
            [
                Warrior("assets/characters/players/warrior/idle/0.png"),
                Mage("assets/characters/players/mage/idle/0.png"),
                Berserker("assets/characters/players/berserker/idle/0.png"),
                Ranger("assets/characters/players/ranger/idle/0.png"),
            ]
        )
        self.__enemies = [
            DreadNought("assets/characters/enemies/dreadnought/idle/0000.png"),
            Devourer("assets/characters/enemies/devourer/idle/0000.png"),
            Enigma("assets/characters/enemies/enigma/idle/0000.png"),
        ]

        self.__xp = XP(json_utility.read_json("settings/user_settings.json")["xp"])
        self.__quests = [
            Quest(
                "Fireball",
                "Cast 10 Fireballs",
                10,
                1000,
            ),
            Quest(
                "Kill DreadNoughts",
                "Kill 5 DreadNoughts",
                5,
                2000,
            ),
        ]
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
                xp=self.__xp,
            )
        )
        self.level_selection_menu = LevelSelectionMenu(
            self.get_screen(),
            self.get_ui_manager(),
            self.get_game_state_manager(),
            self.__enemies,
        )

        self.quest_menu = QuestMenu(
            self.get_screen(),
            self.get_ui_manager(),
            self.get_game_state_manager(),
            quests=self.__quests,
            xp=self.__xp,
        )

        self.__turn_based_fight_state = TurnBasedFight(
            self.get_screen(),
            self.get_ui_manager(),
            self.get_game_state_manager(),
            quests=self.__quests,
        )

        self.__end_menu = EndMenu(
            self.get_screen(),
            self.get_ui_manager(),
            self.get_game_state_manager(),
            xp=self.__xp,
        )

        self.get_game_state_manager().set_initial_state("start_menu")

    def run(self) -> None:
        while self.__running:
            time_delta = self.get_clock().tick_busy_loop(self.__FPS)
            self.__running = self.get_game_state_manager().run(time_delta)

        pygame.quit()
        quit()

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
