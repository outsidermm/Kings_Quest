from states.base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from characters.enemies.base_enemy import BaseEnemy


class LevelSelectionMenu(BaseState):

    __enemies: list[BaseEnemy] = None
    __show_enemy_info: int = -1
    __enemy_buttons: list[UIButton] = None
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

    # Define maximum values for the bars for normalization
    __FIRST_COLUMN_STAT_NAMES: list[str] = [
        "health_points",
        "physical_defense",
        "magical_defense",
        "spell_power",
        "physical_power",
    ]
    __SECOND_COLUMN_STAT_NAMES: list[str] = [
        "health_regeneration",
        "mana_regeneration",
        "mana_points",
        "physical_damage",
        "magical_damage",
    ]

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        enemies: list[BaseEnemy],
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
        self.set_outgoing_transition_data(self.get_incoming_transition_data())

        self.__background_image = pygame.transform.scale(
            pygame.image.load("assets/background_image.png"),
            (self.get_screen().width, self.get_screen().height),
        )

        self.__static_panel_wrapper = UIPanel(
            pygame.Rect((0, 0), (self.get_screen().width, self.get_screen().height)),
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#transparent_panel"),
        )

        UITextBox(
            "Level Selection",
            pygame.Rect((0, -self.get_screen().height * 0.3), (1000, 200)),
            self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@title", object_id="#game_title"),
            container=self.__static_panel_wrapper,
        )

        navigate_character_selection_button_rect = pygame.Rect((75, 0), (300, 100))
        navigate_character_selection_button_rect.bottom = -75
        self.__navigate_character_selection_button = UIButton(
            relative_rect=navigate_character_selection_button_rect,
            text="← Reselect Character",
            manager=self.get_ui_manager(),
            anchors=({"bottom": "bottom"}),
            object_id=ObjectID(class_id="@level_selection_button"),
            container=self.__static_panel_wrapper,
        )

        navigate_quest_rect = pygame.Rect((0, 0), (300, 100))
        navigate_quest_rect.bottomright = (-75, -75)
        self.__navigate_quest_button = UIButton(
            relative_rect=navigate_quest_rect,
            text="Check Quest",
            manager=self.get_ui_manager(),
            anchors=({"right": "right", "bottom": "bottom"}),
            object_id=ObjectID(class_id="@level_selection_button"),
            container=self.__static_panel_wrapper,
        )

        enemy_button_width = 300
        enemy_button_height = 200
        enemy_button_gap = (
            self.get_screen().get_width() - enemy_button_width * len(self.__enemies)
        ) / (len(self.__enemies) + 1)

        for enemy_button_count, enemy in enumerate(self.__enemies):
            self.__enemy_buttons[enemy_button_count] = UIButton(
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
                container=self.__static_panel_wrapper,
            )

        self.__combat_entry_panel = UIPanel(
            pygame.Rect(
                (0, 0), (self.get_screen().width * 0.6, self.get_screen().height * 0.9)
            ),
            manager=self.get_ui_manager(),
            starting_height=2,
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@ability_menu"),
            visible=False,
        )

        self.__navigate_combat_button = UIButton(
            relative_rect=pygame.Rect((-200, 200), (300, 50)),
            text="FIGHT",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__combat_entry_panel,
            object_id=ObjectID(class_id="@level_selection_button"),
        )

        self.__dismiss_popup_button = UIButton(
            relative_rect=pygame.Rect((200, 200), (300, 50)),
            text="CANCEL",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__combat_entry_panel,
            object_id=ObjectID(class_id="@level_selection_button"),
        )

        self.__enemy_name = UITextBox(
            self.__enemies[0].get_name(),
            pygame.Rect((0, 25), (300, 75)),
            self.get_ui_manager(),
            container=self.__combat_entry_panel,
            anchors=({"centerx": "centerx"}),
            object_id=ObjectID(class_id="@level_selection_text"),
        )

        self.__enemy_icon = UIImage(
            pygame.Rect((0, 100), (100, 100)),
            pygame.image.load(self.__enemies[0].get_sprite_location()).convert_alpha(),
            self.get_ui_manager(),
            container=self.__combat_entry_panel,
            anchors=({"centerx": "centerx"}),
        )

        init_y = 250
        gap_per_stats = 40
        first_col_x = -200
        second_col_x = 200

        for stat_count, stat_name in enumerate(self.__FIRST_COLUMN_STAT_NAMES):
            numerical_stat = (
                self.__enemies[0].get_stats()[stat_name]
                if stat_name in self.__enemies[0].get_stats().keys()
                else 0
            )
            self.__stat_text[stat_count] = UITextBox(
                html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                f"{" ".join(word.capitalize() for word in stat_name.split("_"))}: {numerical_stat}",
                relative_rect=pygame.Rect(
                    (first_col_x, init_y + stat_count * gap_per_stats),
                    (300, -1),
                ),
                anchors=({"centerx": "centerx"}),
                manager=self.get_ui_manager(),
                container=self.__combat_entry_panel,
                object_id=ObjectID(object_id="#enemy_statistic"),
            )

        for stat_count, stat_name in enumerate(self.__SECOND_COLUMN_STAT_NAMES):
            numerical_stat = (
                self.__enemies[0].get_stats()[stat_name]
                if stat_name in self.__enemies[0].get_stats().keys()
                else 0
            )
            self.__stat_text[stat_count + 5] = UITextBox(
                html_text=f'<img src="assets/icons_18/{stat_name}.png"> '
                f"{" ".join(word.capitalize() for word in stat_name.split("_"))}: {numerical_stat}",
                relative_rect=pygame.Rect(
                    (second_col_x, init_y + stat_count * gap_per_stats),
                    (300, -1),
                ),
                anchors=({"centerx": "centerx"}),
                manager=self.get_ui_manager(),
                container=self.__combat_entry_panel,
                object_id=ObjectID(object_id="#enemy_statistic"),
            )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_time_to_quit_app(True)
            self.get_ui_manager().process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__navigate_character_selection_button:
                    self.__navigate_character_selection = True
                if event.ui_element == self.__navigate_quest_button:
                    self.__navigate_quest = True
                if event.ui_element == self.__navigate_combat_button:
                    self.__navigate_combat = True
                if event.ui_element == self.__dismiss_popup_button:
                    self.__show_enemy_info = -1
                for enemy_button_index in range(len(self.__enemies)):
                    if event.ui_element == self.__enemy_buttons[enemy_button_index]:
                        self.__show_enemy_info = enemy_button_index

    def run(self) -> None:
        if self.__navigate_character_selection:
            self.set_target_state_name("character_selection_menu")
            self.set_time_to_transition(True)
            return

        if self.__navigate_quest:
            self.set_target_state_name("quest_menu")
            self.set_time_to_transition(True)
            return

        if self.__navigate_combat:
            combat_pair = self.get_incoming_transition_data()
            combat_pair["enemy"] = self.__enemies[self.__show_enemy_info].copy()
            self.set_outgoing_transition_data(combat_pair)
            self.set_target_state_name("turn_based_fight")
            self.set_time_to_transition(True)
            return

    def render(self, time_delta: int) -> None:
        if self.__show_enemy_info != -1:
            self.__enemy_icon.set_image(
                pygame.image.load(
                    self.__enemies[self.__show_enemy_info].get_sprite_location()
                ).convert_alpha()
            )
            self.__enemy_name.set_text(
                self.__enemies[self.__show_enemy_info].get_name()
            )
            for stat_count, stat_name in enumerate(self.__FIRST_COLUMN_STAT_NAMES):
                numerical_stat = (
                    self.__enemies[self.__show_enemy_info].get_stats()[stat_name]
                    if stat_name
                    in self.__enemies[self.__show_enemy_info].get_stats().keys()
                    else 0
                )
                self.__stat_text[stat_count].set_text(
                    f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{" ".join(word.capitalize() for word in stat_name.split("_"))}: {numerical_stat}"
                )

            for stat_count, stat_name in enumerate(self.__SECOND_COLUMN_STAT_NAMES):
                numerical_stat = (
                    self.__enemies[self.__show_enemy_info].get_stats()[stat_name]
                    if stat_name
                    in self.__enemies[self.__show_enemy_info].get_stats().keys()
                    else 0
                )
                self.__stat_text[stat_count + 5].set_text(
                    f'<img src="assets/icons_18/{stat_name}.png"> '
                    f"{" ".join(word.capitalize() for word in stat_name.split("_"))}: {numerical_stat}"
                )

            self.__combat_entry_panel.show()
            self.__static_panel_wrapper.hide()
        else:
            self.__combat_entry_panel.hide()
            self.__static_panel_wrapper.show()

        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(self.__background_image, (0, 0))

        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        self.__navigate_character_selection = False
        self.__navigate_quest = False
        self.__navigate_combat = False

    def end(self) -> None:
        [
            self.__enemy_buttons[enemy_button_index].kill()
            for enemy_button_index in range(len(self.__enemies))
        ]
        self.__navigate_character_selection_button.kill()
        self.__navigate_combat_button.kill()
        self.__navigate_quest_button.kill()
        self.__dismiss_popup_button.kill()
        self.__combat_entry_panel.kill()
        self.__static_panel_wrapper.kill()
        [self.__stat_text[stat_count].kill() for stat_count in range(10)]
        self.__show_enemy_info = -1
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
