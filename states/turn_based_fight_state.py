from .base_state import BaseState
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from state_manager import GameStateManager
from characters.players.base_player import BasePlayer
from characters.enemies.base_enemy import BaseEnemy
from gui.player_combat_hud import PlayerCombatHUD
from gui.enemy_combat_hud import EnemyCombatHUD
from combat_controller import CombatController
import random
from ability import Ability
from utilities.animation_utility import Animation
from utilities.img_utility import load_images
from visual_dialogue import VisualDialogue
from quest import Quest
from typing import List, Dict


class TurnBasedFight(BaseState):
    """
    TurnBasedFight class handles the turn-based fight mechanics in the game,
    including player and enemy actions, animations, and HUD updates.
    """

    __player: BasePlayer = None
    __enemy: BaseEnemy = None
    __round_counter: int = 0
    __combat_round_initialized: bool = False
    __player_controller: CombatController = None
    __enemy_controller: CombatController = None
    __player_HUD: PlayerCombatHUD = None
    __enemy_HUD: EnemyCombatHUD = None
    __ability_selected: Ability = -1
    __ability_button_list: List[UIButton] = [None] * 4
    __is_player_attacking: bool = False
    __is_enemy_attacking: bool = False
    __mouse_pressed: bool = False
    __enemy_hit_height: float = 0
    __player_animation: Animation = None
    __enemy_animation: Animation = None
    __visual_dialogue: VisualDialogue = None
    __visual_dialogue_container: UIPanel = None
    __quests: List[Quest] = None
    __count_down: UITextBox = None
    __temp_quest: Quest = None
    __temp_quest_template: Quest = None
    __animation_assets: Dict[str, Animation] = {}
    __background_image: UIImage = None
    __player_sprite: UIImage = None
    __enemy_sprite: UIImage = None
    __quest_master_sprite: UIImage = None
    __player_info_container: UIPanel = None
    __enemy_info_container: UIPanel = None
    __player_choice_container: UIPanel = None
    __tutorial_text: UITextBox = None
    __start_tick: int = 0

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        quests: List[Quest],
        temp_quest: Quest,
    ):
        """
        Initializes the TurnBasedFight class.

        :param screen: The game screen.
        :param ui_manager: The UI manager for pygame_gui.
        :param game_state_manager: The game state manager.
        :param quests: List of quests.
        :param temp_quest: Temporary quest.
        """
        super().__init__(
            "turn_based_fight",
            screen,
            ui_manager,
            "end_menu",
            game_state_manager,
        )
        self.set_quests(quests)
        self.set_temp_quest_template(temp_quest)

    def start(self) -> None:
        """
        Starts the turn-based fight, setting up players, enemies, HUDs, and animations.
        """
        # Copy the temporary quest template to initialize the temp quest
        self.set_temp_quest(self.get_temp_quest_template().copy())
        # Set the player and enemy using the incoming transition data
        self.set_player(self.get_incoming_transition_data()["player"])
        self.set_enemy(self.get_incoming_transition_data()["enemy"])

        # Load animations for the player, enemy, and quest master
        self.set_animation_assets(
            {
                "player/idle": Animation(
                    load_images(
                        f"characters/players/{self.get_player().get_name()}/idle"
                    ),
                    image_duration=10,
                ).copy(),
                "player/attack": Animation(
                    load_images(
                        f"characters/players/{self.get_player().get_name()}/attack"
                    ),
                    image_duration=6,
                    loop=False,
                ).copy(),
                "enemy/idle": Animation(
                    load_images(
                        f"characters/enemies/{self.get_enemy().get_name()}/idle"
                    ),
                    is_flipped=True,
                ).copy(),
                "enemy/attack": Animation(
                    load_images(
                        f"characters/enemies/{self.get_enemy().get_name()}/attack"
                    ),
                    image_duration=6,
                    loop=False,
                    is_flipped=True,
                ).copy(),
                "quest_master/idle": Animation(
                    load_images("characters/npcs/quest_master/idle"),
                    image_duration=10,
                    is_flipped=True,
                ).copy(),
            }
        )

        # Set the background image for the fight scene
        self.set_background_image(
            UIImage(
                relative_rect=pygame.Rect(
                    (0, 0),
                    (self.get_screen().get_width(), self.get_screen().get_height()),
                ),
                image_surface=pygame.image.load("assets/fight/1.png"),
                manager=self.get_ui_manager(),
            )
        )

        # Set the player sprite
        self.set_player_sprite(
            UIImage(
                relative_rect=pygame.Rect(
                    (self.get_screen().width * 0.3, 300),
                    (200, 200),
                ),
                image_surface=pygame.image.load(
                    self.get_player().get_sprite_location()
                ),
                manager=self.get_ui_manager(),
            )
        )

        # Set the enemy sprite, flipped horizontally
        self.set_enemy_sprite(
            UIImage(
                relative_rect=pygame.Rect(
                    (self.get_screen().width * 0.5, 350),
                    (200, 200),
                ),
                image_surface=pygame.transform.flip(
                    pygame.image.load(
                        self.get_enemy().get_sprite_location()
                    ).convert_alpha(),
                    True,
                    False,
                ),
                manager=self.get_ui_manager(),
            )
        )

        # Set the quest master sprite, flipped horizontally
        self.set_quest_master_sprite(
            UIImage(
                relative_rect=pygame.Rect(
                    (self.get_screen().width * 0.7, 400),
                    (200, 200),
                ),
                image_surface=pygame.transform.flip(
                    pygame.image.load(
                        "assets/characters/npcs/quest_master/idle/0.png"
                    ).convert_alpha(),
                    True,
                    False,
                ),
                manager=self.get_ui_manager(),
            )
        )

        # Create the player info container panel
        self.set_player_info_container(
            UIPanel(
                relative_rect=pygame.Rect((-5, 0), (325, 330)),
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#semi-transparent_panel"),
            )
        )

        # Set up the player's HUD
        self.set_player_HUD(
            PlayerCombatHUD(
                self.get_ui_manager(),
                self.get_player(),
                self.get_player_info_container(),
            )
        )

        # Create the enemy info container panel with right anchor
        enemy_info_rect = pygame.Rect((0, 0), (325, 330))
        enemy_info_rect.right = 5
        self.set_enemy_info_container(
            UIPanel(
                relative_rect=enemy_info_rect,
                anchors={"right": "right"},
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#semi-transparent_panel"),
            )
        )

        # Set up the enemy's HUD, with the image flipped horizontally
        self.set_enemy_HUD(
            EnemyCombatHUD(
                self.get_ui_manager(),
                self.get_enemy(),
                self.get_enemy_info_container(),
                is_flipped=True,
            )
        )

        # Calculate the width of the player choice container and create it
        player_choice_container_width = self.get_screen().width - 650
        self.set_player_choice_container(
            UIPanel(
                relative_rect=pygame.Rect((0, 0), (self.get_screen().width - 650, 200)),
                anchors={"centerx": "centerx"},
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#transparent_panel"),
            )
        )

        # Set up the tutorial text
        self.set_tutorial_text(
            UITextBox(
                html_text="Press the allocated button to use an action (ability / normal attack)",
                relative_rect=pygame.Rect(
                    (0, 200), (self.get_screen().width * 0.5, -1)
                ),
                anchors=({"centerx": "centerx"}),
                manager=self.get_ui_manager(),
                object_id=ObjectID(object_id="#tutorial_text"),
            )
        )

        # Calculate the gaps between ability buttons and create the normal attack button
        unlocked_abilities_number = len(self.get_player().get_unlocked_abilities())
        ability_x_gap = (
            player_choice_container_width - (unlocked_abilities_number + 1) * 130
        ) / (unlocked_abilities_number + 2)
        init_ability_button_y = 25

        normal_attack_tool_tip = (
            f"Deal {self.get_player().get_stats()['physical_damage'] if 'physical_damage' in self.get_player().get_stats().keys() else 0} "
            f"physical damage and {self.get_player().get_stats()['magical_damage'] if 'magical_damage' in self.get_player().get_stats().keys() else 0} "
            f"magical damage to the enemy"
        )
        self.get_ability_button_list()[0] = UIButton(
            text="Normal Attack",
            relative_rect=pygame.Rect(
                (ability_x_gap, init_ability_button_y),
                (130, 100),
            ),
            manager=self.get_ui_manager(),
            container=self.get_player_choice_container(),
            object_id=ObjectID(class_id="@Normal Attack", object_id="#choice_text0"),
            tool_tip_text=normal_attack_tool_tip,
        )

        # Create buttons for each unlocked ability
        for ability_count, ability in enumerate(
            self.get_player().get_unlocked_abilities()
        ):
            self.get_ability_button_list()[ability_count + 1] = UIButton(
                text=ability.get_name(),
                relative_rect=pygame.Rect(
                    (
                        (ability_count + 1) * 130 + (ability_count + 2) * ability_x_gap,
                        init_ability_button_y,
                    ),
                    (130, 100),
                ),
                manager=self.get_ui_manager(),
                container=self.get_player_choice_container(),
                object_id=ObjectID(
                    class_id=f"@{ability.get_name()}",
                    object_id=f"#choice_text{ability_count + 1}",
                ),
                tool_tip_text=ability.get_description(),
            )

        # Set up the countdown text box
        self.set_count_down(
            UITextBox(
                html_text="3",
                relative_rect=pygame.Rect((0, -100), (self.get_screen().width, -1)),
                anchors={"center": "center"},
                manager=self.get_ui_manager(),
                object_id=ObjectID(class_id="@title", object_id="#game_title"),
            )
        )

        # Create the visual dialogue container panel
        visual_dialogue_rect = pygame.Rect((0, 0), (self.get_screen().width, 150))
        visual_dialogue_rect.bottom = 0
        self.set_visual_dialogue_container(
            UIPanel(
                relative_rect=visual_dialogue_rect,
                manager=self.get_ui_manager(),
                anchors={"bottom": "bottom"},
                object_id=ObjectID(object_id="#visual_dialogue_box"),
            )
        )

        # Set up the visual dialogue
        self.set_visual_dialogue(
            VisualDialogue(
                self.get_ui_manager(),
                self.get_visual_dialogue_container(),
                self.get_temp_quest(),
            )
        )

        # Initialize the player and enemy combat controllers
        self.set_player_controller(
            CombatController(self.get_player(), self.get_player_sprite())
        )
        self.set_enemy_controller(
            CombatController(self.get_enemy(), self.get_enemy_sprite())
        )

        # Set initial animations for player, enemy, and quest master
        self.set_player_animation(self.get_animation_assets()["player/idle"])
        self.set_enemy_animation(self.get_animation_assets()["enemy/idle"])
        self.set_quest_master_animation(
            self.get_animation_assets()["quest_master/idle"]
        )

        # Set the start tick, round counter, and flags for combat initialization and attacks
        self.set_start_tick(pygame.time.get_ticks())
        self.set_round_counter(0)
        self.set_combat_round_initialized(False)
        self.set_is_player_attacking(False)
        self.set_is_enemy_attacking(False)

    def handle_events(self) -> None:
        """
        Handles the events occurring during the fight, including button presses and mouse events.
        """
        # Loop through all the events in the pygame event queue
        for event in pygame.event.get():
            # If the quit event is triggered, set the flag to quit the app
            if event.type == pygame.QUIT:
                self.set_time_to_quit_app(True)

            # Process the event with the UI manager
            self.get_ui_manager().process_events(event)

            # Handle button press events
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.get_ability_button_list()[0]:
                    # If the normal attack button is pressed, set ability_selected to None
                    self.set_ability_selected(None)
                else:
                    # Check if any of the ability buttons (index 1 to 3) are pressed
                    for ability_button_index in [1, 2, 3]:
                        if event.ui_element == self.get_ability_button_list()[ability_button_index]:
                            # Set the selected ability based on the button pressed
                            self.set_ability_selected(
                                self.get_player().get_unlocked_abilities()[ability_button_index - 1]
                            )

            # Handle mouse press events
            if pygame.mouse.get_pressed()[0]:
                # Set the mouse_pressed flag to True
                self.set_mouse_pressed(True)
                # Get the current mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Check if the mouse click is on the enemy sprite
                if self.get_enemy_sprite().rect.collidepoint(mouse_pos):
                    # Calculate the enemy hit height based on the mouse position
                    self.set_enemy_hit_height(
                        self.get_enemy_sprite().rect.height - (mouse_pos[1] - self.get_enemy_sprite().rect.y)
                    )
                else:
                    # If the mouse click is not on the enemy sprite, set the enemy hit height to 0
                    self.set_enemy_hit_height(0)

    def run(self) -> None:

        """
        Runs the main logic of the turn-based fight, handling player and enemy actions,
        animations, and HUD updates.
        """
        # Check if the game is set to quit
        if self.get_time_to_quit_app():
            return

        # Calculate the elapsed time since the start of the round
        seconds = (pygame.time.get_ticks() - self.get_start_tick()) / 1000

        # Initialize the combat round after a countdown of 3 seconds
        if seconds > 3:
            self.set_combat_round_initialized(True)
            self.get_count_down().kill()
        else:
            self.get_count_down().set_text(str(3 - int(seconds)))

        # Check if both player and enemy are still alive and if the combat round is initialized
        if (
            self.get_enemy().get_stats()["health_points"] > 0
            and self.get_player().get_stats()["health_points"] > 0
            and self.get_combat_round_initialized()
        ):
            # Determine if it's the player's turn (even round number) or the enemy's turn (odd round number)
            if self.get_round_counter() % 2 == 0:
                # Player's turn
                if self.get_player_controller().get_is_stunned():
                    # If the player is stunned, skip their turn
                    self.get_tutorial_text().set_text("You are stunned and cannot act!")
                    self.get_player_controller().stunned_round()
                    pygame.time.wait(250)
                    self.get_visual_dialogue().set_dialogue(
                        self.get_player().get_name(),
                        self.get_enemy().get_name(),
                        self.get_player().get_stats()["health_points"],
                        self.get_player().get_stats()["mana_points"],
                        0,
                        True,
                        None,
                    )
                    self.set_round_counter(self.get_round_counter() + 1)
                else:
                    # If the player is not stunned
                    if self.get_ability_selected() == -1:
                        # If no ability is selected, prompt the player to select one
                        self.get_tutorial_text().set_text(
                            "Press the allocated button to use an action (ability / normal attack)"
                        )
                    elif not self.get_is_player_attacking():
                        # If the player has selected an ability but hasn't attacked yet
                        locked_ability_decision = self.get_ability_selected()
                        self.get_tutorial_text().set_text(
                            "Use your mouse to try and hit the enemy's key body parts! You only have one chance!"
                        )
                        if (
                            self.get_mouse_pressed()
                            or self.get_player_controller().get_is_stunned()
                        ):
                            # If the player clicks to attack or is stunned
                            self.set_is_player_attacking(True)
                            self.get_player_controller().regenerate()
                            self.get_enemy_controller().regenerate()
                            (
                                physical_damage,
                                magical_damage,
                                debuff_dict,
                            ) = self.get_player_controller().attack(
                                self.get_enemy_hit_height(), locked_ability_decision
                            )
                            self.get_enemy_controller().face_damage(
                                physical_damage, magical_damage, debuff_dict
                            )
                            self.set_player_animation(
                                self.get_animation_assets()["player/attack"].copy()
                            )
                            self.get_visual_dialogue().set_dialogue(
                                self.get_player().get_name(),
                                self.get_enemy().get_name(),
                                self.get_player().get_stats()["health_points"],
                                self.get_player().get_stats()["mana_points"],
                                (physical_damage + magical_damage),
                                False,
                                locked_ability_decision,
                            )
                            if locked_ability_decision is not None:
                                for quest in self.get_quests():
                                    if (
                                        quest.get_name() == "Fireball"
                                        and locked_ability_decision.get_name()
                                        == "Fireball"
                                    ):
                                        quest.increment_progress(1)
                            else:
                                self.get_temp_quest().increment_progress(1)
                    elif (
                        self.get_is_player_attacking()
                        and self.get_player_animation().is_done()
                        and self.get_visual_dialogue().is_done()
                    ):
                        # Reset player state after attack animation is done
                        self.set_player_animation(
                            self.get_animation_assets()["player/idle"].copy()
                        )
                        self.set_ability_selected(-1)
                        self.set_is_player_attacking(False)
                        pygame.time.wait(250)
                        self.set_round_counter(self.get_round_counter() + 1)
            else:
                # Enemy's turn
                if self.get_enemy_controller().get_is_stunned():
                    # If the enemy is stunned, skip their turn
                    self.get_tutorial_text().set_text(
                        "You stunned the boss, you can hit again, good job!"
                    )
                    self.get_enemy_controller().stunned_round()
                    self.set_round_counter(self.get_round_counter() + 1)
                    self.get_visual_dialogue().set_dialogue(
                        self.get_enemy().get_name(),
                        self.get_player().get_name(),
                        self.get_enemy().get_stats()["health_points"],
                        self.get_enemy().get_stats()["mana_points"],
                        0,
                        True,
                        None,
                    )
                else:
                    if not self.get_is_enemy_attacking():
                        # Select a random ability for the enemy to use
                        random_ability_choice = random.randint(
                            0,
                            len(self.get_enemy().get_abilities())
                            - len(self.get_enemy_controller().get_cooldown_abilities()),
                        )
                        random_ability_choice = (
                            None
                            if random_ability_choice == 0
                            else self.get_enemy().get_abilities()[
                                random_ability_choice - 1
                            ]
                        )
                        self.get_player_controller().regenerate()
                        self.get_enemy_controller().regenerate()
                        physical_damage, magical_damage, debuff_dict = (
                            self.get_enemy_controller().attack(0, random_ability_choice)
                        )
                        self.get_player_controller().face_damage(
                            physical_damage, magical_damage, debuff_dict
                        )
                        self.set_enemy_animation(
                            self.get_animation_assets()["enemy/attack"].copy()
                        )
                        self.set_is_enemy_attacking(True)
                        self.get_visual_dialogue().set_dialogue(
                            self.get_enemy().get_name(),
                            self.get_player().get_name(),
                            self.get_enemy().get_stats()["health_points"],
                            self.get_enemy().get_stats()["mana_points"],
                            (physical_damage + magical_damage),
                            False,
                            random_ability_choice,
                        )
                    elif (
                        self.get_is_enemy_attacking()
                        and self.get_enemy_animation().is_done()
                        and self.get_visual_dialogue().is_done()
                    ):
                        # Reset enemy state after attack animation is done
                        self.set_enemy_animation(
                            self.get_animation_assets()["enemy/idle"].copy()
                        )
                        self.set_is_enemy_attacking(False)
                        self.set_round_counter(self.get_round_counter() + 1)

        # Check for victory or defeat
        if self.get_enemy().get_stats()["health_points"] <= 0:
            # Player wins
            for quest in self.get_quests():
                if (
                    quest.get_name() == "Kill DreadNoughts"
                    and self.get_enemy().get_name() == "DreadNought"
                ):
                    quest.increment_progress(1)
            outgoing_transition_dict = self.get_incoming_transition_data()
            outgoing_transition_dict["winner"] = "player"
            if self.get_temp_quest().is_done():
                outgoing_transition_dict["temp_quest_completion"] = (
                    self.get_temp_quest()
                )
            self.set_outgoing_transition_data(outgoing_transition_dict)
            self.set_time_to_transition(True)
        elif self.get_player().get_stats()["health_points"] <= 0:
            # Enemy wins
            outgoing_transition_dict = self.get_incoming_transition_data()
            outgoing_transition_dict["winner"] = "enemy"
            if self.get_temp_quest().is_done():
                outgoing_transition_dict["temp_quest_completion"] = (
                    self.get_temp_quest()
                )
            self.set_outgoing_transition_data(outgoing_transition_dict)
            self.set_time_to_transition(True)

    def reset_event_polling(self) -> None:
        """
        Resets the event polling flags for the next round.
        """
        self.set_mouse_pressed(False)

    def render(self, time_delta: int) -> None:
        """
        Renders the fight scene, updating animations and HUDs.

        :param time_delta: Time elapsed since the last frame.
        """
        # Update visual dialogue
        self.get_visual_dialogue().update()
        
        # Update player and enemy HUDs
        self.get_player_HUD().update()
        self.get_enemy_HUD().update()

        # Update animations for player, enemy, and quest master
        self.get_player_animation().update()
        self.get_enemy_animation().update()
        self.get_quest_master_animation().update()

        # Set the current frame image for player, enemy, and quest master sprites
        self.get_player_sprite().image = self.get_player_animation().img()
        self.get_enemy_sprite().image = self.get_enemy_animation().img()
        self.get_quest_master_sprite().image = self.get_quest_master_animation().img()

        # Update ability button states based on their cooldowns
        for ability_index, ability in enumerate(
            self.get_player().get_unlocked_abilities(), 1
        ):
            if self.get_player_controller().is_ability_on_cooldown(ability):
                # If the ability is on cooldown, update the button text and disable it
                self.get_ability_button_list()[ability_index].set_text(
                    f"Cooldown: {self.get_player_controller().get_cooldown_abilities()[ability.get_name()]}"
                )
                self.get_ability_button_list()[ability_index].disable()
            else:
                # If the ability is not on cooldown, enable the button and set its text to the ability name
                self.get_ability_button_list()[ability_index].enable()
                self.get_ability_button_list()[ability_index].set_text(
                    ability.get_name()
                )

        # Update the UI manager
        self.get_ui_manager().update(time_delta)

        # Clear the screen by blitting a new surface
        self.get_screen().blit(
            pygame.Surface((self.get_screen().width, self.get_screen().height)), (0, 0)
        )
        
        # Draw the UI elements on the screen
        self.get_ui_manager().draw_ui(self.get_screen())

        # If the enemy is attacking, apply a tint effect to the screen
        if self.get_is_enemy_attacking() and not self.get_enemy_animation().is_done():
            self.tint_damage(self.get_screen(), 0.2)
        
        # Update the display with the rendered frame
        pygame.display.update()

    def end(self) -> None:
        """
        Ends the turn-based fight, cleaning up UI elements and resetting the screen.
        """
        self.get_player_sprite().kill()
        self.get_enemy_sprite().kill()
        self.get_quest_master_sprite().kill()
        self.get_player_info_container().kill()
        self.get_enemy_info_container().kill()
        self.get_player_choice_container().kill()
        self.get_tutorial_text().kill()
        self.get_visual_dialogue_container().kill()
        self.get_visual_dialogue().kill()
        self.get_background_image().kill()
        self.get_screen().fill((0, 0, 0))

    def tint_damage(self, surface: pygame.Surface, scale: float) -> None:
        """
        Tints the screen to indicate damage taken.

        :param surface: The surface to tint.
        :param scale: The scale of the tint.
        """
        GB = min(255, max(0, round(255 * (1 - scale))))
        surface.fill((255, GB, GB), special_flags=pygame.BLEND_MULT)

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

    # Getter and setter for __player
    def get_player(self) -> BasePlayer:
        return self.__player

    def set_player(self, player: BasePlayer) -> None:
        self.__player = player

    # Getter and setter for __enemy
    def get_enemy(self) -> BaseEnemy:
        return self.__enemy

    def set_enemy(self, enemy: BaseEnemy) -> None:
        self.__enemy = enemy

    # Getter and setter for __round_counter
    def get_round_counter(self) -> int:
        return self.__round_counter

    def set_round_counter(self, round_counter: int) -> None:
        self.__round_counter = round_counter

    # Getter and setter for __combat_round_initialized
    def get_combat_round_initialized(self) -> bool:
        return self.__combat_round_initialized

    def set_combat_round_initialized(self, combat_round_initialized: bool) -> None:
        self.__combat_round_initialized = combat_round_initialized

    # Getter and setter for __player_controller
    def get_player_controller(self) -> CombatController:
        return self.__player_controller

    def set_player_controller(self, player_controller: CombatController) -> None:
        self.__player_controller = player_controller

    # Getter and setter for __enemy_controller
    def get_enemy_controller(self) -> CombatController:
        return self.__enemy_controller

    def set_enemy_controller(self, enemy_controller: CombatController) -> None:
        self.__enemy_controller = enemy_controller

    # Getter and setter for __player_HUD
    def get_player_HUD(self) -> PlayerCombatHUD:
        return self.__player_HUD

    def set_player_HUD(self, player_HUD: PlayerCombatHUD) -> None:
        self.__player_HUD = player_HUD

    # Getter and setter for __enemy_HUD
    def get_enemy_HUD(self) -> EnemyCombatHUD:
        return self.__enemy_HUD

    def set_enemy_HUD(self, enemy_HUD: EnemyCombatHUD) -> None:
        self.__enemy_HUD = enemy_HUD

    # Getter and setter for __ability_selected
    def get_ability_selected(self) -> Ability:
        return self.__ability_selected

    def set_ability_selected(self, ability_selected: Ability) -> None:
        self.__ability_selected = ability_selected

    # Getter and setter for __ability_button_list
    def get_ability_button_list(self) -> List[UIButton]:
        return self.__ability_button_list

    def set_ability_button_list(self, ability_button_list: List[UIButton]) -> None:
        self.__ability_button_list = ability_button_list

    # Getter and setter for __is_player_attacking
    def get_is_player_attacking(self) -> bool:
        return self.__is_player_attacking

    def set_is_player_attacking(self, is_player_attacking: bool) -> None:
        self.__is_player_attacking = is_player_attacking

    # Getter and setter for __is_enemy_attacking
    def get_is_enemy_attacking(self) -> bool:
        return self.__is_enemy_attacking

    def set_is_enemy_attacking(self, is_enemy_attacking: bool) -> None:
        self.__is_enemy_attacking = is_enemy_attacking

    # Getter and setter for __mouse_pressed
    def get_mouse_pressed(self) -> bool:
        return self.__mouse_pressed

    def set_mouse_pressed(self, mouse_pressed: bool) -> None:
        self.__mouse_pressed = mouse_pressed

    # Getter and setter for __enemy_hit_height
    def get_enemy_hit_height(self) -> float:
        return self.__enemy_hit_height

    def set_enemy_hit_height(self, enemy_hit_height: float) -> None:
        self.__enemy_hit_height = enemy_hit_height

    # Getter and setter for __player_animation
    def get_player_animation(self) -> Animation:
        return self.__player_animation

    def set_player_animation(self, player_animation: Animation) -> None:
        self.__player_animation = player_animation

    # Getter and setter for __enemy_animation
    def get_enemy_animation(self) -> Animation:
        return self.__enemy_animation

    def set_enemy_animation(self, enemy_animation: Animation) -> None:
        self.__enemy_animation = enemy_animation

    # Getter and setter for __visual_dialogue
    def get_visual_dialogue(self) -> VisualDialogue:
        return self.__visual_dialogue

    def set_visual_dialogue(self, visual_dialogue: VisualDialogue) -> None:
        self.__visual_dialogue = visual_dialogue

    # Getter and setter for __visual_dialogue_container
    def get_visual_dialogue_container(self) -> UIPanel:
        return self.__visual_dialogue_container

    def set_visual_dialogue_container(self, visual_dialogue_container: UIPanel) -> None:
        self.__visual_dialogue_container = visual_dialogue_container

    # Getter and setter for __quests
    def get_quests(self) -> List[Quest]:
        return self.__quests

    def set_quests(self, quests: List[Quest]) -> None:
        self.__quests = quests

    # Getter and setter for __count_down
    def get_count_down(self) -> UITextBox:
        return self.__count_down

    def set_count_down(self, count_down: UITextBox) -> None:
        self.__count_down = count_down

    # Getter and setter for __temp_quest
    def get_temp_quest(self) -> Quest:
        return self.__temp_quest

    def set_temp_quest(self, temp_quest: Quest) -> None:
        self.__temp_quest = temp_quest

    # Getter and setter for __temp_quest_template
    def get_temp_quest_template(self) -> Quest:
        return self.__temp_quest_template

    def set_temp_quest_template(self, temp_quest_template: Quest) -> None:
        self.__temp_quest_template = temp_quest_template

    # Getter and setter for __animation_assets
    def get_animation_assets(self) -> Dict[str, Animation]:
        return self.__animation_assets

    def set_animation_assets(self, animation_assets: Dict[str, Animation]) -> None:
        self.__animation_assets = animation_assets

    # Getter and setter for __background_image
    def get_background_image(self) -> UIImage:
        return self.__background_image

    def set_background_image(self, background_image: UIImage) -> None:
        self.__background_image = background_image

    # Getter and setter for __player_sprite
    def get_player_sprite(self) -> UIImage:
        return self.__player_sprite

    def set_player_sprite(self, player_sprite: UIImage) -> None:
        self.__player_sprite = player_sprite

    # Getter and setter for __enemy_sprite
    def get_enemy_sprite(self) -> UIImage:
        return self.__enemy_sprite

    def set_enemy_sprite(self, enemy_sprite: UIImage) -> None:
        self.__enemy_sprite = enemy_sprite

    # Getter and setter for __quest_master_sprite
    def get_quest_master_sprite(self) -> UIImage:
        return self.__quest_master_sprite

    def set_quest_master_sprite(self, quest_master_sprite: UIImage) -> None:
        self.__quest_master_sprite = quest_master_sprite

    # Getter and setter for __player_info_container
    def get_player_info_container(self) -> UIPanel:
        return self.__player_info_container

    def set_player_info_container(self, player_info_container: UIPanel) -> None:
        self.__player_info_container = player_info_container

    # Getter and setter for __enemy_info_container
    def get_enemy_info_container(self) -> UIPanel:
        return self.__enemy_info_container

    def set_enemy_info_container(self, enemy_info_container: UIPanel) -> None:
        self.__enemy_info_container = enemy_info_container

    # Getter and setter for __player_choice_container
    def get_player_choice_container(self) -> UIPanel:
        return self.__player_choice_container

    def set_player_choice_container(self, player_choice_container: UIPanel) -> None:
        self.__player_choice_container = player_choice_container

    # Getter and setter for __tutorial_text
    def get_tutorial_text(self) -> UITextBox:
        return self.__tutorial_text

    def set_tutorial_text(self, tutorial_text: UITextBox) -> None:
        self.__tutorial_text = tutorial_text

    # Getter and setter for __start_tick
    def get_start_tick(self) -> int:
        return self.__start_tick

    def set_start_tick(self, start_tick: int) -> None:
        self.__start_tick = start_tick

    # Getter and setter for __is_stunned
    def get_is_stunned(self) -> bool:
        return self.__is_stunned

    def set_is_stunned(self, is_stunned: bool) -> None:
        self.__is_stunned = is_stunned

    def get_quest_master_animation(self) -> Animation:
        """
        Gets the quest master's animation.

        :return: The quest master's animation.
        """
        return self.__quest_master_animation

    def set_quest_master_animation(self, quest_master_animation: Animation) -> None:
        """
        Sets the quest master's animation.

        :param quest_master_animation: The new quest master's animation.
        """
        self.__quest_master_animation = quest_master_animation
