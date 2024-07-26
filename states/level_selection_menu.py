from states.base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from characters.enemies.base_enemy import BaseEnemy
from utilities.general_utility import convert_snake_to_title

FIRST_COLUMN_STAT_NAMES: list[str] = [
    "health_points",
    "physical_defense",
    "magical_defense",
    "spell_power",
    "physical_power",
]
SECOND_COLUMN_STAT_NAMES: list[str] = [
    "health_regeneration",
    "mana_regeneration",
    "mana_points",
    "physical_damage",
    "magical_damage",
]


class LevelSelectionMenu(BaseState):
    """
    LevelSelectionMenu class to handle the selection of levels and navigation to other states.
    """

    __enemies: list[BaseEnemy] = []
    __show_enemy_info: int = -1
    __enemy_buttons: list[UIButton] = []
    __background_image: pygame.Surface = None
    __navigate_character_selection_button: UIButton = None
    __navigate_character_selection: bool = False
    __navigate_combat_button: UIButton = None
    __navigate_combat: bool = False
    __navigate_quest_button: UIButton = None
    __navigate_quest: bool = False
    __dismiss_popup_button: UIButton = None
    __combat_entry_panel: UIPanel = None
    __static_panel_wrapper: UIPanel = None
    __stat_text: list[UITextBox] = [None] * 10
    __enemy_name: UITextBox = None
    __enemy_icon: UIImage = None
    __dismiss_popup_button: UIButton = None
    __enemy_buttons: list[UIButton] = []

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        enemies: list[BaseEnemy],
    ):
        """
        Initializes the LevelSelectionMenu class.

        :param screen: The game screen surface.
        :param ui_manager: The UI manager for pygame_gui.
        :param game_state_manager: The game state manager.
        :param enemies: List of enemies to be displayed.
        """
        super().__init__(
            "level_selection_menu",
            screen,
            ui_manager,
            "turn_based_fight",
            game_state_manager,
        )
        self.set_enemies(enemies)
        self.set_enemy_buttons([None] * len(self.get_enemies()))

    def start(self) -> None:
        """
        Starts the level selection menu by setting up UI elements and background image.
        """
        self.set_outgoing_transition_data(self.get_incoming_transition_data())

        self.set_background_image(
            pygame.transform.scale(
                pygame.image.load("assets/background_image.png"),
                (self.get_screen().get_width(), self.get_screen().get_height()),
            )
        )

        self.set_static_panel_wrapper(
            UIPanel(
                pygame.Rect(
                    (0, 0),
                    (self.get_screen().get_width(), self.get_screen().get_height()),
                ),
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#transparent_panel"),
            )
        )

        UITextBox(
            "Level Selection",
            pygame.Rect((0, -self.get_screen().get_height() * 0.3), (1000, 200)),
            self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@title", object_id="#game_title"),
            container=self.get_static_panel_wrapper(),
        )

        navigate_character_selection_button_rect = pygame.Rect((75, 0), (300, 100))
        navigate_character_selection_button_rect.bottom = -75
        self.set_navigate_character_selection_button(
            UIButton(
                relative_rect=navigate_character_selection_button_rect,
                text="← Reselect Character",
                manager=self.get_ui_manager(),
                anchors=({"bottom": "bottom"}),
                object_id=ObjectID(class_id="@level_selection_button"),
                container=self.get_static_panel_wrapper(),
            )
        )

        navigate_quest_rect = pygame.Rect((0, 0), (300, 100))
        navigate_quest_rect.bottomright = (-75, -75)
        self.set_navigate_quest_button(
            UIButton(
                relative_rect=navigate_quest_rect,
                text="Check Quest",
                manager=self.get_ui_manager(),
                anchors=({"right": "right", "bottom": "bottom"}),
                object_id=ObjectID(class_id="@level_selection_button"),
                container=self.get_static_panel_wrapper(),
            )
        )

        enemy_button_width = 300
        enemy_button_height = 200
        enemy_button_gap = (
            self.get_screen().get_width() - enemy_button_width * len(self.get_enemies())
        ) / (len(self.get_enemies()) + 1)

        for enemy_button_count, enemy in enumerate(self.get_enemies()):
            self.get_enemy_buttons()[enemy_button_count] = UIButton(
                relative_rect=pygame.Rect(
                    (
                        enemy_button_gap * (enemy_button_count + 1)
                        + enemy_button_width * enemy_button_count,
                        0,
                    ),
                    (enemy_button_width, enemy_button_height),
                ),
                text=f"{enemy_button_count+1}: {enemy.get_name()}",
                anchors=({"centery": "centery"}),
                manager=self.get_ui_manager(),
                object_id=ObjectID(class_id="@level_selection_button"),
                container=self.get_static_panel_wrapper(),
            )

        self.set_combat_entry_panel(
            UIPanel(
                pygame.Rect(
                    (0, 0),
                    (
                        self.get_screen().get_width() * 0.6,
                        self.get_screen().get_height() * 0.9,
                    ),
                ),
                manager=self.get_ui_manager(),
                starting_height=2,
                anchors=({"center": "center"}),
                object_id=ObjectID(class_id="@ability_menu"),
                visible=False,
            )
        )

        self.set_navigate_combat_button(
            UIButton(
                relative_rect=pygame.Rect((-200, 200), (300, 50)),
                text="FIGHT",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                container=self.get_combat_entry_panel(),
                object_id=ObjectID(class_id="@level_selection_button"),
            )
        )

        self.set_dismiss_popup_button(
            UIButton(
                relative_rect=pygame.Rect((200, 200), (300, 50)),
                text="CANCEL",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                container=self.get_combat_entry_panel(),
                object_id=ObjectID(class_id="@level_selection_button"),
            )
        )

        self.set_enemy_name(
            UITextBox(
                self.get_enemies()[0].get_name(),
                pygame.Rect((0, 25), (300, 75)),
                self.get_ui_manager(),
                container=self.get_combat_entry_panel(),
                anchors=({"centerx": "centerx"}),
                object_id=ObjectID(class_id="@level_selection_text"),
            )
        )

        self.set_enemy_icon(
            UIImage(
                pygame.Rect((0, 100), (100, 100)),
                pygame.image.load(
                    self.get_enemies()[0].get_sprite_location()
                ).convert_alpha(),
                self.get_ui_manager(),
                container=self.get_combat_entry_panel(),
                anchors=({"centerx": "centerx"}),
            )
        )

        init_y = 250
        gap_per_stats = 40
        first_col_x = -200
        second_col_x = 200

        for stat_count, stat_name in enumerate(FIRST_COLUMN_STAT_NAMES):
            numerical_stat = (
                self.get_enemies()[0].get_stats()[stat_name]
                if stat_name in self.get_enemies()[0].get_stats().keys()
                else 0
            )
            self.get_stat_text()[stat_count] = UITextBox(
                html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                f"{convert_snake_to_title(stat_name)}: {numerical_stat}",
                relative_rect=pygame.Rect(
                    (first_col_x, init_y + stat_count * gap_per_stats),
                    (300, -1),
                ),
                anchors=({"centerx": "centerx"}),
                manager=self.get_ui_manager(),
                container=self.get_combat_entry_panel(),
                object_id=ObjectID(object_id="#enemy_statistic"),
            )

        for stat_count, stat_name in enumerate(SECOND_COLUMN_STAT_NAMES):
            numerical_stat = (
                self.get_enemies()[0].get_stats()[stat_name]
                if stat_name in self.get_enemies()[0].get_stats().keys()
                else 0
            )
            self.get_stat_text()[stat_count + 5] = UITextBox(
                html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                f"{convert_snake_to_title(stat_name)}: {numerical_stat}",
                relative_rect=pygame.Rect(
                    (second_col_x, init_y + stat_count * gap_per_stats),
                    (300, -1),
                ),
                anchors=({"centerx": "centerx"}),
                manager=self.get_ui_manager(),
                container=self.get_combat_entry_panel(),
                object_id=ObjectID(object_id="#enemy_statistic"),
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
                if event.ui_element == self.get_navigate_character_selection_button():
                    self.set_navigate_character_selection(True)
                if event.ui_element == self.get_navigate_quest_button():
                    self.set_navigate_quest(True)
                if event.ui_element == self.get_navigate_combat_button():
                    self.set_navigate_combat(True)
                if event.ui_element == self.get_dismiss_popup_button():
                    self.set_show_enemy_info(-1)
                for enemy_button_index in range(len(self.get_enemies())):
                    if event.ui_element == self.get_enemy_buttons()[enemy_button_index]:
                        self.set_show_enemy_info(enemy_button_index)

    def run(self) -> None:
        """
        Runs the logic for the level selection menu, such as navigating to different states.
        This method checks various conditions to determine if a state transition should occur.
        """
        # Check if the character selection menu should be navigated to
        if self.get_navigate_character_selection():
            # Set the target state to the character selection menu
            self.set_target_state_name("character_selection_menu")
            # Mark that a transition should occur
            self.set_time_to_transition(True)
            return

        # Check if the quest menu should be navigated to
        if self.get_navigate_quest():
            # Set the target state to the quest menu
            self.set_target_state_name("quest_menu")
            # Mark that a transition should occur
            self.set_time_to_transition(True)
            return

        # Check if the combat menu should be navigated to
        if self.get_navigate_combat():
            # Get the incoming transition data
            combat_pair = self.get_incoming_transition_data()
            # Add enemy information to the transition data
            combat_pair["enemy"] = self.get_enemies()[self.get_show_enemy_info()].copy()
            # Set the outgoing transition data
            self.set_outgoing_transition_data(combat_pair)
            # Set the target state to the turn-based fight
            self.set_target_state_name("turn_based_fight")
            # Mark that a transition should occur
            self.set_time_to_transition(True)
            return

    def render(self, time_delta: int) -> None:
        """
        Renders the level selection menu, including enemy information and static panels.

        :param time_delta: Time elapsed since the last frame.
        """
        # Check if enemy information should be displayed
        if self.get_show_enemy_info() != -1:
            # Load and set the enemy icon image
            self.get_enemy_icon().set_image(
                pygame.image.load(
                    self.get_enemies()[self.get_show_enemy_info()].get_sprite_location()
                ).convert_alpha()
            )
            # Set the enemy name text
            self.get_enemy_name().set_text(
                self.get_enemies()[self.get_show_enemy_info()].get_name()
            )

            # Loop through the first column of stat names and display their values
            for stat_count, stat_name in enumerate(FIRST_COLUMN_STAT_NAMES):
                # Retrieve the numerical stat value, default to 0 if stat not found
                numerical_stat = (
                    self.get_enemies()[self.get_show_enemy_info()].get_stats()[
                        stat_name
                    ]
                    if stat_name
                    in self.get_enemies()[self.get_show_enemy_info()].get_stats().keys()
                    else 0
                )
                # Set the stat text with an icon
                self.get_stat_text()[stat_count].set_text(
                    f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{convert_snake_to_title(stat_name)}: {numerical_stat}"
                )

            # Loop through the second column of stat names and display their values
            for stat_count, stat_name in enumerate(SECOND_COLUMN_STAT_NAMES):
                # Retrieve the numerical stat value, default to 0 if stat not found
                numerical_stat = (
                    self.get_enemies()[self.get_show_enemy_info()].get_stats()[
                        stat_name
                    ]
                    if stat_name
                    in self.get_enemies()[self.get_show_enemy_info()].get_stats().keys()
                    else 0
                )
                # Set the stat text with an icon
                self.get_stat_text()[stat_count + 5].set_text(
                    f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{convert_snake_to_title(stat_name)}: {numerical_stat}"
                )

            # Show the combat entry panel and hide the static panel wrapper
            self.get_combat_entry_panel().show()
            self.get_static_panel_wrapper().hide()
        else:
            # Hide the combat entry panel and show the static panel wrapper
            self.get_combat_entry_panel().hide()
            self.get_static_panel_wrapper().show()

        # Update the UI manager with the time delta
        self.get_ui_manager().update(time_delta)
        # Blit (copy) the background image onto the screen at coordinates (0, 0)
        self.get_screen().blit(self.get_background_image(), (0, 0))

        # Draw the UI elements onto the screen
        self.get_ui_manager().draw_ui(self.get_screen())
        # Update the display to reflect the changes
        pygame.display.update()

    def reset_event_polling(self) -> None:
        """
        Resets the event polling flags.
        """
        self.set_navigate_character_selection(False)
        self.set_navigate_quest(False)
        self.set_navigate_combat(False)

    def end(self) -> None:
        """
        Ends the level selection menu by killing all UI elements.
        """
        [button.kill() for button in self.get_enemy_buttons()]
        self.get_navigate_character_selection_button().kill()
        self.get_navigate_combat_button().kill()
        self.get_navigate_quest_button().kill()
        self.get_dismiss_popup_button().kill()
        self.get_combat_entry_panel().kill()
        self.get_static_panel_wrapper().kill()
        [self.get_stat_text()[stat_count].kill() for stat_count in range(10)]
        self.set_show_enemy_info(-1)
        self.get_screen().fill((0, 0, 0))

    # Getters and setters

    def get_enemies(self) -> list[BaseEnemy]:
        return self.__enemies

    def set_enemies(self, enemies: list[BaseEnemy]) -> None:
        self.__enemies = enemies

    def get_show_enemy_info(self) -> int:
        return self.__show_enemy_info

    def set_show_enemy_info(self, show_enemy_info: int) -> None:
        self.__show_enemy_info = show_enemy_info

    def get_enemy_buttons(self) -> list[UIButton]:
        return self.__enemy_buttons

    def set_enemy_buttons(self, enemy_buttons: list[UIButton]) -> None:
        self.__enemy_buttons = enemy_buttons

    def get_background_image(self) -> pygame.Surface:
        return self.__background_image

    def set_background_image(self, background_image: pygame.Surface) -> None:
        self.__background_image = background_image

    def get_navigate_character_selection_button(self) -> UIButton:
        return self.__navigate_character_selection_button

    def set_navigate_character_selection_button(self, button: UIButton) -> None:
        self.__navigate_character_selection_button = button

    def get_navigate_character_selection(self) -> bool:
        return self.__navigate_character_selection

    def set_navigate_character_selection(self, navigate: bool) -> None:
        self.__navigate_character_selection = navigate

    def get_navigate_combat_button(self) -> UIButton:
        return self.__navigate_combat_button

    def set_navigate_combat_button(self, button: UIButton) -> None:
        self.__navigate_combat_button = button

    def get_navigate_combat(self) -> bool:
        return self.__navigate_combat

    def set_navigate_combat(self, navigate: bool) -> None:
        self.__navigate_combat = navigate

    def get_navigate_quest_button(self) -> UIButton:
        return self.__navigate_quest_button

    def set_navigate_quest_button(self, button: UIButton) -> None:
        self.__navigate_quest_button = button

    def get_navigate_quest(self) -> bool:
        return self.__navigate_quest

    def set_navigate_quest(self, navigate: bool) -> None:
        self.__navigate_quest = navigate

    def get_dismiss_popup_button(self) -> UIButton:
        return self.__dismiss_popup_button

    def set_dismiss_popup_button(self, button: UIButton) -> None:
        self.__dismiss_popup_button = button

    def get_combat_entry_panel(self) -> UIPanel:
        return self.__combat_entry_panel

    def set_combat_entry_panel(self, panel: UIPanel) -> None:
        self.__combat_entry_panel = panel

    def get_static_panel_wrapper(self) -> UIPanel:
        return self.__static_panel_wrapper

    def set_static_panel_wrapper(self, panel: UIPanel) -> None:
        self.__static_panel_wrapper = panel

    def get_stat_text(self) -> list[UITextBox]:
        return self.__stat_text

    def set_stat_text(self, stat_text: list[UITextBox]) -> None:
        self.__stat_text = stat_text

    def get_enemy_name(self) -> UITextBox:
        return self.__enemy_name

    def set_enemy_name(self, enemy_name: UITextBox) -> None:
        self.__enemy_name = enemy_name

    def get_enemy_icon(self) -> UIImage:
        return self.__enemy_icon

    def set_enemy_icon(self, enemy_icon: UIImage) -> None:
        self.__enemy_icon = enemy_icon
