from .base_state import BaseState
from characters.base_character import BaseCharacter
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from state_manager import GameStateManager
from characters.base_character import BaseCharacter
from xp import XP
from typing import Tuple
from combat_controller import CombatController
from health_bar import HealthBar
import random
from ability import Ability


class TurnBasedFight(BaseState):

    __player: BaseCharacter = None
    __enemy: BaseCharacter = None
    __round_counter: int = 0
    __combat_round_initalised: bool = False
    __player_controller: CombatController = None
    __enemy_controller: CombatController = None
    __player_health_bar: HealthBar = None
    __enemy_health_bar: HealthBar = None
    __ability_selected: Ability = -1
    __ability_button_list: list[UIButton] = [None] * 17
    __attacking: bool = False
    __turn_end: bool = False
    __mouse_pressed: bool = False
    __enemy_hit_height: float = 0

    __xp: XP = None

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

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        player: BaseCharacter,
        enemy: BaseCharacter,
        xp: XP = None,
    ):
        super().__init__(screen, ui_manager, game_state_manager)
        self.__xp = XP()
        self.__player = player
        self.__enemy = enemy

    def start(self) -> None:
        self.__background_image = UIImage(
            relative_rect=pygame.Rect(
                (0, 0), (self.get_screen().get_width(), self.get_screen().get_height())
            ),
            image_surface=pygame.image.load("assets/fight/1.png"),
            manager=self.get_ui_manager(),
        )
        self.__player_sprite = UIImage(
            relative_rect=pygame.Rect(
                (200, 300),
                (200, 200),
            ),
            image_surface=pygame.image.load(self.__player.get_sprite_location()),
            manager=self.get_ui_manager(),
        )
        self.__enemy_sprite = UIImage(
            relative_rect=pygame.Rect(
                (400, 300),
                (200, 200),
            ),
            image_surface=pygame.transform.flip(
                pygame.image.load(self.__enemy.get_sprite_location()).convert_alpha(),
                True,
                False,
            ),
            manager=self.get_ui_manager(),
        )
        self.__player_info_container = UIPanel(
            relative_rect=pygame.Rect((-5, 0), (325, 315)),
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#semi-transparent_panel"),
        )

        # icon_rect = (
        #     pygame.Rect(
        #         (position.right + icon_sprite_gap-icon_size[0],
        #         position.top),
        #         icon_size
        #     )
        #     if self.__flip
        #     else pygame.Rect(
        #         (position.left - icon_sprite_gap,
        #         position.top),
        #         icon_size
        #     )
        # )

        self.__player_health_bar = HealthBar(
            self.get_ui_manager(),
            self.__player_info_container,
            pygame.Rect((100, 20), (225, 30)),
            self.__player.get_statistics()["health_points"],
            self.__player.get_statistics()["health_points"],
        )

        icon_sprite = pygame.transform.scale(
            pygame.image.load("assets/statistics/health_points.webp"), (48, 48)
        )
        UIImage(
            pygame.Rect((50, 40), (48, 48)),
            image_surface=icon_sprite,
            manager=self.get_ui_manager(),
            container=self.__player_info_container,
        )

        self.__player_HUD_text: dict[str, UITextBox] = {}
        HUD_init_text_y = 30
        HUD_text_x = 100
        HUD_step = 30
        for statistic_count, (statistic_name, statistic_value) in enumerate(
            self.__player.get_statistics().items()
        ):
            if (
                statistic_name in self.__CHARACTER_MAX_VAL.keys()
                and statistic_name != "health_points"
            ):
                self.__player_HUD_text[statistic_name] = UITextBox(
                    html_text=f'<img src="assets/icons_18/{statistic_name}.png"> '
                    f"{" ".join(word.capitalize() for word in statistic_name.split("_"))}: {statistic_value}",
                    relative_rect=pygame.Rect(
                        (HUD_text_x, HUD_init_text_y + statistic_count * HUD_step),
                        (-1, -1),
                    ),
                    manager=self.get_ui_manager(),
                    object_id=ObjectID(object_id="#HUD-text"),
                    container=self.__player_info_container,
                )

        enemy_info_rect = pygame.Rect((0, 0), (325, 200))
        enemy_info_rect.right = 5
        self.__enemy_info_container = UIPanel(
            relative_rect=enemy_info_rect,
            anchors={"right": "right"},
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#transparent_panel"),
        )

        enemy_health_bar_rect = pygame.Rect((0, 30), (225, 25))
        enemy_health_bar_rect.right = 225
        self.__enemy_health_bar = HealthBar(
            self.get_ui_manager(),
            self.__enemy_info_container,
            enemy_health_bar_rect,
            self.__enemy.get_statistics()["health_points"],
            self.__enemy.get_statistics()["health_points"],
            flip=True,
        )

        player_choice_container_width = self.get_screen().width - 650
        self.__player_choice_container = UIPanel(
            relative_rect=pygame.Rect((0, 0), (self.get_screen().width - 650, 200)),
            anchors={"centerx": "centerx"},
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#transparent_panel"),
        )

        self.__tutorial_text = UITextBox(
            html_text="Press the allocated button to use an action (ability / normal attack)",
            relative_rect=pygame.Rect((0, 200), (self.get_screen().width * 0.4, -1)),
            anchors=({"centerx": "centerx"}),
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#tutorial_text"),
        )

        unlocked_abilities_number = len(self.__player.get_unlocked_abilities())
        ability_x_gap = (
            player_choice_container_width - (unlocked_abilities_number + 1) * 125
        ) / (unlocked_abilities_number + 2)
        init_ability_button_y = 25

        normal_attack_tool_tip = f"Deal {self.__player.get_statistics()['physical_damage'] if "physical_damage" in self.__player.get_statistics().keys() else 0} physical damage and {self.__player.get_statistics()['magical_damage'] if "magical_damage" in self.__player.get_statistics().keys() else 0} magical damage to the enemy"
        self.__ability_button_list[0] = UIButton(
            text="Normal Attack",
            relative_rect=pygame.Rect(
                (ability_x_gap, init_ability_button_y),
                (125, 100),
            ),
            manager=self.get_ui_manager(),
            container=self.__player_choice_container,
            object_id=ObjectID(class_id="@Normal Attack", object_id="#choice_text0"),
            tool_tip_text=normal_attack_tool_tip,
        )
        for ability_count, ability in enumerate(self.__player.get_unlocked_abilities()):

            self.__ability_button_list[ability_count + 1] = UIButton(
                text=ability.get_name(),
                relative_rect=pygame.Rect(
                    (
                        ability_x_gap + (ability_count + 1) * 125 + ability_x_gap,
                        init_ability_button_y,
                    ),
                    (125, 100),
                ),
                manager=self.get_ui_manager(),
                container=self.__player_choice_container,
                object_id=ObjectID(
                    class_id=f"@{ability.get_name()}",
                    object_id=f"#choice_text{ability_count + 1}",
                ),
                tool_tip_text=ability.get_description(),
            )

        visual_dialogue_rect = pygame.Rect((0, 0), (self.get_screen().width, 150))
        visual_dialogue_rect.bottom = 0
        self.__visual_dialogue = UIPanel(
            relative_rect=visual_dialogue_rect,
            manager=self.get_ui_manager(),
            anchors={"bottom": "bottom"},
            object_id=ObjectID(object_id="#visual_dialogue_box"),
        )

        self.__player_controller = CombatController(self.__player, self.__player_sprite)
        self.__enemy_controller = CombatController(self.__enemy, self.__enemy_sprite)

    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.__ability_button_list[0]:
                self.__ability_selected = None
            else:
                for ability_button_index in [1, 2, 3]:
                    if (
                        event.ui_element
                        == self.__ability_button_list[ability_button_index]
                    ):
                        self.__ability_selected = (
                            self.__player.get_unlocked_abilities()[
                                ability_button_index - 1
                            ]
                        )

        if pygame.mouse.get_pressed()[0]:
            self.__mouse_pressed = True
            mouse_pos = pygame.mouse.get_pos()
            if self.__enemy_sprite.rect.collidepoint(mouse_pos):
                self.__enemy_hit_height = self.__enemy_sprite.rect.height - (
                    mouse_pos[1] - self.__enemy_sprite.rect.y
                )
            else:
                self.__enemy_hit_height = 0

    def run(self) -> None:
        self.__combat_round_initalised = True
        if not self.__combat_round_initalised:
            pass  # Initialize the combat round - 3,2,1 GO

        if (
            self.__enemy.get_statistics()["health_points"] > 0
            and self.__player.get_statistics()["health_points"] > 0
            and self.__combat_round_initalised
        ):
            if self.__round_counter % 2 == 0:
                # When the user has not picked the ability to use and is not stunned
                if (
                    self.__ability_selected == -1
                    and not self.__player_controller.is_stunned()
                ):
                    self.__tutorial_text.set_text(
                        "Press the allocated button to use an action (ability / normal attack)"
                    )

                elif not self.__attacking:  # When the user is aiming for the enemies
                    if self.__player_controller.is_stunned():
                        self.__tutorial_text.set_text("You are stunned and cannot act!")
                    else:
                        locked_ability_decision = (
                            self.__ability_selected
                        )  # lock in to the ability selected
                        self.__tutorial_text.set_text(
                            "Use your mouse to try and hit the enemy's key body parts! You only have one chance!"
                        )

                    # If the user has clicked, then attack with the given values
                    if self.__mouse_pressed or self.__player_controller.is_stunned():
                        print(self.__player.get_statistics())
                        print(self.__enemy.get_statistics())
                        self.__attacking = True
                        # Regenerate before turn action occurs
                        self.__player_controller.regenerate()
                        self.__enemy_controller.regenerate()
                        # Compute damage and debuffs, apply buffs
                        physical_damage, magical_damage, debuff_dict = (
                            self.__player_controller.attack(
                                self.__enemy_hit_height, locked_ability_decision
                            )
                        )
                        # Apply the damage and debuffs to the enemy
                        self.__enemy_controller.face_damage(
                            physical_damage, magical_damage, debuff_dict
                        )
                        print(self.__player.get_statistics())
                        print(self.__enemy.get_statistics())
                elif (
                    self.__attacking and not self.__turn_end
                ):  # Attacking, perform animation, update the health bars
                    self.__turn_end = True
                elif self.__turn_end:

                    self.__ability_selected = -1  # Reset turn action flags
                    self.__attacking = False
                    self.__round_counter += 1

                # Regeneration
            else:
                random_choice = random.randint(0, 4)
                print("enemy round")
                self.__round_counter += 1
                # if random_choice == 4:
                #     self.__enemy_controller.attack(0)
                # else:
                #     self.__enemy_controller.attack(0, self.__enemy.get_abilities()[random_choice])

        if self.__enemy.get_statistics()["health_points"] <= 0:
            # Enemy died
            pass
        elif self.__player.get_statistics()["health_points"] <= 0:
            # Player died
            pass
        else:
            # Draw
            pass

    def reset_event_polling(self) -> None:
        self.__mouse_pressed = False

    def render(self, time_delta):
        self.__player_health_bar.update(self.__player.get_statistics()["health_points"])
        self.__enemy_health_bar.update(self.__enemy.get_statistics()["health_points"])

        for ability in self.__player.get_unlocked_abilities():
            if self.__player_controller.is_ability_on_cooldown(ability):
                self.__ability_button_list[
                    self.__player.get_unlocked_abilities().index(ability) + 1
                ].disable()
            else:
                self.__ability_button_list[
                    self.__player.get_unlocked_abilities().index(ability) + 1
                ].enable()

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
