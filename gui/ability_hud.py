import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from ability import Ability
from pygame_gui.core import ObjectID
from characters.players.base_player import BasePlayer


class AbilityHUD:
    __ability_header: UITextBox = None
    __ability_icon: UIImage = None
    __ability_description: UITextBox = None
    __ability_button: UIButton = None

    __ABILITY_BUTTON_TEXT = {
        0: "OWNED",
        1: "Unlocked on LVL 4",
        2: "Unlock for 600 XP",
    }

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        container: UIPanel,
        player: BasePlayer,
        ability: Ability,
        ability_count: int,
    ) -> None:

        ability_init_y = 125
        init_ability_icon_x = init_ability_text_x = 100
        init_ability_title_x = 150
        init_ability_button_x = -100
        ability_y_gap = 150
        self.__ability_header = UITextBox(
            ability.get_name(),
            relative_rect=pygame.Rect(
                (
                    init_ability_title_x,
                    ability_init_y + ability_count * ability_y_gap,
                ),
                (-1, -1),
            ),
            manager=ui_manager,
            container=container,
            object_id=ObjectID(class_id="@sub_title", object_id="#ability_sub_title"),
        )

        self.__ability_icon = UIImage(
            relative_rect=pygame.Rect(
                (
                    init_ability_icon_x,
                    ability_init_y + ability_count * ability_y_gap + 5,
                ),
                (40, 40),
            ),
            image_surface=pygame.image.load(ability.get_icon_URL()),
            manager=ui_manager,
            container=container,
        )

        self.__ability_description = UITextBox(
            ability.get_description(),
            relative_rect=pygame.Rect(
                (
                    init_ability_text_x,
                    ability_init_y + ability_count * ability_y_gap + 50,
                ),
                (screen.width * 0.6, -1),
            ),
            manager=ui_manager,
            container=container,
            object_id=ObjectID(object_id="#ability_text"),
        )

        ability_button_rect = pygame.Rect(
            (0, ability_init_y + ability_count * ability_y_gap), (200, 50)
        )
        ability_button_rect.right = init_ability_button_x
        if ability in player.get_unlocked_abilities():
            self.__ability_button = UIButton(
                relative_rect=ability_button_rect,
                text=self.__ABILITY_BUTTON_TEXT[0],
                manager=ui_manager,
                anchors=({"right": "right"}),
                container=container,
                object_id=ObjectID(class_id="@lock_button"),
            )
        else:
            self.__ability_button = UIButton(
                relative_rect=ability_button_rect,
                text=self.__ABILITY_BUTTON_TEXT[ability_count],
                manager=ui_manager,
                anchors=({"right": "right"}),
                container=container,
                object_id=ObjectID(class_id="@unlock_button"),
            )

    def update(self, player: BasePlayer, ability: Ability, ability_count: int) -> None:
        self.__ability_header.set_text(ability.get_name())
        self.__ability_icon.set_image(pygame.image.load(ability.get_icon_URL()))
        self.__ability_description.set_text(ability.get_description())

        if ability in player.get_unlocked_abilities():
            self.__ability_button.set_text(self.__ABILITY_BUTTON_TEXT[0])
            self.__ability_button.change_object_id(ObjectID(class_id="@lock_button"))
        else:
            self.__ability_button.set_text(self.__ABILITY_BUTTON_TEXT[ability_count])
            self.__ability_button.change_object_id(ObjectID(class_id="@unlock_button"))

    def kill(self) -> None:
        self.__ability_button.kill()
        self.__ability_description.kill()
        self.__ability_icon.kill()
        self.__ability_header.kill()

    def get_ability_button(self) -> UIButton:
        return self.__ability_button
