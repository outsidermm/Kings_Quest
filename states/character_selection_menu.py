from .base_state import BaseState
from characters.base_character import BaseCharacter
import pygame, pygame_gui
from state_manager import GameStateManager
from characters.base_character import BaseCharacter
from xp import XP

#TODO Upgrades made
class StatisticBar(pygame_gui.elements.UIStatusBar):
    def __init__(
        self,
        text: str = None,
        *args,
        **kwargs,
    ):
        self.__bar_text = text
        super().__init__(*args, **kwargs)

    def status_text(self) -> str:
        return self.__bar_text

    def set_text(self, text: str):
        self.__bar_text = text


class CharacterSelectionMenu(BaseState):

    __characters: list[BaseCharacter] = None
    __selection_page = 0
    __game_start: bool = False
    __upgrade_character: bool = False
    __left_switch_character: bool = False
    __right_switch_character: bool = False
    __ability_menu_active: bool = False
    __purchase_upgrade = False
    __dismiss_upgrade = False
    __dismiss_upgrade = False
    __character_switch: bool = False
    __refund_upgrade: bool = False
    __purchase_ability = False
    __last_pop_up_opened: str = None

    __xp: XP = None

    # Define maximum values for the bars for normalization
    __CHARACTER_MAX_VAL: dict[str | float] = {
        "health_points": 1150,  # Berserker's 1000 + 150 upgrade
        "physical_defense": 200,  # Warrior
        "magical_defense": 100,  # Mage
        "spell_power": 135,  # Mage's 120 + 15 upgrade
        "physical_power": 200,  # Warrior's 90 + 90 upgrade
        "health_regeneration": 15,  # Berserker
        "mana_regeneration": 5,  # Mage
        "mana_points": 250,  # Mage's 200 + 50 upgrade
        "physical_damage": 110,  # Berserker
        "magical_damage": 30,  # Mage
    }

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        characters: list[BaseCharacter],
        xp: XP = None,
    ):
        super().__init__(screen, ui_manager, game_state_manager)
        self.__characters = characters
        self.__characater_count = len(characters)
        self.__characater_name_list = [character.get_name() for character in characters]
        self.__xp = XP()

    def progress_bar(self, statistic: str) -> float:
        return (
            self.get_characters()[self.__selection_page].get_statistics()[statistic]
            / self.__CHARACTER_MAX_VAL[statistic]
            if statistic
            in self.get_characters()[self.__selection_page].get_statistics().keys()
            else 0
        )

    def start(self) -> None:
        self.__character_picture_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (0, 0), (self.get_screen().height, self.get_screen().width * 0.6)
            ),
            manager=self.get_ui_manager(),
            object_id=pygame_gui.core.ObjectID(class_id="@character_pic_panel"),
        )

        self.__character_picture = pygame_gui.elements.UIImage(
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
            pygame_gui.elements.UIButton(
                relative_rect=right_arrow,
                text="→",
                manager=self.get_ui_manager(),
                anchors=({"right": "right", "bottom": "bottom"}),
                container=self.__character_picture_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@arrow"),
            )
        )

        left_arrow = pygame.Rect((50, 0), (125, 70))
        left_arrow.bottom = -75
        self.set_left_arrow_select(
            pygame_gui.elements.UIButton(
                relative_rect=left_arrow,
                text="←",
                manager=self.get_ui_manager(),
                anchors=({"bottom": "bottom"}),
                container=self.__character_picture_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@arrow"),
            )
        )

        select_rect = pygame.Rect((0, 0), (125, 70))
        select_rect.bottom = -75
        self.__go_button = pygame_gui.elements.UIButton(
            relative_rect=select_rect,
            text="START",
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx", "bottom": "bottom"}),
            container=self.__character_picture_panel,
            object_id=pygame_gui.core.ObjectID(class_id="@go_button"),
        )

        right_info = pygame.Rect(
            (0, 0), (self.get_screen().width * 0.45, self.get_screen().height)
        )
        right_info.right = 0
        self.__character_info_panel = pygame_gui.elements.UIPanel(
            relative_rect=right_info,
            manager=self.get_ui_manager(),
            anchors=({"right": "right"}),
            object_id=pygame_gui.core.ObjectID(class_id="@character_info_panel"),
        )

        self.__character_name = pygame_gui.elements.UITextBox(
            self.__characater_name_list[0],
            relative_rect=pygame.Rect((50, 30), (-1, -1)),
            manager=self.get_ui_manager(),
            anchors=({"left": "left"}),
            container=self.__character_info_panel,
            object_id=pygame_gui.core.ObjectID(
                class_id="@sub_title", object_id="#character_name"
            ),
        )

        ability_rec = pygame.Rect((0, 0), (475, 60))
        ability_rec.bottom = -35
        self.__view_ability_button = pygame_gui.elements.UIButton(
            relative_rect=ability_rec,
            text="View Abilities",
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx", "bottom": "bottom"}),
            container=self.__character_info_panel,
            object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
        )

        upgrade_button_location = pygame.Rect((50, 30), (200, 60))
        upgrade_button_location.right = -50
        if self.get_characters()[self.__selection_page].get_character_level() == 1:
            self.__upgrade_button = pygame_gui.elements.UIButton(
                relative_rect=upgrade_button_location,
                text="Upgrade for 200 XP",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                container=self.__character_info_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
            )
        elif self.get_characters()[self.__selection_page].get_character_level() == 2:
            self.__upgrade_button = pygame_gui.elements.UIButton(
                relative_rect=upgrade_button_location,
                text="Upgrade for 400 XP",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                container=self.__character_info_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
            )
        elif self.get_characters()[self.__selection_page].get_character_level() == 3:
            self.__upgrade_button = pygame_gui.elements.UIButton(
                relative_rect=upgrade_button_location,
                text="Upgrade for 800 XP",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                container=self.__character_info_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
            )
        else:
            self.__upgrade_button = pygame_gui.elements.UIButton(
                relative_rect=upgrade_button_location,
                text="MAX LEVEL",
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                container=self.__character_info_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@lock_button"),
            )

        init_img_x = 50
        init_text_x = 100
        init_bar_x = 300
        init_y = 108
        gap_per_statistics = 50
        self.__statistic_img: list[pygame_gui.elements.UIImage] = [None] * len(
            self.__CHARACTER_MAX_VAL
        )
        self.__statistic_text: list[pygame_gui.elements.UITextBox] = [None] * len(
            self.__CHARACTER_MAX_VAL
        )
        self.__statistic_bar: list[StatisticBar] = [None] * len(
            self.__CHARACTER_MAX_VAL
        )

        for statistic_count, (statistic, value) in enumerate(
            self.__CHARACTER_MAX_VAL.items()
        ):
            self.__statistic_img[statistic_count] = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(
                    (init_img_x, init_y + statistic_count * gap_per_statistics + 5),
                    (40, 40),
                ),
                image_surface=pygame.image.load(f"assets/statistics/{statistic}.webp"),
                manager=self.get_ui_manager(),
                container=self.__character_info_panel,
            )

            self.__statistic_text[statistic_count] = pygame_gui.elements.UITextBox(
                " ".join(word.capitalize() for word in statistic.split("_")),
                relative_rect=pygame.Rect(
                    (init_text_x, init_y + statistic_count * gap_per_statistics),
                    (300, -1),
                ),
                manager=self.get_ui_manager(),
                anchors=({"left": "left"}),
                container=self.__character_info_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@statistic_text"),
            )

            bar_location = pygame.Rect(
                (init_bar_x, init_y + statistic_count * gap_per_statistics + 12.5),
                (200, 30),
            )
            bar_location.right = -50
            numerical_statistic = (
                self.get_characters()[self.__selection_page].get_statistics()[statistic]
                if statistic
                in self.get_characters()[self.__selection_page].get_statistics().keys()
                else 0
            )

            self.__statistic_bar[statistic_count] = StatisticBar(
                relative_rect=bar_location,
                manager=self.get_ui_manager(),
                anchors=({"right": "right"}),
                percent_method=(lambda stat=statistic: self.progress_bar(stat)),
                container=self.__character_info_panel,
                object_id=pygame_gui.core.ObjectID(class_id="@statistics_bar"),
                text=f"{numerical_statistic}/{self.__CHARACTER_MAX_VAL[statistic]}",
            )

        self.__ability_menu = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (0, 0),
                (self.get_screen().width * 0.95, self.get_screen().height * 0.95),
            ),
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=pygame_gui.core.ObjectID(class_id="@ability_menu"),
            starting_height=2,
            visible=False,
        )

        ability_menu_close_button_rect = pygame.Rect((0, 0), (150, 50))
        ability_menu_close_button_rect.right = -100
        ability_menu_close_button_rect.bottom = -100

        self.__ability_menu_header = pygame_gui.elements.UITextBox(
            "ABILITIES",
            relative_rect=pygame.Rect((-100, 50), (-1, -1)),
            manager=self.get_ui_manager(),
            anchors=({"centerx": "centerx"}),
            container=self.__ability_menu,
            object_id=pygame_gui.core.ObjectID(
                class_id="@sub_title", object_id="#ability_header"
            ),
        )

        self.__ability_menu_close = pygame_gui.elements.UIButton(
            relative_rect=ability_menu_close_button_rect,
            text="CLOSE",
            manager=self.get_ui_manager(),
            anchors=({"right": "right", "bottom": "bottom"}),
            container=self.__ability_menu,
            object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
        )

        ability_init_y = 125
        init_ability_icon_x = init_ability_text_x = 100
        init_ability_title_x = 150
        init_ability_button_x = -100
        ability_y_gap = 150

        self.__ability_header: list[pygame_gui.elements.UITextBox] = [None] * 3
        self.__ability_description: list[pygame_gui.elements.UITextBox] = [None] * 3
        self.__ability_icon: list[pygame_gui.elements.UIImage] = [None] * 3
        self.__ability_button_list: list[pygame_gui.elements.UIButton] = [None] * 3

        ability_button_text = {
            0: "OWNED",
            1: "Unlocked on LVL 4",
            2: "Unlock for 600 XP",
        }

        for ability_count, ability in enumerate(
            self.get_characters()[self.__selection_page].get_ability_list()
        ):
            self.__ability_header[ability_count] = pygame_gui.elements.UITextBox(
                ability.get_name(),
                relative_rect=pygame.Rect(
                    (
                        init_ability_title_x,
                        ability_init_y + ability_count * ability_y_gap,
                    ),
                    (-1, -1),
                ),
                manager=self.get_ui_manager(),
                container=self.__ability_menu,
                object_id=pygame_gui.core.ObjectID(
                    class_id="@sub_title", object_id="#ability_sub_title"
                ),
            )

            self.__ability_icon[ability_count] = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(
                    (
                        init_ability_icon_x,
                        ability_init_y + ability_count * ability_y_gap + 5,
                    ),
                    (40, 40),
                ),
                image_surface=pygame.image.load(ability.get_icon_URL()),
                manager=self.get_ui_manager(),
                container=self.__ability_menu,
            )

            self.__ability_description[ability_count] = pygame_gui.elements.UITextBox(
                ability.get_description(),
                relative_rect=pygame.Rect(
                    (
                        init_ability_text_x,
                        ability_init_y + ability_count * ability_y_gap + 50,
                    ),
                    (self.get_screen().width * 0.6, -1),
                ),
                manager=self.get_ui_manager(),
                container=self.__ability_menu,
                object_id=pygame_gui.core.ObjectID(object_id="#ability_text"),
            )

            ability_button_rect = pygame.Rect(
                (0, ability_init_y + ability_count * ability_y_gap), (200, 50)
            )
            ability_button_rect.right = -100
            if (
                ability
                in self.get_characters()[self.__selection_page].get_unlocked_abilities()
            ):
                self.__ability_button_list[ability_count] = (
                    pygame_gui.elements.UIButton(
                        relative_rect=ability_button_rect,
                        text=ability_button_text[0],
                        manager=self.get_ui_manager(),
                        anchors=({"right": "right"}),
                        container=self.__ability_menu,
                        object_id=pygame_gui.core.ObjectID(class_id="@lock_button"),
                    )
                )
            else:
                self.__ability_button_list[ability_count] = (
                    pygame_gui.elements.UIButton(
                        relative_rect=ability_button_rect,
                        text=ability_button_text[ability_count],
                        manager=self.get_ui_manager(),
                        anchors=({"right": "right"}),
                        container=self.__ability_menu,
                        object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
                    )
                )

        self.__upgrade_character_panel: list[pygame_gui.elements.UIPanel] = [None] * 2
        self.__upgrade_character_panel[0] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (0, 0),
                (self.get_screen().width * 0.4, self.get_screen().height * 0.5),
            ),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            starting_height=3,
            object_id=pygame_gui.core.ObjectID(class_id="@character_pic_panel"),
            visible=False,
        )

        self.__upgrade_character_panel[1] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (0, 0),
                (self.get_screen().width * 0.4, self.get_screen().height * 0.5),
            ),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            starting_height=3,
            object_id=pygame_gui.core.ObjectID(class_id="@character_pic_panel"),
            visible=False,
        )
        self.__xp_text = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect((-100, -100), (-1, -1)),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            container=self.__upgrade_character_panel[1],
            object_id=pygame_gui.core.ObjectID(object_id="#upgrade_menu_text"),
        )

        self.__upgrade_confirm = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 75), (150, 50)),
            text="CONFIRM",
            manager=self.get_ui_manager(),
            anchors=({"left": "left", "centery": "centery"}),
            container=self.__upgrade_character_panel[1],
            object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
        )

        cancel_button_rect = pygame.Rect((0, 75), (150, 50))
        cancel_button_rect.right = -50
        self.__upgrade_cancel = pygame_gui.elements.UIButton(
            relative_rect=cancel_button_rect,
            text="CANCEL",
            manager=self.get_ui_manager(),
            anchors=({"right": "right", "centery": "centery"}),
            container=self.__upgrade_character_panel[1],
            object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
        )

        self.__lack_of_xp = pygame_gui.elements.UITextBox(
            "Not enough XP!",
            relative_rect=pygame.Rect((-100, -100), (-1, -1)),
            anchors=({"center": "center"}),
            manager=self.get_ui_manager(),
            container=self.__upgrade_character_panel[0],
            object_id=pygame_gui.core.ObjectID(object_id="#upgrade_menu_text"),
        )
        self.__upgrade_dismiss = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 100), (150, 50)),
            text="OK",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__upgrade_character_panel[0],
            object_id=pygame_gui.core.ObjectID(class_id="@unlock_button"),
        )

    def handle_events(self, event: pygame.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.get_left_arrow_select():
                self.__left_switch_character = True
            if event.ui_element == self.get_right_arrow_select():
                self.__right_switch_character = True
            if event.ui_element == self.__upgrade_button:
                self.__upgrade_character = True
            if event.ui_element == self.__go_button:
                self.__game_start = True
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
            if event.ui_element == self.__ability_button_list[2]:
                self.__purchase_ability = True

    def run(self):
        if self.__left_switch_character:
            self.__character_switch = True
            self.__selection_page = (
                self.__selection_page - 1
            ) % self.__characater_count
        elif self.__right_switch_character:
            self.__selection_page = (
                self.__selection_page + 1
            ) % self.__characater_count
            self.__character_switch = True

        if self.__character_switch:
            self.__character_name.set_text(
                self.__characater_name_list[self.__selection_page]
            )
            self.__character_picture.set_image(
                pygame.image.load(
                    self.get_characters()[self.__selection_page].get_sprite_location()
                ).convert_alpha()
            )

            for statistic_count, (statistic, value) in enumerate(
                self.__CHARACTER_MAX_VAL.items()
            ):

                numerical_statistic = (
                    self.get_characters()[self.__selection_page].get_statistics()[
                        statistic
                    ]
                    if statistic
                    in self.get_characters()[self.__selection_page]
                    .get_statistics()
                    .keys()
                    else 0
                )
                self.__statistic_bar[statistic_count].set_text(
                    f"{numerical_statistic}/{self.__CHARACTER_MAX_VAL[statistic]}"
                )
                self.__statistic_bar[statistic_count].redraw()

            if self.get_characters()[self.__selection_page].get_character_level() == 1:
                self.__upgrade_button.set_text("Upgrade for 200 XP")
                self.__upgrade_button.change_object_id(
                    pygame_gui.core.ObjectID(class_id="@unlock_button")
                )
            elif (
                self.get_characters()[self.__selection_page].get_character_level() == 2
            ):
                self.__upgrade_button.set_text("Upgrade for 400 XP")
                self.__upgrade_button.change_object_id(
                    pygame_gui.core.ObjectID(class_id="@unlock_button")
                )
            elif (
                self.get_characters()[self.__selection_page].get_character_level() == 3
            ):
                self.__upgrade_button.set_text("Upgrade for 800 XP")
                self.__upgrade_button.change_object_id(
                    pygame_gui.core.ObjectID(class_id="@unlock_button")
                )
            else:
                self.__upgrade_button.set_text("MAX LEVEL")
                self.__upgrade_button.change_object_id(
                    pygame_gui.core.ObjectID(class_id="@lock_button")
                )

            for ability_count, ability in enumerate(
                self.get_characters()[self.__selection_page].get_ability_list()
            ):
                self.__ability_header[ability_count].set_text(ability.get_name())
                self.__ability_icon[ability_count].set_image(
                    pygame.image.load(ability.get_icon_URL())
                )
                self.__ability_description[ability_count].set_text(
                    ability.get_description()
                )

                ability_button_text = {
                    0: "OWNED",
                    1: "Unlocked on LVL 4",
                    2: "Unlock for 600 XP",
                }
                if (
                    ability
                    in self.get_characters()[
                        self.__selection_page
                    ].get_unlocked_abilities()
                ):
                    self.__ability_button_list[ability_count].set_text(
                        ability_button_text[0]
                    )
                    self.__ability_button_list[ability_count].change_object_id(
                        pygame_gui.core.ObjectID(class_id="@lock_button")
                    )
                else:
                    self.__ability_button_list[ability_count].set_text(
                        ability_button_text[ability_count]
                    )
                    self.__ability_button_list[ability_count].change_object_id(
                        pygame_gui.core.ObjectID(class_id="@unlock_button")
                    )

        self.__character_switch = False
        if self.__ability_menu_active:
            self.__ability_menu.show()
        else:
            self.__ability_menu.hide()

        xp_expense = {
            1: 200,
            2: 400,
            3: 800,
        }

        if self.__upgrade_character and self.get_characters()[self.__selection_page].get_character_level() < 4:
            self.__last_pop_up_opened = "character"
            self.__character_info_panel.disable()
            self.__character_picture_panel.disable()

            old_xp = self.__xp.get_xp()
            try:
                self.__xp.lose_xp(
                    xp_expense[
                        self.get_characters()[
                            self.__selection_page
                        ].get_character_level()
                    ]
                )
                self.__xp_text.set_text(
                    f"Old XP: {old_xp}\nNew XP: {self.__xp.get_xp()}"
                )
                self.__upgrade_character_panel[1].show()
                self.__upgrade_character_panel[0].hide()
            except:
                self.__upgrade_character_panel[1].hide()
                self.__upgrade_character_panel[0].show()

        self.__upgrade_character = False


        if self.__dismiss_upgrade and self.__last_pop_up_opened == "character":
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[0].hide()
            self.__dismiss_upgrade = False

        if self.__purchase_upgrade and self.__last_pop_up_opened == "character":
            self.get_characters()[self.__selection_page].upgrade()
            self.__purchase_upgrade = False
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()
            self.__character_switch = True

        if self.__refund_upgrade and self.__last_pop_up_opened == "character":
            self.__xp.gain_xp(
                xp_expense[
                    self.get_characters()[self.__selection_page].get_character_level()
                ]
            )
            self.__refund_upgrade = False
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()

        UNLOCK_ABILITY_COST = 600
        if self.__purchase_ability and self.__characters[self.__selection_page].get_ability_list()[2] not in self.__characters[self.__selection_page].get_unlocked_abilities():
            self.__last_pop_up_opened = "ability"
            self.__character_info_panel.disable()
            self.__character_picture_panel.disable()

            old_xp = self.__xp.get_xp()
            try:
                self.__xp.lose_xp(UNLOCK_ABILITY_COST)
                self.__xp_text.set_text(
                    f"Old XP: {old_xp}\nNew XP: {self.__xp.get_xp()}"
                )
                self.__upgrade_character_panel[1].show()
                self.__upgrade_character_panel[0].hide()
            except:
                self.__upgrade_character_panel[1].hide()
                self.__upgrade_character_panel[0].show()
        self.__purchase_ability = False

        if self.__dismiss_upgrade and self.__last_pop_up_opened == "ability":
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[0].hide()
            self.__dismiss_upgrade = False

        if self.__purchase_upgrade and self.__last_pop_up_opened == "ability":
            print("1")
            self.get_characters()[self.__selection_page].unlock_ability()
            print(self.get_characters()[self.__selection_page].get_unlocked_abilities())
            self.__purchase_upgrade = False
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()
            self.__character_switch = True

        if self.__refund_upgrade and self.__last_pop_up_opened == "ability":
            self.__xp.gain_xp(
                xp_expense[
                    self.get_characters()[self.__selection_page].get_character_level()
                ]
            )
            self.__refund_upgrade = False
            self.__character_info_panel.enable()
            self.__character_picture_panel.enable()
            self.__upgrade_character_panel[1].hide()

        if self.__game_start:
            pass
            # self.get_game_state_manager().set_state("gameplay")

    def reset_event_polling(self) -> None:
        self.__left_switch_character = False
        self.__right_switch_character = False

    def render(self, time_delta):
        pass

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

    def get_characters(self) -> list[BaseCharacter]:
        return self.__characters

    def set_characters(self, characters: list[BaseCharacter]) -> None:
        self.__characters = characters

    def get_right_arrow_select(self) -> pygame_gui.elements.UIButton:
        return self.__right_arrow_select

    def set_right_arrow_select(
        self, right_arrow_select: pygame_gui.elements.UIButton
    ) -> None:
        self.__right_arrow_select = right_arrow_select

    def get_left_arrow_select(self) -> pygame_gui.elements.UIButton:
        return self.__left_arrow_select

    def set_left_arrow_select(
        self, left_arrow_select: pygame_gui.elements.UIButton
    ) -> None:
        self.__left_arrow_select = left_arrow_select
