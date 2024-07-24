import pygame
import pygame_gui
from pygame_gui.elements import UITextBox, UIPanel
from ability import Ability
import random
from pygame_gui.core import ObjectID
from quest import Quest


class VisualDialogue:
    """
    VisualDialogue class to manage and display dialogue and quest information in the game.
    """

    # Class variables with initial values
    __dialogue_life_time: int = 0
    __temp_quest: Quest = None
    __dialogue_UI: UITextBox = None
    __quest_display: UITextBox = None

    def __init__(
        self, ui_manager: pygame_gui.UIManager, container: UIPanel, temp_quest: Quest
    ) -> None:
        """
        Initializes the VisualDialogue class.

        :param ui_manager: The UI manager for pygame_gui.
        :param container: The container UIPanel.
        :param temp_quest: The temporary quest.
        """
        # Setting the initial values using setters
        self.set_temp_quest(temp_quest)

        # Initializing the dialogue UITextBox
        self.set_dialogue_UI(UITextBox(
            "",
            pygame.Rect((25, 10), (container.relative_rect.width * 0.45, -1)),
            ui_manager,
            container=container,
            object_id=ObjectID(object_id="#visual_dialogue_text"),
        ))
        self.get_dialogue_UI().hide()

        # Setting up the quest display UITextBox
        quest_display_rect = pygame.Rect(
            (0, 10), (container.relative_rect.width * 0.5, -1)
        )
        quest_display_rect.right = -25
        self.set_quest_display(UITextBox(
            f"Quest master: Hello! hello! will you {self.get_temp_quest().get_description()} for money of unknown sums? :/\nProgress: {self.get_temp_quest().get_progress()}/{self.get_temp_quest().get_aim()}",
            quest_display_rect,
            ui_manager,
            anchors={"right": "right"},
            container=container,
            object_id=ObjectID(object_id="#quest_display_text"),
        ))

    def set_dialogue(
        self,
        player_name: str,
        enemy_name: str,
        health_points: int,
        mana_points: int,
        total_damage: int,
        is_stunned: bool,
        ability: Ability,
    ) -> None:
        """
        Sets the dialogue based on the provided parameters.

        :param player_name: The player's name.
        :param enemy_name: The enemy's name.
        :param health_points: The player's health points.
        :param mana_points: The player's mana points.
        :param total_damage: The total damage dealt.
        :param is_stunned: Whether the player is stunned.
        :param ability: The ability used by the player.
        """
        # Initialize dialogue outputs
        player_dialogue_output = ""
        enemy_dialogue_output = ""
        final_dialogue_output = ""

        # Possible player dialogues
        player_dialogues = [
            "It's my turn to attack!",
            "Brace yourself, here they come!",
        ]

        # Possible enemy dialogues
        enemy_dialogues = ["Let's see what you've got!", "Prepare to be crushed!"]

        # Additional dialogues based on health points
        if health_points < 50:
            player_dialogues.append("I'm not done yet!")
            player_dialogues.append("I can still fight!")
            enemy_dialogues.append("You're barely standing. Just give up!")
        elif health_points < 200:
            player_dialogues.append("I need to be careful.")
            enemy_dialogues.append("Your end is near!")
            player_dialogues.append("I won't go down easily!")
            enemy_dialogues.append("You can't win this!")

        # Additional dialogues based on mana points
        if mana_points < 20:
            player_dialogues.append("I need more mana!")
            enemy_dialogues.append("Running out of tricks, are we?")
            player_dialogues.append("I'm running low on magic.")
            enemy_dialogues.append("Your magic is weakening!")

        # Additional dialogues based on stun status
        if is_stunned:
            player_dialogues.append("I can't move!")
            enemy_dialogues.append("You're helpless now!")
            player_dialogues.append("I'm paralyzed!")
            enemy_dialogues.append("I have you where I want you!")

        # Additional dialogues based on ability used
        if ability is not None:
            player_dialogues.append(f"Take this! {ability.get_name()}!")
            player_dialogues.append(f"Feel my power! {ability.get_name()}!")
            enemy_dialogues.append(f"Your {ability.get_name()} is too easy!")
            enemy_dialogues.append(f"Your {ability.get_name()} is no match for me!!")

        # Additional dialogues based on damage dealt
        if total_damage > 100:
            player_dialogues.append("That was a powerful hit!")
            player_dialogues.append("I won't let you get away with that!")
            enemy_dialogues.append("You'll pay for that!")
            enemy_dialogues.append("That won't happen again!")

        # Randomly choose the number of dialogues for player and enemy
        player_dialogue_number, enemy_dialogue_number = random.choice(
            [(1, 1), (2, 0), (0, 2), (1, 0), (0, 1)]
        )

        # Select and format player dialogues
        for _ in range(player_dialogue_number):
            player_dialogue = random.choice(player_dialogues)
            player_dialogues.pop(player_dialogues.index(player_dialogue))
            player_dialogue_output += f"{player_name}: {player_dialogue}\n"

        # Select and format enemy dialogues
        for _ in range(enemy_dialogue_number):
            enemy_dialogue = random.choice(enemy_dialogues)
            enemy_dialogues.pop(enemy_dialogues.index(enemy_dialogue))
            enemy_dialogue_output += f"{enemy_name}: {enemy_dialogue}\n"

        # Combine player and enemy dialogues
        if player_dialogue_output != "":
            final_dialogue_output += player_dialogue_output
        if enemy_dialogue_output != "":
            final_dialogue_output += enemy_dialogue_output

        # Set the dialogue text and show the dialogue box
        self.get_dialogue_UI().set_text(final_dialogue_output)
        self.get_dialogue_UI().show()
        self.set_dialogue_life_time(20)

    def update(self) -> None:
        """
        Updates the quest display and decreases the dialogue lifetime.
        """
        # Update quest display text
        self.get_quest_display().set_text(
            f"Quest master: Hello! hello! will you {self.get_temp_quest().get_description()} for money of unknown sums? :/\nProgress: {self.get_temp_quest().get_progress()}/{self.get_temp_quest().get_aim()}",
        )
        # Decrease dialogue lifetime
        if self.get_dialogue_life_time() > 0:
            self.set_dialogue_life_time(self.get_dialogue_life_time() - 1)

    def is_done(self) -> bool:
        """
        Checks if the dialogue lifetime has ended.

        :return: True if the dialogue lifetime is zero or less, False otherwise.
        """
        return self.get_dialogue_life_time() <= 0

    def kill(self) -> None:
        """
        Kills the dialogue and quest display elements.
        """
        self.get_dialogue_UI().kill()
        self.get_quest_display().kill()

    # Getters and setters with docstrings

    def get_dialogue_life_time(self) -> int:
        """
        Gets the current dialogue lifetime.

        :return: The current dialogue lifetime.
        """
        return self.__dialogue_life_time

    def set_dialogue_life_time(self, value: int) -> None:
        """
        Sets the current dialogue lifetime.

        :param value: The new dialogue lifetime.
        """
        self.__dialogue_life_time = value

    def get_temp_quest(self) -> Quest:
        """
        Gets the temporary quest.

        :return: The temporary quest.
        """
        return self.__temp_quest

    def set_temp_quest(self, value: Quest) -> None:
        """
        Sets the temporary quest.

        :param value: The new temporary quest.
        """
        self.__temp_quest = value

    # Getter and setter for __dialogue
    def get_dialogue_UI(self) -> UITextBox:
        """
        Gets the dialogue UITextBox.

        :return: The dialogue UITextBox.
        """
        return self.__dialogue_UI

    def set_dialogue_UI(self, value: UITextBox) -> None:
        """
        Sets the dialogue UITextBox.

        :param value: The new dialogue UITextBox.
        """
        self.__dialogue_UI = value

    # Getter and setter for __quest_display
    def get_quest_display(self) -> UITextBox:
        """
        Gets the quest display UITextBox.

        :return: The quest display UITextBox.
        """
        return self.__quest_display

    def set_quest_display(self, value: UITextBox) -> None:
        """
        Sets the quest display UITextBox.

        :param value: The new quest display UITextBox.
        """
        self.__quest_display = value