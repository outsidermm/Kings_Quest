from states.base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from characters.enemies.base_enemy import BaseEnemy
from xp import XP


class LevelSelectionMenu(BaseState):

    __enemies: list[BaseEnemy] = None
    __game_start: bool = False
    __ability_menu_active: bool = False
    __quit_button_pressed: bool = False
    __show_enemy_info: int = -1
    __enemy_buttons: list[UIButton] = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        enemies: list[BaseEnemy],
        xp: XP = None,
    ):
        super().__init__(
            "level_selection_menu",
            screen,
            ui_manager,
            "turn_based_fight",
            game_state_manager,
        )
        self.__enemies = enemies
        self.__enemy_buttons = [None] * len(self.__enemies)
        

    def start(self) -> None:
        enemy_button_width = enemy_button_height= 200
        enemy_button_gap = (
            self.get_screen().get_width() - enemy_button_width * len(self.__enemies)
        ) / (len(self.__enemies) + 1)
        for enemy_button_count, enemy in enumerate(self.__enemies):
            self.__enemy_buttons[enemy_button_count] = UIButton(
                relative_rect=pygame.Rect(
                    (
                        enemy_button_gap * (enemy_button_count + 1)
                        + enemy_button_width * enemy_button_count,0
                    ),
                    (enemy_button_width, enemy_button_height),
                ),
                text=f"{enemy_button_count+1}: {enemy.get_name()}",
                anchors=({"centery": "centery"}),
                manager=self.get_ui_manager(),
            )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_button_pressed = True
            self.get_ui_manager().process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for enemy_button_index in range(len(self.__enemies)):
                    if event.ui_element == self.__enemy_buttons[enemy_button_index]:
                        self.__show_enemy_info = enemy_button_index

    def run(self) -> None:
        if self.__quit_button_pressed:
            self.set_time_to_quit_app(True)
            return

        if self.__game_start:
            self.set_time_to_transition(True)
            return

        print( self.__show_enemy_info)
        if self.__show_enemy_info != -1:
            pass

    def render(self, time_delta: int) -> None:
        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(
            pygame.Surface((self.get_screen().width, self.get_screen().height)), (0, 0)
        )
        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        self.__quit_button_pressed = False
        self.__show_enemy_info = -1

    def end(self) -> None:
        self.get_screen().fill((0, 0, 0))

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

    def set_time_to_quit_app(self, time_to_quit_app: bool) -> None:
        super().set_time_to_quit_app(time_to_quit_app)

    def get_time_to_quit_app(self) -> bool:
        return super().get_time_to_quit_app()

    def set_time_to_transition(self, time_to_transition: bool) -> None:
        super().set_time_to_transition(time_to_transition)

    def get_time_to_transition(self) -> bool:
        return super().get_time_to_transition()
