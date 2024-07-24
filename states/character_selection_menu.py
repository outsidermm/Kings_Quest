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


class CharacterSelectionMenu(BaseState):
    __characters: list[BasePlayer] = None
    __selection_page: int = 0
    __navigate_level_selection: bool = False
    __upgrade_character: bool = False
    __left_switch_character: bool = False
    __right_switch_character: bool = False
    __ability_menu_active: bool = False
    __purchase_upgrade: bool = False
    __dismiss_upgrade: bool = False
    __update_GUI: bool = False
    __refund_upgrade: bool = False
    __purchase_ability: bool = False
    __last_pop_up_opened: str = None
    __ability_HUDs: list[AbilityHUD] = [None] * 3
    __xp: XP = None
    __character_picture_panel: UIPanel = None
    __character_picture: UIImage = None
    __right_arrow_select: UIButton = None
    __left_arrow_select: UIButton = None
    __go_button: UIButton = None
    __character_info_panel: UIPanel = None
    __character_name: UITextBox = None
    __view_ability_button: UIButton = None
    __upgrade_button: UIButton = None
    __ability_menu: UIPanel = None
    __ability_menu_close: UIButton = None
    __upgrade_confirm: UIButton = None
    __upgrade_cancel: UIButton = None
    __upgrade_dismiss: UIButton = None
    __xp_text: UITextBox = None
    __stat_HUDs: list[StatisticHUD] = [None] * 10
    __upgrade_character_panel: list[UIPanel] = [None] * 2

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
        xp: XP,
    ):
        super().__init__(
            "character_selection_menu",
            screen,
            ui_manager,
            "level_selection_menu",
            game_state_manager,
        )
        self.set_characters(characters)
        self.set_characater_count(len(characters))
        self.set_characater_name_list(
            [character.get_name() for character in characters]
        )
        self.set_xp(xp)

    def start(self) -> None:
        self.set_character_picture_panel(
            UIPanel(
                relative_rect=pygame.Rect(
                    (0, 0), (self.get_screen().height, self.get_screen().width * 0.6)
                ),
                manager=self.get_ui_manager(),
                object_id=ObjectID(class_id="@character_pic_panel"),
            )
        )

        self.set_character_picture(
            UIImage(
                relative_rect=pygame.Rect(
                    (0, -75),
                    (self.get_screen().height * 0.8, self.get_screen().width * 0.48),
                ),
                image_surface=pygame.image.load(
                    self.get_characters()[
                        self.get_selection_page()
                    ].get_sprite_location()
                ).convert_alpha(),
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                container=self.get_character_picture_panel(),
            )
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
                container=self.get_character_picture_panel(),
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
                container=self.get_character_picture_panel(),
                object_id=ObjectID(class_id="@arrow"),
            )
        )

        select_rect = pygame.Rect((0, 0), (125, 70))
        select_rect.bottom = -75
        self.set_go_button(
            UIButton(
                relative_rect=select_rect,
                text="START",
                manager=self.get_ui_manager(),
                anchors=({"centerx": "centerx", "bottom": "bottom"}),
                container=self.get_character_picture_panel(),
                object_id=ObjectID(class_id="@go_button"),
            )
        )

        right_info = pygame.Rect(
            (0, 0), (self.get_screen().width * 0.45, self.get_screen().height)
        )
        right_info.right = 0
        self.set_character_info_panel(
            UIPanel(
                relative_rect=right_info,
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                object_id=ObjectID(class_id="@character_info_panel"),
            )
        )

        self.set_character_name(
            UITextBox(
                self.get_characater_name_list()[0],
                relative_rect=pygame.Rect((50, 30), (-1, -1)),
                manager=self.get_ui_manager(),
                anchors=({"left": "left"}),
                container=self.get_character_info_panel(),
                object_id=ObjectID(class_id="@sub_title", object_id="#character_info"),
            )
        )

        ability_rec = pygame.Rect((0, 0), (475, 60))
        ability_rec.bottom = -35
        self.set_view_ability_button(
            UIButton(
                relative_rect=ability_rec,
                text="View Abilities",
                manager=self.get_ui_manager(),
                anchors=({"centerx": "centerx", "bottom": "bottom"}),
                container=self.get_character_info_panel(),
                object_id=ObjectID(class_id="@unlock_button"),
            )
        )

        upgrade_button_location = pygame.Rect((50, 30), (200, 60))
        upgrade_button_location.right = -50
        self.set_upgrade_button(
            UIButton(
                relative_rect=upgrade_button_location,
                text=f"Upgrade for {self.__UPGRADE_LVL_XP_COST[self.get_characters()[self.get_selection_page()].get_character_level()]} XP",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                container=self.get_character_info_panel(),
                object_id=ObjectID(class_id="@unlock_button"),
            )
        )
        if self.get_characters()[self.get_selection_page()].get_character_level() == 4:
            self.get_upgrade_button().set_text("MAX LEVEL")
            self.get_upgrade_button().change_object_id(
                ObjectID(class_id="@lock_button")
            )

        for stat_count, (stat_name, max_stat_value) in enumerate(
            self.__CHARACTER_MAX_VAL.items()
        ):
            self.get_stat_HUDs()[stat_count] = StatisticHUD(
                self.get_ui_manager(),
                self.get_character_info_panel(),
                self.get_characters()[self.get_selection_page()].get_stats(),
                stat_name,
                max_stat_value,
                stat_count,
            )

        self.set_ability_menu(
            UIPanel(
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
        )

        ability_menu_close_button_rect = pygame.Rect((0, 0), (150, 50))
        ability_menu_close_button_rect.right = -100
        ability_menu_close_button_rect.bottom = -100

        UITextBox(
            "ABILITIES",
            relative_rect=pygame.Rect((-100, 50), (-1, -1)),
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx"}),
            container=self.get_ability_menu(),
            object_id=ObjectID(class_id="@sub_title", object_id="#ability_text"),
        )

        self.set_ability_menu_close(
            UIButton(
                relative_rect=ability_menu_close_button_rect,
                text="CLOSE",
                manager=self.get_ui_manager(),
                anchors=({"right": "right", "bottom": "bottom"}),
                container=self.get_ability_menu(),
                object_id=ObjectID(class_id="@unlock_button"),
            )
        )

        for ability_count, ability in enumerate(
            self.get_characters()[self.get_selection_page()].get_abilities()
        ):
            self.get_ability_HUDs()[ability_count] = AbilityHUD(
                self.get_screen(),
                self.get_ui_manager(),
                self.get_ability_menu(),
                self.get_characters()[self.get_selection_page()],
                ability,
                ability_count,
            )

        # Not Enough XP Panel
        self.get_upgrade_character_panel()[0] = UIPanel(
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
        self.get_upgrade_character_panel()[1] = UIPanel(
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
        self.set_xp_text(
            UITextBox(
                "",
                relative_rect=pygame.Rect((-100, -100), (-1, -1)),
                anchors=({"center": "center"}),
                manager=self.get_ui_manager(),
                container=self.get_upgrade_character_panel()[1],
                object_id=ObjectID(object_id="#upgrade_menu_text"),
            )
        )

        self.set_upgrade_confirm(
            UIButton(
                relative_rect=pygame.Rect((50, 75), (150, 50)),
                text="CONFIRM",
                manager=self.get_ui_manager(),
                anchors=({"left": "left", "centery": "centery"}),
                container=self.get_upgrade_character_panel()[1],
                object_id=ObjectID(class_id="@unlock_button"),
            )
        )

        cancel_button_rect = pygame.Rect((0, 75), (150, 50))
        cancel_button_rect.right = -50
        self.set_upgrade_cancel(
            UIButton(
                relative_rect=cancel_button_rect,
                text="CANCEL",
                manager=self.get_ui_manager(),
                anchors=({"right": "right", "centery": "centery"}),
                container=self.get_upgrade_character_panel()[1],
                object_id=ObjectID(class_id="@unlock_button"),
            )
        )

        UITextBox(
            "Not enough XP!",
            relative_rect=pygame.Rect((-100, -100), (-1, -1)),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            container=self.get_upgrade_character_panel()[0],
            object_id=ObjectID(object_id="#upgrade_menu_text"),
        )
        self.set_upgrade_dismiss(
            UIButton(
                relative_rect=pygame.Rect((0, 100), (150, 50)),
                text="OK",
                manager=self.get_ui_manager(),
                anchors=({"center": "center"}),
                container=self.get_upgrade_character_panel()[0],
                object_id=ObjectID(class_id="@unlock_button"),
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
                if event.ui_element == self.get_left_arrow_select():
                    self.set_left_switch_character(True)
                if event.ui_element == self.get_right_arrow_select():
                    self.set_right_switch_character(True)
                if event.ui_element == self.get_upgrade_button():
                    self.set_upgrade_character(True)
                if event.ui_element == self.get_go_button():
                    self.set_navigate_level_selection(True)
                if event.ui_element == self.get_view_ability_button():
                    self.set_ability_menu_active(True)
                if event.ui_element == self.get_ability_menu_close():
                    self.set_ability_menu_active(False)
                if event.ui_element == self.get_upgrade_confirm():
                    self.set_purchase_upgrade(True)
                if event.ui_element == self.get_upgrade_cancel():
                    self.set_refund_upgrade(True)
                if event.ui_element == self.get_upgrade_dismiss():
                    self.set_dismiss_upgrade(True)
                if event.ui_element == self.get_ability_HUDs()[2].get_ability_button():
                    self.set_purchase_ability(True)

    def run(self) -> None:
        """
        Runs the logic for character selection, such as navigating to level selection,
        switching characters, upgrading characters, and purchasing abilities.
        """
        if self.get_navigate_level_selection():
            # If the player has selected to navigate to the level selection screen,
            # set the outgoing transition data with the current player and trigger the transition.
            self.set_outgoing_transition_data(
                {"player": self.get_characters()[self.get_selection_page()].copy()}
            )
            self.set_time_to_transition(True)
            return

        if self.get_left_switch_character():
            # If the player has selected to switch to the previous character,
            # update the selection page and set the flag to update the GUI.
            self.set_selection_page(
                (self.get_selection_page() - 1) % self.get_characater_count()
            )
            self.set_update_GUI(True)
        elif self.get_right_switch_character():
            # If the player has selected to switch to the next character,
            # update the selection page and set the flag to update the GUI.
            self.set_selection_page(
                (self.get_selection_page() + 1) % self.get_characater_count()
            )
            self.set_update_GUI(True)

        if self.get_ability_menu_active():
            # Show the ability menu if it is active.
            self.get_ability_menu().show()
        else:
            # Hide the ability menu if it is not active.
            self.get_ability_menu().hide()

        if (
            self.get_upgrade_character()
            and self.get_characters()[self.get_selection_page()].get_character_level()
            < 4
        ):
            # If the player has selected to upgrade the character and the character level is less than 4,
            # open the upgrade character panel.
            self.set_last_pop_up_opened("character")
            self.get_character_info_panel().disable()
            self.get_character_picture_panel().disable()

            old_xp = self.get_xp().get_xp()
            try:
                # Try to deduct the XP cost for the upgrade.
                self.get_xp().lose_xp(
                    self.__UPGRADE_LVL_XP_COST[
                        self.get_characters()[
                            self.get_selection_page()
                        ].get_character_level()
                    ]
                )
                # Update the XP text and show the appropriate panel.
                self.get_xp_text().set_text(
                    f"Old XP: {old_xp}\nNew XP: {self.get_xp().get_xp()}"
                )
                self.get_upgrade_character_panel()[1].show()
            except:
                # Show the panel indicating insufficient XP.
                self.get_upgrade_character_panel()[0].show()

        if self.get_dismiss_upgrade() and self.get_last_pop_up_opened() == "character":
            # If the upgrade is dismissed and the last popup opened was for character,
            # enable the character info and picture panels and hide the upgrade panel.
            self.get_character_info_panel().enable()
            self.get_character_picture_panel().enable()
            self.get_upgrade_character_panel()[0].hide()

        if self.get_purchase_upgrade() and self.get_last_pop_up_opened() == "character":
            # If the upgrade is purchased and the last popup opened was for character,
            # upgrade the character, enable the character info and picture panels, hide the upgrade panel,
            # and set the flag to update the GUI.
            self.get_characters()[self.get_selection_page()].upgrade()
            self.get_character_info_panel().enable()
            self.get_character_picture_panel().enable()
            self.get_upgrade_character_panel()[1].hide()
            self.set_update_GUI(True)

        if self.get_refund_upgrade() and self.get_last_pop_up_opened() == "character":
            # If the upgrade is refunded and the last popup opened was for character,
            # refund the XP, enable the character info and picture panels, and hide the upgrade panel.
            self.get_xp().gain_xp(
                self.__UPGRADE_LVL_XP_COST[
                    self.get_characters()[
                        self.get_selection_page()
                    ].get_character_level()
                ]
            )
            self.get_character_info_panel().enable()
            self.get_character_picture_panel().enable()
            self.get_upgrade_character_panel()[1].hide()

        if (
            self.get_purchase_ability()
            and self.get_characters()[self.get_selection_page()].get_abilities()[2]
            not in self.get_characters()[
                self.get_selection_page()
            ].get_unlocked_abilities()
        ):
            # If the ability is purchased and it is not already unlocked,
            # open the ability purchase panel.
            self.set_last_pop_up_opened("ability")
            self.get_character_info_panel().disable()
            self.get_character_picture_panel().disable()

            old_xp = self.get_xp().get_xp()
            try:
                # Try to deduct the XP cost for the ability.
                self.get_xp().lose_xp(self.__UNLOCK_ABILITY_COST)
                # Update the XP text and show the appropriate panel.
                self.get_xp_text().set_text(
                    f"Old XP: {old_xp}\nNew XP: {self.get_xp().get_xp()}"
                )
                self.get_upgrade_character_panel()[1].show()
            except:
                # Show the panel indicating insufficient XP.
                self.get_upgrade_character_panel()[0].show()

        if self.get_dismiss_upgrade() and self.get_last_pop_up_opened() == "ability":
            # If the ability purchase is dismissed and the last popup opened was for ability,
            # enable the character info and picture panels and hide the upgrade panel.
            self.get_character_info_panel().enable()
            self.get_character_picture_panel().enable()
            self.get_upgrade_character_panel()[0].hide()

        if self.get_purchase_upgrade() and self.get_last_pop_up_opened() == "ability":
            # If the ability is purchased and the last popup opened was for ability,
            # unlock the ability, enable the character info and picture panels, hide the upgrade panel,
            # and set the flag to update the GUI.
            self.get_characters()[self.get_selection_page()].unlock_ability()
            self.get_character_info_panel().enable()
            self.get_character_picture_panel().enable()
            self.get_upgrade_character_panel()[1].hide()
            self.set_update_GUI(True)

        if self.get_refund_upgrade() and self.get_last_pop_up_opened() == "ability":
            # If the ability purchase is refunded and the last popup opened was for ability,
            # refund the XP, enable the character info and picture panels, and hide the upgrade panel.
            self.get_xp().gain_xp(self.__UNLOCK_ABILITY_COST)
            self.get_character_info_panel().enable()
            self.get_character_picture_panel().enable()
            self.get_upgrade_character_panel()[1].hide()

    def render(self, time_delta: int) -> None:
        """
        Renders the character selection menu, updating UI elements and handling GUI changes.

        :param time_delta: Time elapsed since the last frame.
        """
        if self.get_update_GUI():
            # Update the ability HUDs for the current character
            for ability_count, ability in enumerate(
                self.get_characters()[self.get_selection_page()].get_abilities()
            ):
                self.get_ability_HUDs()[ability_count].update(
                    self.get_characters()[self.get_selection_page()],
                    ability,
                    ability_count,
                )

            # Update the stat HUDs for the current character
            for stat_count, (stat_name, max_stat_value) in enumerate(
                self.__CHARACTER_MAX_VAL.items()
            ):
                self.get_stat_HUDs()[stat_count].update(
                    self.get_characters()[self.get_selection_page()].get_stats(),
                    stat_name,
                    max_stat_value,
                )

            # Update the character name in the HUD
            self.get_character_name().set_text(
                self.get_characater_name_list()[self.get_selection_page()]
            )

            # Update the character picture in the HUD
            self.get_character_picture().set_image(
                pygame.image.load(
                    self.get_characters()[
                        self.get_selection_page()
                    ].get_sprite_location()
                ).convert_alpha()
            )

            # Update the text and style of the upgrade button based on character level
            self.get_upgrade_button().set_text(
                f"Upgrade for {self.__UPGRADE_LVL_XP_COST[self.get_characters()[self.get_selection_page()].get_character_level()]} XP"
            )
            self.get_upgrade_button().change_object_id(
                ObjectID(class_id="@unlock_button")
            )

            # If character level is max, set the button text to "MAX LEVEL"
            if (
                self.get_characters()[self.get_selection_page()].get_character_level()
                == 4
            ):
                self.get_upgrade_button().set_text("MAX LEVEL")
                self.get_upgrade_button().change_object_id(
                    ObjectID(class_id="@lock_button")
                )

        # Update the UI manager
        self.get_ui_manager().update(time_delta)

        # Clear the screen
        self.get_screen().blit(
            pygame.Surface((self.get_screen().width, self.get_screen().height)), (0, 0)
        )

        # Draw the updated UI elements on the screen
        self.get_ui_manager().draw_ui(self.get_screen())

        # Update the display to show the changes
        pygame.display.update()

    def reset_event_polling(self) -> None:
        """
        Resets the event polling flags.
        """
        self.set_left_switch_character(False)
        self.set_right_switch_character(False)
        self.set_purchase_ability(False)
        self.set_upgrade_character(False)
        self.set_refund_upgrade(False)
        self.set_purchase_upgrade(False)
        self.set_dismiss_upgrade(False)
        self.set_update_GUI(False)
        self.set_navigate_level_selection(False)

    def end(self) -> None:
        """
        Ends the character selection menu by killing all UI elements.
        """
        self.get_character_info_panel().kill()
        self.get_character_picture_panel().kill()
        self.get_ability_menu().kill()
        self.get_right_arrow_select().kill()
        self.get_left_arrow_select().kill()
        self.get_go_button().kill()
        self.get_character_name().kill()
        self.get_view_ability_button().kill()
        self.get_upgrade_button().kill()
        self.get_ability_menu_close().kill()
        self.get_upgrade_confirm().kill()
        self.get_upgrade_cancel().kill()
        self.get_upgrade_dismiss().kill()
        self.get_xp_text().kill()
        [ability_HUD.kill() for ability_HUD in self.get_ability_HUDs()]
        [stat_HUD.kill() for stat_HUD in self.get_stat_HUDs()]
        [upgrade_panel.kill() for upgrade_panel in self.get_upgrade_character_panel()]
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

    def get_selection_page(self) -> int:
        return self.__selection_page

    def set_selection_page(self, selection_page: int) -> None:
        self.__selection_page = selection_page

    def get_navigate_level_selection(self) -> bool:
        return self.__navigate_level_selection

    def set_navigate_level_selection(self, navigate_level_selection: bool) -> None:
        self.__navigate_level_selection = navigate_level_selection

    def get_upgrade_character(self) -> bool:
        return self.__upgrade_character

    def set_upgrade_character(self, upgrade_character: bool) -> None:
        self.__upgrade_character = upgrade_character

    def get_left_switch_character(self) -> bool:
        return self.__left_switch_character

    def set_left_switch_character(self, left_switch_character: bool) -> None:
        self.__left_switch_character = left_switch_character

    def get_right_switch_character(self) -> bool:
        return self.__right_switch_character

    def set_right_switch_character(self, right_switch_character: bool) -> None:
        self.__right_switch_character = right_switch_character

    def get_ability_menu_active(self) -> bool:
        return self.__ability_menu_active

    def set_ability_menu_active(self, ability_menu_active: bool) -> None:
        self.__ability_menu_active = ability_menu_active

    def get_purchase_upgrade(self) -> bool:
        return self.__purchase_upgrade

    def set_purchase_upgrade(self, purchase_upgrade: bool) -> None:
        self.__purchase_upgrade = purchase_upgrade

    def get_dismiss_upgrade(self) -> bool:
        return self.__dismiss_upgrade

    def set_dismiss_upgrade(self, dismiss_upgrade: bool) -> None:
        self.__dismiss_upgrade = dismiss_upgrade

    def get_update_GUI(self) -> bool:
        return self.__update_GUI

    def set_update_GUI(self, update_GUI: bool) -> None:
        self.__update_GUI = update_GUI

    def get_refund_upgrade(self) -> bool:
        return self.__refund_upgrade

    def set_refund_upgrade(self, refund_upgrade: bool) -> None:
        self.__refund_upgrade = refund_upgrade

    def get_purchase_ability(self) -> bool:
        return self.__purchase_ability

    def set_purchase_ability(self, purchase_ability: bool) -> None:
        self.__purchase_ability = purchase_ability

    def get_last_pop_up_opened(self) -> str:
        return self.__last_pop_up_opened

    def set_last_pop_up_opened(self, last_pop_up_opened: str) -> None:
        self.__last_pop_up_opened = last_pop_up_opened

    def get_ability_HUDs(self) -> list[AbilityHUD]:
        return self.__ability_HUDs

    def set_ability_HUDs(self, ability_HUDs: list[AbilityHUD]) -> None:
        self.__ability_HUDs = ability_HUDs

    def get_xp(self) -> XP:
        return self.__xp

    def set_xp(self, xp: XP) -> None:
        self.__xp = xp

    def get_character_picture_panel(self) -> UIPanel:
        return self.__character_picture_panel

    def set_character_picture_panel(self, character_picture_panel: UIPanel) -> None:
        self.__character_picture_panel = character_picture_panel

    def get_character_picture(self) -> UIImage:
        return self.__character_picture

    def set_character_picture(self, character_picture: UIImage) -> None:
        self.__character_picture = character_picture

    def get_right_arrow_select(self) -> UIButton:
        return self.__right_arrow_select

    def set_right_arrow_select(self, right_arrow_select: UIButton) -> None:
        self.__right_arrow_select = right_arrow_select

    def get_left_arrow_select(self) -> UIButton:
        return self.__left_arrow_select

    def set_left_arrow_select(self, left_arrow_select: UIButton) -> None:
        self.__left_arrow_select = left_arrow_select

    def get_go_button(self) -> UIButton:
        return self.__go_button

    def set_go_button(self, go_button: UIButton) -> None:
        self.__go_button = go_button

    def get_character_info_panel(self) -> UIPanel:
        return self.__character_info_panel

    def set_character_info_panel(self, character_info_panel: UIPanel) -> None:
        self.__character_info_panel = character_info_panel

    def get_character_name(self) -> UITextBox:
        return self.__character_name

    def set_character_name(self, character_name: UITextBox) -> None:
        self.__character_name = character_name

    def get_view_ability_button(self) -> UIButton:
        return self.__view_ability_button

    def set_view_ability_button(self, view_ability_button: UIButton) -> None:
        self.__view_ability_button = view_ability_button

    def get_upgrade_button(self) -> UIButton:
        return self.__upgrade_button

    def set_upgrade_button(self, upgrade_button: UIButton) -> None:
        self.__upgrade_button = upgrade_button

    def get_stat_HUDs(self) -> list[StatisticHUD]:
        return self.__stat_HUDs

    def set_stat_HUDs(self, stat_HUDs: list[StatisticHUD]) -> None:
        self.__stat_HUDs = stat_HUDs

    def get_ability_menu(self) -> UIPanel:
        return self.__ability_menu

    def set_ability_menu(self, ability_menu: UIPanel) -> None:
        self.__ability_menu = ability_menu

    def get_ability_menu_close(self) -> UIButton:
        return self.__ability_menu_close

    def set_ability_menu_close(self, ability_menu_close: UIButton) -> None:
        self.__ability_menu_close = ability_menu_close

    def get_upgrade_character_panel(self) -> list[UIPanel]:
        return self.__upgrade_character_panel

    def set_upgrade_character_panel(
        self, upgrade_character_panel: list[UIPanel]
    ) -> None:
        self.__upgrade_character_panel = upgrade_character_panel

    def get_xp_text(self) -> UITextBox:
        return self.__xp_text

    def set_xp_text(self, xp_text: UITextBox) -> None:
        self.__xp_text = xp_text

    def get_upgrade_confirm(self) -> UIButton:
        return self.__upgrade_confirm

    def set_upgrade_confirm(self, upgrade_confirm: UIButton) -> None:
        self.__upgrade_confirm = upgrade_confirm

    def get_upgrade_cancel(self) -> UIButton:
        return self.__upgrade_cancel

    def set_upgrade_cancel(self, upgrade_cancel: UIButton) -> None:
        self.__upgrade_cancel = upgrade_cancel

    def get_upgrade_dismiss(self) -> UIButton:
        return self.__upgrade_dismiss

    def set_upgrade_dismiss(self, upgrade_dismiss: UIButton) -> None:
        self.__upgrade_dismiss = upgrade_dismiss

    def get_characater_count(self) -> int:
        return self.__characater_count

    def set_characater_count(self, characater_count: int) -> None:
        self.__characater_count = characater_count

    def get_characater_name_list(self) -> list[str]:
        return self.__characater_name_list

    def set_characater_name_list(self, characater_name_list: list[str]) -> None:
        self.__characater_name_list = characater_name_list
