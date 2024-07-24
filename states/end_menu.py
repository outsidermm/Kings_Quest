from states.base_state import BaseState
from state_manager import GameStateManager
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextBox
from pygame_gui.core import ObjectID
from xp import XP
import random


class EndMenu(BaseState):
    """
    EndMenu class to display the end of game screen, showing the result and earned XP.
    """

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
        """
        Initializes the EndMenu class.

        :param screen: The game screen surface.
        :param ui_manager: The UI manager for pygame_gui.
        :param game_state_manager: The game state manager.
        :param xp: The XP object for managing experience points.
        """
        super().__init__(
            "end_menu",
            screen,
            ui_manager,
            "start_menu",
            game_state_manager,
        )
        self.set_xp(xp)

    def start(self) -> None:
        """
        Starts the end menu by setting up UI elements and background image.
        """
        # Set the outgoing transition data to be the same as the incoming transition data
        self.set_outgoing_transition_data(self.get_incoming_transition_data())

        # Load and scale the background image to fit the screen size
        self.set_background_image(
            pygame.transform.scale(
                pygame.image.load("assets/background_image.png"),
                (self.get_screen().get_width(), self.get_screen().get_height()),
            )
        )

        # Generate random XP values for winning the game and completing the quest
        xp_won = random.randint(100, 300)
        xp_quest = random.randint(100, 300)

        # Create the game heading text box, initially setting it to "You Won!"
        self.set_game_heading(
            UITextBox(
                "You Won!",
                pygame.Rect((0, -self.get_screen().get_height() * 0.3), (1000, 200)),
                self.get_ui_manager(),
                anchors=({"center": "center"}),
                object_id=ObjectID(class_id="@title", object_id="#game_title"),
            )
        )

        # Create the game description text box, displaying the amount of XP won
        self.set_game_description(
            UITextBox(
                f"You have gained {xp_won} XP!",
                pygame.Rect((0, 300), (400, -1)),
                self.get_ui_manager(),
                anchors=({"centerx": "centerx"}),
                object_id=ObjectID(class_id="#enemy_statistic"),
            )
        )

        # Check the winner from the incoming transition data
        if self.get_incoming_transition_data()["winner"] == "enemy":
            # If the enemy won, update the heading to "You Lost!"
            self.get_game_heading().set_text("You Lost!")
            
            # Check if the quest was completed
            if "temp_quest_completion" in self.get_incoming_transition_data().keys():
                # If the quest was completed, update the description and add quest XP
                self.get_game_description().set_text(
                    f"Better luck next time!\nHowever, you did complete the quest.\nYou earned {xp_quest} XP!"
                )
                self.get_xp().gain_xp(xp_quest)
            else:
                # If the quest was not completed, update the description accordingly
                self.get_game_description().set_text(
                    f"Better luck next time!\nYou also failed the quest master's quest!"
                )
        else:
            # If the player won, add the XP won to the player's total XP
            self.get_xp().gain_xp(xp_won)
            
            # Check if the quest was completed
            if "temp_quest_completion" in self.get_incoming_transition_data().keys():
                # If the quest was completed, update the description and add quest XP
                self.get_game_description().set_text(
                    f"You have gained {xp_won} XP for beating the boss!\nAlso, you did complete the quest.\nYou earned an additional {xp_quest} XP!"
                )
                self.get_xp().gain_xp(xp_quest)
            else:
                # If the quest was not completed, update the description accordingly
                self.get_game_description().set_text(
                    f"You have gained {xp_won} XP for beating the boss!\nUnfortunately, you did fail the quest master's quest!"
                )

        # Prepare outgoing transition data by removing "winner" and "temp_quest_completion" keys
        outgoing_dict_without_winner_key = self.get_incoming_transition_data()
        del outgoing_dict_without_winner_key["winner"]
        if "temp_quest_completion" in outgoing_dict_without_winner_key.keys():
            del outgoing_dict_without_winner_key["temp_quest_completion"]
        self.set_outgoing_transition_data(outgoing_dict_without_winner_key)

        # Create the button to navigate back to the start menu
        self.set_navigate_start_menu_button(
            UIButton(
                relative_rect=pygame.Rect((0, 175), (400, 75)),
                text="RETURN TO START MENU",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                object_id=ObjectID(class_id="@level_selection_button"),
            )
        )
        
        
    def handle_events(self) -> None:
        """
        Handles events such as button presses and quitting the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_time_to_quit_app(True)
            self.get_ui_manager().process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.get_navigate_start_menu_button():
                    self.set_navigate_start_menu(True)

    def run(self) -> None:
        """
        Runs the logic for the end menu, such as navigating to the start menu.
        """
        if self.get_navigate_start_menu():
            # Retrieve the current outgoing transition data
            outgoing_dict_without_character_keys = self.get_outgoing_transition_data()
            
            # Remove the "player" and "enemy" keys from the transition data
            del outgoing_dict_without_character_keys["player"]
            del outgoing_dict_without_character_keys["enemy"]
            
            # Set the updated transition data without the "player" and "enemy" keys
            self.set_outgoing_transition_data(outgoing_dict_without_character_keys)
            
            # Indicate that it's time to transition to the next state
            self.set_time_to_transition(True)
            return

    def render(self, time_delta: int) -> None:
        """
        Renders the end menu screen.

        :param time_delta: Time elapsed since the last frame.
        """
        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(self.get_background_image(), (0, 0))
        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        """
        Resets the event polling flags.
        """
        self.set_navigate_start_menu(False)

    def end(self) -> None:
        """
        Ends the end menu by killing all UI elements.
        """
        self.get_game_description().kill()
        self.get_game_heading().kill()
        self.get_navigate_start_menu_button().kill()
        self.get_screen().fill((0, 0, 0))

    # Getters and setters

    def get_background_image(self) -> pygame.Surface:
        return self.__background_image

    def set_background_image(self, background_image: pygame.Surface) -> None:
        self.__background_image = background_image

    def get_navigate_start_menu_button(self) -> UIButton:
        return self.__navigate_start_menu_button

    def set_navigate_start_menu_button(self, button: UIButton) -> None:
        self.__navigate_start_menu_button = button

    def get_navigate_start_menu(self) -> bool:
        return self.__navigate_start_menu

    def set_navigate_start_menu(self, navigate: bool) -> None:
        self.__navigate_start_menu = navigate

    def get_xp(self) -> XP:
        return self.__xp

    def set_xp(self, xp: XP) -> None:
        self.__xp = xp

    def get_game_heading(self) -> UITextBox:
        return self.__game_heading

    def set_game_heading(self, game_heading: UITextBox) -> None:
        self.__game_heading = game_heading

    def get_game_description(self) -> UITextBox:
        return self.__game_description

    def set_game_description(self, game_description: UITextBox) -> None:
        self.__game_description = game_description

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
