from .base_state import BaseState
from characters.base_character import BaseCharacter
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from state_manager import GameStateManager
from characters.base_character import BaseCharacter
from xp import XP
from gui.combat_hud import CombatHUD
from combat_controller import CombatController
import random
from ability import Ability
from gui.combat_hud import CombatHUD
from animator import Animation
from utilities import load_images


class TurnBasedFight(BaseState):

    __player: BaseCharacter = None
    __enemy: BaseCharacter = None
    __round_counter: int = 0
    __combat_round_initalised: bool = False
    __player_controller: CombatController = None
    __enemy_controller: CombatController = None
    __player_HUD: CombatHUD = None
    __enemy_HUD: CombatHUD = None
    __ability_selected: Ability = -1
    __ability_button_list: list[UIButton] = [None] * 4
    __is_player_attacking: bool = False
    __mouse_pressed: bool = False
    __enemy_hit_height: float = 0
    __player_animation: Animation = None
    __enemy_animation: Animation = None
    __is_enemy_attacking: bool = False
    __quit_button_pressed: bool = False

    __xp: XP = None
    __ANIMATION_ASSETS: dict[str, Animation] = {}

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        enemy: BaseCharacter,
        xp: XP = None,
    ):
        super().__init__(
            "turn_based_fight",
            screen,
            ui_manager,
            "level_selection_menu",
            game_state_manager,
        )
        self.__xp = XP()
        self.__enemy = enemy

        self.__ANIMATION_ASSETS["enemy/idle"] = Animation(
            load_images(f"characters/{self.__enemy.get_name()}/idle"),
            is_flipped=True,
        )
        self.__ANIMATION_ASSETS["enemy/attack"] = Animation(
            load_images(f"characters/{self.__enemy.get_name()}/attack"),
            image_duration=6,
            loop=False,
            is_flipped=True,
        )

    def start(self) -> None:
        self.__player = self.get_incoming_transition_data()["player"]

        self.__ANIMATION_ASSETS["player/idle"] = Animation(
            load_images(f"characters/{self.__player.get_name()}/idle"),
            image_duration=10,
        )
        self.__ANIMATION_ASSETS["player/attack"] = Animation(
            load_images(f"characters/{self.__player.get_name()}/attack"),
            image_duration=6,
            loop=False,
        )

        self.__background_image = UIImage(
            relative_rect=pygame.Rect(
                (0, 0), (self.get_screen().get_width(), self.get_screen().get_height())
            ),
            image_surface=pygame.image.load("assets/fight/1.png"),
            manager=self.get_ui_manager(),
        )
        self.__player_sprite = UIImage(
            relative_rect=pygame.Rect(
                (self.get_screen().width * 0.3, 300),
                (200, 200),
            ),
            image_surface=pygame.image.load(self.__player.get_sprite_location()),
            manager=self.get_ui_manager(),
        )
        self.__enemy_sprite = UIImage(
            relative_rect=pygame.Rect(
                (self.get_screen().width * 0.5, 350),
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
            relative_rect=pygame.Rect((-5, 0), (325, 330)),
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#semi-transparent_panel"),
        )

        self.__player_HUD = CombatHUD(
            self.get_ui_manager(), self.__player, self.__player_info_container
        )

        enemy_info_rect = pygame.Rect((0, 0), (325, 330))
        enemy_info_rect.right = 5
        self.__enemy_info_container = UIPanel(
            relative_rect=enemy_info_rect,
            anchors={"right": "right"},
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#semi-transparent_panel"),
        )

        self.__enemy_HUD = CombatHUD(
            self.get_ui_manager(),
            self.__enemy,
            self.__enemy_info_container,
            is_flipped=True,
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
            player_choice_container_width - (unlocked_abilities_number + 1) * 130
        ) / (unlocked_abilities_number + 2)
        init_ability_button_y = 25

        normal_attack_tool_tip = f"Deal {self.__player.get_statistics()['physical_damage'] if "physical_damage" in self.__player.get_statistics().keys() else 0} physical damage and {self.__player.get_statistics()['magical_damage'] if "magical_damage" in self.__player.get_statistics().keys() else 0} magical damage to the enemy"
        self.__ability_button_list[0] = UIButton(
            text="Normal Attack",
            relative_rect=pygame.Rect(
                (ability_x_gap, init_ability_button_y),
                (130, 100),
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
                        (ability_count + 1) * 130 + (ability_count + 2) * ability_x_gap,
                        init_ability_button_y,
                    ),
                    (130, 100),
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

        self.__player_animation = self.__ANIMATION_ASSETS["player/idle"].copy()
        self.__enemy_animation = self.__ANIMATION_ASSETS["enemy/idle"].copy()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_button_pressed = True
            self.get_ui_manager().process_events(event)
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
        if self.__quit_button_pressed:
            self.set_time_to_quit_app(True)
            return

        self.__combat_round_initalised = True
        if not self.__combat_round_initalised:
            pass  # Initialize the combat round - 3,2,1 GO

        if (
            self.__enemy.get_statistics()["health_points"] > 0
            and self.__player.get_statistics()["health_points"] > 0
            and self.__combat_round_initalised
        ):
            if self.__round_counter % 2 == 0:
                if self.__player_controller.is_stunned():
                    self.__tutorial_text.set_text("You are stunned and cannot act!")
                    self.__player_controller.stunned_round()
                    pygame.time.wait(250)
                    self.__round_counter += 1
                else:
                    # When the user has not picked the ability to use and is not stunned
                    if self.__ability_selected == -1:
                        self.__tutorial_text.set_text(
                            "Press the allocated button to use an action (ability / normal attack)"
                        )
                    # When the user is aiming for the enemies
                    elif not self.__is_player_attacking:
                        locked_ability_decision = (
                            self.__ability_selected
                        )  # lock in to the ability selected
                        self.__tutorial_text.set_text(
                            "Use your mouse to try and hit the enemy's key body parts! You only have one chance!"
                        )

                        # If the user has clicked, then attack with the given values
                        if (
                            self.__mouse_pressed
                            or self.__player_controller.is_stunned()
                        ):
                            self.__is_player_attacking = True
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
                            self.__player_animation = self.__ANIMATION_ASSETS[
                                "player/attack"
                            ].copy()
                    # Attacking, perform animation, update the health bars
                    elif (
                        self.__is_player_attacking and self.__player_animation.is_done()
                    ):
                        self.__player_animation = self.__ANIMATION_ASSETS[
                            "player/idle"
                        ].copy()
                        self.__ability_selected = -1  # Reset turn action flags
                        self.__is_player_attacking = False
                        self.__round_counter += 1

            else:
                if self.__enemy_controller.is_stunned():
                    self.__tutorial_text.set_text(
                        "You stunned the boss, you can hit again, good job!"
                    )
                    self.__enemy_controller.stunned_round()
                    pygame.time.wait(250)
                    self.__round_counter += 1
                else:
                    if not self.__is_enemy_attacking:
                        random_ability_choice = random.randint(
                            0,
                            len(self.__enemy.get_abilities())
                            - len(self.__enemy_controller.get_cooldown_abilities()),
                        )

                        random_ability_choice = (
                            None
                            if random_ability_choice == 0
                            else self.__enemy.get_abilities()[random_ability_choice - 1]
                        )
                        self.__player_controller.regenerate()
                        self.__enemy_controller.regenerate()
                        # Compute damage and debuffs, apply buffs
                        physical_damage, magical_damage, debuff_dict = (
                            self.__enemy_controller.attack(0, random_ability_choice)
                        )
                        # Apply the damage and debuffs to the player
                        self.__player_controller.face_damage(
                            physical_damage, magical_damage, debuff_dict
                        )
                        self.__enemy_animation = self.__ANIMATION_ASSETS[
                            "enemy/attack"
                        ].copy()
                        self.__is_enemy_attacking = True

                    elif self.__is_enemy_attacking and self.__enemy_animation.is_done():
                        self.__enemy_animation = self.__ANIMATION_ASSETS[
                            "enemy/idle"
                        ].copy()
                        self.__is_enemy_attacking = False
                        self.__round_counter += 1

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
        self.__quit_button_pressed = False

    def render(self, time_delta: int):
        self.__player_HUD.update()
        self.__enemy_HUD.update()

        self.__player_animation.update()
        self.__enemy_animation.update()

        self.__player_sprite.image = self.__player_animation.img()
        self.__enemy_sprite.image = self.__enemy_animation.img()

        for ability_index in range(len(self.__player.get_unlocked_abilities())):
            if self.__player_controller.is_ability_on_cooldown(
                self.__player.get_unlocked_abilities()[ability_index]
            ):
                self.__ability_button_list[ability_index + 1].set_text(
                    f"Cooldown: {self.__player_controller.get_cooldown_abilities()[self.__player.get_unlocked_abilities()[ability_index].get_name()]}"
                )
                self.__ability_button_list[ability_index + 1].disable()
            else:
                self.__ability_button_list[ability_index + 1].enable()
                self.__ability_button_list[ability_index + 1].set_text(
                    self.__player.get_unlocked_abilities()[ability_index].get_name()
                )
        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(
            pygame.Surface((self.get_screen().width, self.get_screen().height)), (0, 0)
        )
        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def end(self) -> None:
        self.__player_sprite.kill()
        self.__enemy_sprite.kill()
        self.__player_info_container.kill()
        self.__enemy_info_container.kill()
        self.__player_choice_container.kill()
        self.__tutorial_text.kill()
        self.__visual_dialogue.kill()
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
