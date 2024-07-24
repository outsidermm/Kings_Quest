from states.base_state import BaseState
from state_manager import GameStateManager
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from xp import XP
from quest import Quest


class QuestMenu(BaseState):
    __quests: list[Quest] = []
    __show_quest_info: int = -1
    __quest_buttons: list[UIButton] = []
    __background_image: pygame.Surface = None
    __navigate_lvl_selection_button: UIButton = None
    __navigate_lvl_selection: bool = False
    __exit_quest_button: UIButton = None
    __quest_overview: UIPanel = None
    __static_panel_wrapper: UIPanel = None
    __quest_name: UITextBox = None
    __quest_description: UITextBox = None
    __claim_quest_button: UIButton = None
    __claim_quest: bool = False
    __xp: XP = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        quests: list[Quest],
        xp: XP,
    ):
        """
        Initializes the QuestMenu class.

        :param screen: The game screen.
        :param ui_manager: The UI manager.
        :param game_state_manager: The game state manager.
        :param quests: The list of quests.
        :param xp: The player's XP.
        """
        super().__init__(
            "quest_menu",
            screen,
            ui_manager,
            "level_selection_menu",
            game_state_manager,
        )
        self.set_quests(quests)
        self.set_quest_buttons([None] * len(quests))
        self.set_xp(xp)

    def start(self) -> None:
        """
        Starts the quest menu by setting up UI elements and background image.
        """
        # Set outgoing transition data from incoming transition data
        self.set_outgoing_transition_data(self.get_incoming_transition_data())

        # Load and set the background image for the quest menu
        self.set_background_image(
            pygame.transform.scale(
                pygame.image.load("assets/background_image.png"),
                (self.get_screen().get_width(), self.get_screen().get_height()),
            )
        )

        # Create and set the main static panel wrapper
        self.set_static_panel_wrapper(
            UIPanel(
                pygame.Rect((0, 0), (self.get_screen().get_width(), self.get_screen().get_height())),
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#transparent_panel"),
            )
        )

        # Create and set the title text box
        UITextBox(
            "Quests",
            pygame.Rect((0, -self.get_screen().get_height() * 0.3), (1000, 200)),
            self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@title", object_id="#game_title"),
            container=self.get_static_panel_wrapper(),
        )

        # Create and set the "Level Selection" navigation button
        navigate_lvl_selection_button_rect = pygame.Rect((75, 0), (300, 100))
        navigate_lvl_selection_button_rect.bottom = -75
        self.set_navigate_lvl_selection_button(
            UIButton(
                relative_rect=navigate_lvl_selection_button_rect,
                text="← Level Selection",
                manager=self.get_ui_manager(),
                anchors=({"bottom": "bottom"}),
                object_id=ObjectID(class_id="@level_selection_button"),
                container=self.get_static_panel_wrapper(),
            )
        )

        # Calculate the dimensions and position for quest buttons
        quest_button_width = 300
        quest_button_height = 200
        quest_button_gap = (
            self.get_screen().get_width() - quest_button_width * len(self.get_quests())
        ) / (len(self.get_quests()) + 1)
        
        # Create and set quest buttons for each quest
        for quest_button_count, quest in enumerate(self.get_quests()):
            self.get_quest_buttons()[quest_button_count] = UIButton(
                relative_rect=pygame.Rect(
                    (
                        quest_button_gap * (quest_button_count + 1)
                        + quest_button_width * quest_button_count,
                        0,
                    ),
                    (quest_button_width, quest_button_height),
                ),
                text=f"{quest_button_count + 1}: {quest.get_name()}",
                anchors=({"centery": "centery"}),
                manager=self.get_ui_manager(),
                object_id=ObjectID(class_id="@level_selection_button"),
                container=self.get_static_panel_wrapper(),
            )
            # Disable the button if the quest is already claimed
            if quest.get_is_claimed():
                self.get_quest_buttons()[quest_button_count].set_text("CLAIMED")
                self.get_quest_buttons()[quest_button_count].disable()

        # Create and set the quest overview panel
        self.set_quest_overview(
            UIPanel(
                pygame.Rect(
                    (0, 0), (self.get_screen().get_width() * 0.4, self.get_screen().get_height() * 0.7)
                ),
                manager=self.get_ui_manager(),
                starting_height=2,
                anchors=({"center": "center"}),
                object_id=ObjectID(class_id="@ability_menu"),
                visible=False,
            )
        )

        # Create and set the quest name text box
        self.set_quest_name(
            UITextBox(
                self.get_quests()[0].get_name(),
                pygame.Rect((0, 25), (300, 75)),
                self.get_ui_manager(),
                container=self.get_quest_overview(),
                anchors=({"centerx": "centerx"}),
                object_id=ObjectID(class_id="@level_selection_text"),
            )
        )

        # Create and set the quest description text box
        self.set_quest_description(
            UITextBox(
                f"{self.get_quests()[0].get_description()}\n Current Progress: {self.get_quests()[0].get_progress()}/{self.get_quests()[0].get_aim()}\nReward: {self.get_quests()[0].get_reward()} XP",
                pygame.Rect((0, 100), (400, -1)),
                self.get_ui_manager(),
                container=self.get_quest_overview(),
                anchors=({"centerx": "centerx"}),
                object_id=ObjectID(class_id="#enemy_statistic"),
            )
        )

        # Create and set the "Claim" quest button
        self.set_claim_quest_button(
            UIButton(
                relative_rect=pygame.Rect((0, 75), (300, 50)),
                text="CLAIM",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                container=self.get_quest_overview(),
                object_id=ObjectID(class_id="@level_selection_button"),
            )
        )

        # Create and set the "Cancel" quest button
        self.set_exit_quest_button(
            UIButton(
                relative_rect=pygame.Rect((0, 175), (300, 50)),
                text="CANCEL",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                container=self.get_quest_overview(),
                object_id=ObjectID(class_id="@level_selection_button"),
            )
        )
        
    def handle_events(self) -> None:
        """
        Handles events such as button presses and quitting the game.
        """
        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                self.set_time_to_quit_app(True)
            self.get_ui_manager().process_events(event)

            # Handle button press events
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.get_navigate_lvl_selection_button():
                    self.set_navigate_lvl_selection(True)
                if event.ui_element == self.get_claim_quest_button():
                    self.set_claim_quest(True)
                if event.ui_element == self.get_exit_quest_button():
                    self.set_show_quest_info(-1)
                # Determine which quest button was pressed
                for quest_button_index in range(len(self.get_quests())):
                    if event.ui_element == self.get_quest_buttons()[quest_button_index]:
                        self.set_show_quest_info(quest_button_index)

    def run(self) -> None:
        """
        Runs the logic for the quest menu, such as navigating to the level selection
        or claiming quests.
        """
        # Navigate to the level selection menu
        if self.get_navigate_lvl_selection():
            self.set_target_state_name("level_selection_menu")
            self.set_time_to_transition(True)
            return

        # Claim the quest reward
        if self.get_claim_quest():
            self.get_xp().gain_xp(self.get_quests()[self.get_show_quest_info()].get_reward())
            self.get_quest_buttons()[self.get_show_quest_info()].set_text("CLAIMED")
            self.get_quests()[self.get_show_quest_info()].claim()
            self.get_quest_buttons()[self.get_show_quest_info()].disable()
            self.set_show_quest_info(-1)

    def render(self, time_delta: int) -> None:
        """
        Renders the quest menu, including the quest overview and static panels.

        :param time_delta: Time elapsed since the last frame.
        """
        # Show quest details if a quest is selected
        if self.get_show_quest_info() != -1:
            self.get_quest_name().set_text(self.get_quests()[self.get_show_quest_info()].get_name())
            self.get_quest_description().set_text(
                f"{self.get_quests()[self.get_show_quest_info()].get_description()}\n Current Progress: {self.get_quests()[self.get_show_quest_info()].get_progress()}/{self.get_quests()[self.get_show_quest_info()].get_aim()}\nReward: {self.get_quests()[self.get_show_quest_info()].get_reward()} XP",
            )
            # Show claim button if quest is done
            if self.get_quests()[self.get_show_quest_info()].is_done():
                self.get_claim_quest_button().show()
            else:
                self.get_claim_quest_button().hide()
            self.get_quest_overview().show()
            self.get_static_panel_wrapper().hide()
        else:
            self.get_quest_overview().hide()
            self.get_static_panel_wrapper().show()

        # Update and render UI elements
        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(self.get_background_image(), (0, 0))
        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        """
        Resets the event polling flags.
        """
        self.set_navigate_lvl_selection(False)
        self.set_claim_quest(False)

    def end(self) -> None:
        """
        Ends the quest menu by killing all UI elements.
        """
        # Kill all quest buttons
        [button.kill() for button in self.get_quest_buttons()]
        # Kill the other UI elements
        self.get_navigate_lvl_selection_button().kill()
        self.get_claim_quest_button().kill()
        self.get_exit_quest_button().kill()
        self.get_quest_overview().kill()
        self.get_static_panel_wrapper().kill()
        self.get_quest_name().kill()
        self.get_quest_description().kill()
        # Clear the screen
        self.get_screen().fill((0, 0, 0))

    # Getters and setters
    def get_quests(self) -> list[Quest]:
        return self.__quests

    def set_quests(self, quests: list[Quest]) -> None:
        self.__quests = quests

    def get_show_quest_info(self) -> int:
        return self.__show_quest_info

    def set_show_quest_info(self, show_quest_info: int) -> None:
        self.__show_quest_info = show_quest_info

    def get_quest_buttons(self) -> list[UIButton]:
        return self.__quest_buttons

    def set_quest_buttons(self, quest_buttons: list[UIButton]) -> None:
        self.__quest_buttons = quest_buttons

    def get_background_image(self) -> pygame.Surface:
        return self.__background_image

    def set_background_image(self, background_image: pygame.Surface) -> None:
        self.__background_image = background_image

    def get_navigate_lvl_selection_button(self) -> UIButton:
        return self.__navigate_lvl_selection_button

    def set_navigate_lvl_selection_button(self, navigate_lvl_selection_button: UIButton) -> None:
        self.__navigate_lvl_selection_button = navigate_lvl_selection_button

    def get_navigate_lvl_selection(self) -> bool:
        return self.__navigate_lvl_selection

    def set_navigate_lvl_selection(self, navigate_lvl_selection: bool) -> None:
        self.__navigate_lvl_selection = navigate_lvl_selection

    def get_exit_quest_button(self) -> UIButton:
        return self.__exit_quest_button

    def set_exit_quest_button(self, exit_quest_button: UIButton) -> None:
        self.__exit_quest_button = exit_quest_button

    def get_quest_overview(self) -> UIPanel:
        return self.__quest_overview

    def set_quest_overview(self, quest_overview: UIPanel) -> None:
        self.__quest_overview = quest_overview

    def get_static_panel_wrapper(self) -> UIPanel:
        return self.__static_panel_wrapper

    def set_static_panel_wrapper(self, static_panel_wrapper: UIPanel) -> None:
        self.__static_panel_wrapper = static_panel_wrapper

    def get_quest_name(self) -> UITextBox:
        return self.__quest_name

    def set_quest_name(self, quest_name: UITextBox) -> None:
        self.__quest_name = quest_name

    def get_quest_description(self) -> UITextBox:
        return self.__quest_description

    def set_quest_description(self, quest_description: UITextBox) -> None:
        self.__quest_description = quest_description

    def get_claim_quest_button(self) -> UIButton:
        return self.__claim_quest_button

    def set_claim_quest_button(self, claim_quest_button: UIButton) -> None:
        self.__claim_quest_button = claim_quest_button

    def get_claim_quest(self) -> bool:
        return self.__claim_quest

    def set_claim_quest(self, claim_quest: bool) -> None:
        self.__claim_quest = claim_quest

    def get_xp(self) -> XP:
        return self.__xp

    def set_xp(self, xp: XP) -> None:
        self.__xp = xp

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