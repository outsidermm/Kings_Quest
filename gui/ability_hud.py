import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from ability import Ability
from pygame_gui.core import ObjectID
from characters.players.base_player import BasePlayer


class AbilityHUD:
    """
    HUD for displaying ability information including icon, description, and unlock status.

    Attributes:
        __ability_header (UITextBox): The text box for the ability name.
        __ability_icon (UIImage): The image for the ability icon.
        __ability_description (UITextBox): The text box for the ability description.
        __ability_button (UIButton): The button for unlocking or displaying ability status.
        __ABILITY_BUTTON_TEXT (dict[int, str]): Dictionary mapping ability status to button text.
    """

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
        """
        Initializes the AbilityHUD with the provided parameters.

        :param screen: The game screen.
        :param ui_manager: Manager for the UI elements.
        :param container: The container panel for the HUD.
        :param player: The player character.
        :param ability: The ability to display.
        :param ability_count: The index of the ability in the player's ability list.
        """
        ability_init_y = 125
        init_ability_icon_x = init_ability_text_x = 100
        init_ability_title_x = 150
        init_ability_button_x = -100
        ability_y_gap = 150

        # Initialize the ability header (name)
        self.set_ability_header(
            UITextBox(
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
                object_id=ObjectID(
                    class_id="@sub_title", object_id="#ability_sub_title"
                ),
            )
        )

        # Initialize the ability icon
        self.set_ability_icon(
            UIImage(
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
        )

        # Initialize the ability description
        self.set_ability_description(
            UITextBox(
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
        )

        ability_button_rect = pygame.Rect(
            (0, ability_init_y + ability_count * ability_y_gap), (200, 50)
        )
        ability_button_rect.right = init_ability_button_x

        # Initialize the ability button based on unlock status
        if ability in player.get_unlocked_abilities():
            self.set_ability_button(
                UIButton(
                    relative_rect=ability_button_rect,
                    text=self.get_ability_button_text()[0],
                    manager=ui_manager,
                    anchors=({"right": "right"}),
                    container=container,
                    object_id=ObjectID(class_id="@lock_button"),
                )
            )
        else:
            self.set_ability_button(
                UIButton(
                    relative_rect=ability_button_rect,
                    text=self.get_ability_button_text()[ability_count],
                    manager=ui_manager,
                    anchors=({"right": "right"}),
                    container=container,
                    object_id=ObjectID(class_id="@unlock_button"),
                )
            )

    def update(self, player: BasePlayer, ability: Ability, ability_count: int) -> None:
        """
        Updates the ability HUD with the current ability details.

        :param player: The player character.
        :param ability: The ability to update.
        :param ability_count: The index of the ability in the player's ability list.
        """
        # Update the ability header (name)
        self.get_ability_header().set_text(ability.get_name())
        # Update the ability icon image
        self.get_ability_icon().set_image(pygame.image.load(ability.get_icon_URL()))
        # Update the ability description
        self.get_ability_description().set_text(ability.get_description())

        # Update the ability button based on unlock status
        if ability in player.get_unlocked_abilities():
            self.get_ability_button().set_text(self.get_ability_button_text()[0])
            self.get_ability_button().change_object_id(
                ObjectID(class_id="@lock_button")
            )
        else:
            self.get_ability_button().set_text(
                self.get_ability_button_text()[ability_count]
            )
            self.get_ability_button().change_object_id(
                ObjectID(class_id="@unlock_button")
            )

    def kill(self) -> None:
        """
        Kills (removes) all HUD elements.
        """
        self.get_ability_header().kill()
        self.get_ability_icon().kill()
        self.get_ability_description().kill()
        self.get_ability_button().kill()

    # Getters and Setters for encapsulation and data protection
    def get_ability_button(self) -> UIButton:
        """
        Gets the ability button.

        :return: The ability button.
        """
        return self.__ability_button

    def set_ability_button(self, ability_button: UIButton) -> None:
        """
        Sets the ability button.

        :param ability_button: The ability button to set.
        """
        self.__ability_button = ability_button

    def get_ability_header(self) -> UITextBox:
        """
        Gets the ability header text box.

        :return: The ability header text box.
        """
        return self.__ability_header

    def set_ability_header(self, ability_header: UITextBox) -> None:
        """
        Sets the ability header text box.

        :param ability_header: The ability header text box to set.
        """
        self.__ability_header = ability_header

    def get_ability_icon(self) -> UIImage:
        """
        Gets the ability icon image.

        :return: The ability icon image.
        """
        return self.__ability_icon

    def set_ability_icon(self, ability_icon: UIImage) -> None:
        """
        Sets the ability icon image.

        :param ability_icon: The ability icon image to set.
        """
        self.__ability_icon = ability_icon

    def get_ability_description(self) -> UITextBox:
        """
        Gets the ability description text box.

        :return: The ability description text box.
        """
        return self.__ability_description

    def set_ability_description(self, ability_description: UITextBox) -> None:
        """
        Sets the ability description text box.

        :param ability_description: The ability description text box to set.
        """
        self.__ability_description = ability_description

    def get_ability_button_text(self) -> dict[int, str]:
        """
        Gets the ability button text dictionary.

        :return: The ability button text dictionary.
        """
        return self.__ABILITY_BUTTON_TEXT