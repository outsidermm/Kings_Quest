from states.base_state import BaseState
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from state_manager import GameStateManager
from characters.players.base_player import BasePlayer
from xp import XP
from typing import Any
from gui.ability_hud import AbilityHUD
from gui.statistic_hud import StatisticHUD


# TODO Need to show highlights made


class CharacterSelectionMenu(BaseState):

    __characters: list[BasePlayer] = None
    __selection_page = 0
    __navigate_level_selection: bool = False
    __upgrade_character: bool = False
    __left_switch_character: bool = False
    __right_switch_character: bool = False
    __ability_menu_active: bool = False
    __purchase_upgrade = False
    __dismiss_upgrade = False
    __dismiss_upgrade = False
    __update_GUI: bool = False
    __refund_upgrade: bool = False
    __purchase_ability: bool = False
    __last_pop_up_opened: str = None
    __quit_button_pressed: bool = False
    __ability_HUDs: list[AbilityHUD] = [None] * 3

    __xp: XP = None

    __UPGRADE_LVL_XP_COST: dict[int, Any] = {
        1: 200,
        2: 400,
        3: 800,
        4: -1,
    }

    # Define maximum values for the bars for normalization
    __CHARACTER_MAX_VAL: dict[str, int] = {
        "health_points": 1350,  # Berserker's max health points
        "physical_defense": 250,  # Warrior's max physical defense
        "magical_defense": 150,  # Mage's max magical defense
        "spell_power": 145,  # Mage's 130 + 15 upgrade
        "physical_power": 200,  # Warrior's 90 + 90 upgrade
        "health_regeneration": 20,  # Warrior's max health regeneration
        "mana_regeneration": 10,  # Mage's max mana regeneration
        "mana_points": 300,  # Mage's 250 + 50 upgrade
        "physical_damage": 110,  # Berserker's max physical damage
        "magical_damage": 60,  # Mage's max magical damage
    }

    __UNLOCK_ABILITY_COST: int = 600

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        characters: list[BasePlayer],
        xp: XP = None,
    ):
        super().__init__(
            "character_selection_menu",
            screen,
            ui_manager,
            "level_selection_menu",
            game_state_manager,
        )
        self.__characters = characters
        self.__characater_count = len(characters)
        self.__characater_name_list = [character.get_name() for character in characters]
        self.__xp = XP()

    def start(self) -> None:
        self.__character_picture_panel = UIPanel(
            relative_rect=pygame.Rect(
                (0, 0), (self.get_screen().height, self.get_screen().width * 0.6)
            ),
            manager=self.get_ui_manager(),
            object_id=ObjectID(class_id="@character_pic_panel"),
        )

        self.__character_picture = UIImage(
            relative_rect=pygame.Rect(
                (0, -75),
                (self.get_screen().height * 0.8, self.get_screen().width * 0.48),
            ),
            image_surface=pygame.image.load(
                self.get_characters()[self.__selection_page].get_sprite_location()
            ).convert_alpha(),
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__character_picture_panel,
        )

        right_arrow = pygame.Rect((0, 0), (125, 70))
        right_arrow.right = -50
        right_arrow.bottom = -75
        self.set_right_arrow_select(
            UIButton(
                relative_rect=right_arrow,
                text="→",
                manager=self.get_ui_manager(),
                anchors=({"right": "right", "bottom": "bottom"}),
                container=self.__character_picture_panel,
                object_id=ObjectID(class_id="@arrow"),
            )
        )

        left_arrow = pygame.Rect((50, 0), (125, 70))
        left_arrow.bottom = -75
        self.set_left_arrow_select(
            UIButton(
                relative_rect=left_arrow,
                text="←",
                manager=self.get_ui_manager(),
                anchors=({"bottom": "bottom"}),
                container=self.__character_picture_panel,
                object_id=ObjectID(class_id="@arrow"),
            )
        )

        select_rect = pygame.Rect((0, 0), (125, 70))
        select_rect.bottom = -75
        self.__go_button = UIButton(
            relative_rect=select_rect,
            text="START",
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx", "bottom": "bottom"}),
            container=self.__character_picture_panel,
            object_id=ObjectID(class_id="@go_button"),
        )

        right_info = pygame.Rect(
            (0, 0), (self.get_screen().width * 0.45, self.get_screen().height)
        )
        right_info.right = 0
        self.__character_info_panel = UIPanel(
            relative_rect=right_info,
            manager=self.get_ui_manager(),
            anchors=({"right": "right"}),
            object_id=ObjectID(class_id="@character_info_panel"),
        )

        self.__character_name = UITextBox(
            self.__characater_name_list[0],
            relative_rect=pygame.Rect((50, 30), (-1, -1)),
            manager=self.get_ui_manager(),
            anchors=({"left": "left"}),
            container=self.__character_info_panel,
            object_id=ObjectID(class_id="@sub_title", object_id="#character_info"),
        )

        ability_rec = pygame.Rect((0, 0), (475, 60))
        ability_rec.bottom = -35
        self.__view_ability_button = UIButton(
            relative_rect=ability_rec,
            text="View Abilities",
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx", "bottom": "bottom"}),
            container=self.__character_info_panel,
            object_id=ObjectID(class_id="@unlock_button"),
        )

        upgrade_button_location = pygame.Rect((50, 30), (200, 60))
        upgrade_button_location.right = -50
        self.__upgrade_button = UIButton(
            relative_rect=upgrade_button_location,
            text=f"Upgrade for {self.__UPGRADE_LVL_XP_COST[
                self.get_characters()[self.__selection_page].get_character_level()
            ]} XP",
            manager=self.get_ui_manager(),
            anchors=({"right": "right"}),
            container=self.__character_info_panel,
            object_id=ObjectID(class_id="@unlock_button"),
        )
        if self.get_characters()[self.__selection_page].get_character_level() == 4:
            self.__upgrade_button.set_text("MAX LEVEL")
            self.__upgrade_button.change_object_id(ObjectID(class_id="@lock_button"))

        self.__statistic_HUDs: list[StatisticHUD] = [None] * 10

        for statistic_count, (statistic_name, max_statistic_value) in enumerate(
            self.__CHARACTER_MAX_VAL.items()
        ):
            self.__statistic_HUDs[statistic_count] = StatisticHUD(
                self.get_ui_manager(),
                self.__character_info_panel,
                self.get_characters()[self.__selection_page].get_statistics(),
                statistic_name,
                max_statistic_value,
                statistic_count,
            )

        self.__ability_menu = UIPanel(
            relative_rect=pygame.Rect(
                (0, 0),
                (self.get_screen().width * 0.95, self.get_screen().height * 0.95),
            ),
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@ability_menu"),
            starting_height=2,
            visible=False,
        )

        ability_menu_close_button_rect = pygame.Rect((0, 0), (150, 50))
        ability_menu_close_button_rect.right = -100
        ability_menu_close_button_rect.bottom = -100

        UITextBox(
            "ABILITIES",
            relative_rect=pygame.Rect((-100, 50), (-1, -1)),
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx"}),
            container=self.__ability_menu,
            object_id=ObjectID(class_id="@sub_title", object_id="#ability_text"),
        )

        self.__ability_menu_close = UIButton(
            relative_rect=ability_menu_close_button_rect,
            text="CLOSE",
            manager=self.get_ui_manager(),
            anchors=({"right": "right", "bottom": "bottom"}),
            container=self.__ability_menu,
            object_id=ObjectID(class_id="@unlock_button"),
        )

        for ability_count, ability in enumerate(
            self.get_characters()[self.__selection_page].get_abilities()
        ):
            self.__ability_HUDs[ability_count] = AbilityHUD(
                self.get_screen(),
                self.get_ui_manager(),
                self.__ability_menu,
                self.get_characters()[self.__selection_page],
                ability,
                ability_count,
            )

        self.__upgrade_character_panel: list[UIPanel] = [None] * 2
        # Not Enough XP Panel
        self.__upgrade_character_panel[0] = UIPanel(
            relative_rect=pygame.Rect(
                (0, 0),
                (self.get_screen().width * 0.4, self.get_screen().height * 0.5),
            ),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            starting_height=3,
            object_id=ObjectID(class_id="@character_pic_panel"),
            visible=False,
        )

        # Enough XP Panel
        self.__upgrade_character_panel[1] = UIPanel(
            relative_rect=pygame.Rect(
                (0, 0),
                (self.get_screen().width * 0.4, self.get_screen().height * 0.5),
            ),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            starting_height=3,
            object_id=ObjectID(class_id="@character_pic_panel"),
            visible=False,
        )
        self.__xp_text = UITextBox(
            "",
            relative_rect=pygame.Rect((-100, -100), (-1, -1)),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            container=self.__upgrade_character_panel[1],
            object_id=ObjectID(object_id="#upgrade_menu_text"),
        )

        self.__upgrade_confirm = UIButton(
            relative_rect=pygame.Rect((50, 75), (150, 50)),
            text="CONFIRM",
            manager=self.get_ui_manager(),
            anchors=({"left": "left", "centery": "centery"}),
            container=self.__upgrade_character_panel[1],
            object_id=ObjectID(class_id="@unlock_button"),
        )

        cancel_button_rect = pygame.Rect((0, 75), (150, 50))
        cancel_button_rect.right = -50
        self.__upgrade_cancel = UIButton(
            relative_rect=cancel_button_rect,
            text="CANCEL",
            manager=self.get_ui_manager(),
            anchors=({"right": "right", "centery": "centery"}),
            container=self.__upgrade_character_panel[1],
            object_id=ObjectID(class_id="@unlock_button"),
        )

        UITextBox(
            "Not enough XP!",
            relative_rect=pygame.Rect((-100, -100), (-1, -1)),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            container=self.__upgrade_character_panel[0],
            object_id=ObjectID(object_id="#upgrade_menu_text"),
        )
        self.__upgrade_dismiss = UIButton(
            relative_rect=pygame.Rect((0, 100), (150, 50)),
            text="OK",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__upgrade_character_panel[0],
            object_id=ObjectID(class_id="@unlock_button"),
        )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_button_pressed = True
            self.get_ui_manager().process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.get_left_arrow_select():
                    self.__left_switch_character = True
                if event.ui_element == self.get_right_arrow_select():
                    self.__right_switch_character = True
                if event.ui_element == self.__upgrade_button:
                    self.__upgrade_character = True
                if event.ui_element == self.__go_button:
                    self.__navigate_level_selection = True
                if event.ui_element == self.__view_ability_button:
                    self.__ability_menu_active = True
                if event.ui_element == self.__ability_menu_close:
                    self.__ability_menu_active = False
                if event.ui_element == self.__upgrade_confirm:
                    self.__purchase_upgrade = True
                if event.ui_element == self.__upgrade_cancel:
                    self.__refund_upgrade = True
                if event.ui_element == self.__upgrade_dismiss:
                    self.__dismiss_upgrade = True
                if event.ui_element == self.__ability_HUDs[2].get_ability_button():
                    self.__purchase_ability = True

    def run(self) -> None:
        if self.__quit_button_pressed:
            self.set_time_to_quit_app(True)
            return

        if self.__navigate_level_selection:
            self.set_outgoing_transition_data(
                {"player": self.get_characters()[self.__selection_page]}
            )
            self.set_time_to_transition(True)
            return

        if self.__left_switch_character:
            self.__selection_page = (
                self.__selection_page - 1
            ) % self.__characater_count
            self.__update_GUI = True
        elif self.__right_switch_character:
            self.__selection_page = (
                self.__selection_page + 1
            ) % self.__characater_count
            self.__update_GUI = True

        if self.__ability_menu_active:
            self.__ability_menu.show()
        else:
            self.__ability_menu.hide()

        if (
            self.__upgrade_character
            and self.get_characters()[self.__selection_page].get_character_level() < 4
        ):
            self.__last_pop_up_opened = "character"
            self.__character_info_panel.disable()
            self.__character_picture_panel.disable()

            old_xp = self.__xp.get_xp()
            try:
                self.__xp.lose_xp(
                    self.__UPGRADE_LVL_XP_COST[
                        self.get_characters()[
                            self.__selection_page
                        ].get_character_level()
                    ]
                )
                self.__xp_text.set_text(
                    f"Old XP: {old_xp}\nNew XP: {self.__xp.get_xp()}"
                )
                self.__upgrade_character_panel[1].show()
            except:
                self.__upgrade_character_panel[0].show()

        if self.__dismiss_upgrade and self.__last_pop_up_opened == "character":
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[0].hide()

        if self.__purchase_upgrade and self.__last_pop_up_opened == "character":
            self.get_characters()[self.__selection_page].upgrade()
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()
            self.__update_GUI = True

        if self.__refund_upgrade and self.__last_pop_up_opened == "character":
            self.__xp.gain_xp(
                self.__UPGRADE_LVL_XP_COST[
                    self.get_characters()[self.__selection_page].get_character_level()
                ]
            )
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()

        if (
            self.__purchase_ability
            and self.__characters[self.__selection_page].get_abilities()[2]
            not in self.__characters[self.__selection_page].get_unlocked_abilities()
        ):
            self.__last_pop_up_opened = "ability"
            self.__character_info_panel.disable()
            self.__character_picture_panel.disable()

            old_xp = self.__xp.get_xp()
            try:
                self.__xp.lose_xp(self.__UNLOCK_ABILITY_COST)
                self.__xp_text.set_text(
                    f"Old XP: {old_xp}\nNew XP: {self.__xp.get_xp()}"
                )
                self.__upgrade_character_panel[1].show()
            except:
                self.__upgrade_character_panel[0].show()

        if self.__dismiss_upgrade and self.__last_pop_up_opened == "ability":
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[0].hide()

        if self.__purchase_upgrade and self.__last_pop_up_opened == "ability":
            self.get_characters()[self.__selection_page].unlock_ability()
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()
            self.__update_GUI = True

        if self.__refund_upgrade and self.__last_pop_up_opened == "ability":
            self.__xp.gain_xp(self.__UNLOCK_ABILITY_COST)
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()

    def render(self, time_delta: int) -> None:
        if self.__update_GUI:
            for ability_count, ability in enumerate(
                self.get_characters()[self.__selection_page].get_abilities()
            ):
                self.__ability_HUDs[ability_count].update(
                    self.get_characters()[self.__selection_page], ability, ability_count
                )

            for statistic_count, (statistic_name, max_statistic_value) in enumerate(
                self.__CHARACTER_MAX_VAL.items()
            ):
                self.__statistic_HUDs[statistic_count].update(
                    self.get_characters()[self.__selection_page].get_statistics(),
                    statistic_name,
                    max_statistic_value,
                )

            self.__character_name.set_text(
                self.__characater_name_list[self.__selection_page]
            )
            self.__character_picture.set_image(
                pygame.image.load(
                    self.get_characters()[self.__selection_page].get_sprite_location()
                ).convert_alpha()
            )

            self.__upgrade_button.set_text(
                f"Upgrade for {self.__UPGRADE_LVL_XP_COST[
                self.get_characters()[self.__selection_page].get_character_level()
            ]} XP"
            )
            self.__upgrade_button.change_object_id(ObjectID(class_id="@unlock_button"))
            if self.get_characters()[self.__selection_page].get_character_level() == 4:
                self.__upgrade_button.set_text("MAX LEVEL")
                self.__upgrade_button.change_object_id(
                    ObjectID(class_id="@lock_button")
                )

        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(
            pygame.Surface((self.get_screen().width, self.get_screen().height)), (0, 0)
        )
        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        self.__left_switch_character = False
        self.__right_switch_character = False
        self.__purchase_ability = False
        self.__upgrade_character = False
        self.__refund_upgrade = False
        self.__purchase_upgrade = False
        self.__dismiss_upgrade = False
        self.__update_GUI = False
        self.__quit_button_pressed = False
        self.__navigate_level_selection = False

    def end(self) -> None:
        self.__character_info_panel.kill()
        self.__character_picture_panel.kill()
        self.__ability_menu.kill()
        self.__right_arrow_select.kill()
        self.__left_arrow_select.kill()
        self.__go_button.kill()
        self.__character_name.kill()
        self.__view_ability_button.kill()
        self.__upgrade_button.kill()
        self.__ability_menu_close.kill()
        self.__upgrade_confirm.kill()
        self.__upgrade_cancel.kill()
        self.__upgrade_dismiss.kill()
        self.__xp_text.kill()
        [ability_HUD.kill() for ability_HUD in self.__ability_HUDs]
        [statistic_HUD.kill() for statistic_HUD in self.__statistic_HUDs]
        [upgrade_panel.kill() for upgrade_panel in self.__upgrade_character_panel]
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

    def get_characters(self) -> list[BasePlayer]:
        return self.__characters

    def set_characters(self, characters: list[BasePlayer]) -> None:
        self.__characters = characters

    def get_right_arrow_select(self) -> UIButton:
        return self.__right_arrow_select

    def set_right_arrow_select(self, right_arrow_select: UIButton) -> None:
        self.__right_arrow_select = right_arrow_select

    def get_left_arrow_select(self) -> UIButton:
        return self.__left_arrow_select

    def set_left_arrow_select(self, left_arrow_select: UIButton) -> None:
        self.__left_arrow_select = left_arrow_select

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
