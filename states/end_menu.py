from states.base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UITextBox
from pygame_gui.core import ObjectID
from xp import XP
import random


class EndMenu(BaseState):
    __background_image: pygame.Surface = None
    __navigate_start_menu_button: UIButton = None
    __navigate_start_menu: bool = False
    __xp: XP = None
    __game_heading: UITextBox = None
    __game_description: UITextBox = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        xp: XP,
    ):
        super().__init__(
            "end_menu",
            screen,
            ui_manager,
            "start_menu",
            game_state_manager,
        )
        self.__xp = xp

    def start(self) -> None:
        self.set_outgoing_transition_data(self.get_incoming_transition_data())

        self.__background_image = pygame.transform.scale(
            pygame.image.load("assets/background_image.png"),
            (self.get_screen().width, self.get_screen().height),
        )

        xp_won = random.randint(100, 300)
        xp_quest = random.randint(100, 300)
        self.__game_heading = UITextBox(
            "You Won!",
            pygame.Rect((0, -self.get_screen().height * 0.3), (1000, 200)),
            self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@title", object_id="#game_title"),
        )

        self.__game_description = UITextBox(
            f"You have gained {xp_won} XP!",
            pygame.Rect((0, 300), (400, -1)),
            self.get_ui_manager(),
            anchors=({"centerx": "centerx"}),
            object_id=ObjectID(class_id="#enemy_statistic"),
        )
        if self.get_incoming_transition_data()["winner"] == "enemy":
            self.__game_heading.set_text("You Lost!")
            if "temp_quest_completion" in self.get_incoming_transition_data().keys():
                self.__game_description.set_text(
                    f"Better luck next time!\nHowever, you did complete the quest.\nYou earned {xp_quest} XP!"
                )
                self.__xp.gain_xp(xp_quest)
            else:
                self.__game_description.set_text(
                    f"Better luck next time!\nYou also failed the quest master's quest!"
                )
        else:
            self.__xp.gain_xp(xp_won)
            if "temp_quest_completion" in self.get_incoming_transition_data().keys():
                self.__game_description.set_text(
                    f"You have gained {xp_won} XP for beating the boss!\nAlso, you did complete the quest.\nYou earned an addition {xp_quest} XP!"
                )
                self.__xp.gain_xp(xp_quest)
            else:
                self.__game_description.set_text(
                    f"You have gained {xp_won} XP for beating the boss!\nUnforunately, you did fail the quest master's quest!"
                )

        outgoing_dict_without_winner_key = self.get_incoming_transition_data()
        del outgoing_dict_without_winner_key["winner"]
        if "temp_quest_completion" in outgoing_dict_without_winner_key.keys():
            del outgoing_dict_without_winner_key["temp_quest_completion"]
        self.set_outgoing_transition_data(outgoing_dict_without_winner_key)

        self.__navigate_start_menu_button = UIButton(
            relative_rect=pygame.Rect((0, 175), (400, 75)),
            text="RETURN TO START MENU",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@level_selection_button"),
        )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_time_to_quit_app(True)
            self.get_ui_manager().process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__navigate_start_menu_button:
                    self.__navigate_start_menu = True

    def run(self) -> None:
        if self.__navigate_start_menu:
            outgoing_dict_without_character_keys = self.get_outgoing_transition_data()
            del outgoing_dict_without_character_keys["player"]
            del outgoing_dict_without_character_keys["enemy"]
            self.set_outgoing_transition_data(outgoing_dict_without_character_keys)
            self.set_time_to_transition(True)
            return

    def render(self, time_delta: int) -> None:

        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(self.__background_image, (0, 0))

        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        self.__navigate_start_menu = False

    def end(self) -> None:
        self.__game_description.kill()
        self.__game_heading.kill()
        self.__navigate_start_menu_button.kill()
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

    def set_target_state_name(self, target_state_name: str) -> None:
        super().set_target_state_name(target_state_name)

    def get_target_state_name(self) -> str:
        return super().get_target_state_name()
