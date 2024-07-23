import pygame
import pygame_gui
from pygame.time import Clock
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
from characters.enemies.base_enemy import BaseEnemy
from characters.players.base_player import BasePlayer
from xp import XP
from quest import Quest
import json_utility


class Game:
    """
    Game class to initialize and run the game.
    """

    __game_state_manager: GameStateManager = None
    __clock: Clock = None
    __running: bool = True

    def __init__(self) -> None:
        """
        Initializes the game, sets up pygame, UI, and game states.
        """
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        screen = pygame.display.set_mode((1280, 720))

        ui_manager = pygame_gui.UIManager((1280, 720))

        # Load UI themes
        ui_manager.get_theme().load_theme("settings/general.json")
        ui_manager.get_theme().load_theme("settings/character_selection_theme.json")
        ui_manager.get_theme().load_theme("settings/level_selection_theme.json")
        ui_manager.get_theme().load_theme("settings/combat_theme.json")
        ui_manager.get_theme().load_theme("settings/health_bar.json")

        # Default user data
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

        players: list[BasePlayer] = [
            Warrior("assets/characters/players/warrior/idle/0.png"),
            Mage("assets/characters/players/mage/idle/0.png"),
            Berserker("assets/characters/players/berserker/idle/0.png"),
            Ranger("assets/characters/players/ranger/idle/0.png"),
        ]

        enemies: list[BaseEnemy] = [
            DreadNought("assets/characters/enemies/dreadnought/idle/0000.png"),
            Devourer("assets/characters/enemies/devourer/idle/0000.png"),
            Enigma("assets/characters/enemies/enigma/idle/0000.png"),
        ]

        xp = XP(json_utility.read_json("settings/user_settings.json")["xp"])
        quests: list[Quest] = [
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

        StartMenu(screen, ui_manager, self.get_game_state_manager())
        CharacterSelectionMenu(
            screen,
            ui_manager,
            self.get_game_state_manager(),
            players,
            xp,
        )
        LevelSelectionMenu(
            screen,
            ui_manager,
            self.get_game_state_manager(),
            enemies,
        )
        QuestMenu(
            screen,
            ui_manager,
            self.get_game_state_manager(),
            quests,
            xp,
        )
        TurnBasedFight(
            screen,
            ui_manager,
            self.get_game_state_manager(),
            quests,
            temp_quest=Quest(
                "Normal Attack",
                "use normal attack 10 times",
                10,
                1000,
                is_temporary=True,
            ),
        )
        EndMenu(
            screen,
            ui_manager,
            self.get_game_state_manager(),
            xp,
        )

        self.get_game_state_manager().set_initial_state("start_menu")

    def run(self) -> None:
        """
        Runs the main game loop.
        """
        while self.get_running():
            time_delta = self.get_clock().tick_busy_loop(60)
            self.set_running(self.get_game_state_manager().run(time_delta))

        pygame.quit()
        quit()

    def get_game_state_manager(self) -> GameStateManager:
        """
        Gets the game state manager.

        :return: The game state manager.
        """
        return self.__game_state_manager

    def set_game_state_manager(self, game_state_manager: GameStateManager) -> None:
        """
        Sets the game state manager.

        :param game_state_manager: The new game state manager.
        """
        self.__game_state_manager = game_state_manager

    def set_clock(self, clock: Clock) -> None:
        """
        Sets the game clock.

        :param clock: The new game clock.
        """
        self.__clock = clock

    def get_clock(self) -> Clock:
        """
        Gets the game clock.

        :return: The game clock.
        """
        return self.__clock

    def get_running(self) -> bool:
        """
        Checks if the game is running.

        :return: True if the game is running, False otherwise.
        """
        return self.__running

    def set_running(self, running: bool) -> None:
        """
        Sets the running status of the game.

        :param running: The new running status.
        """
        self.__running = running
