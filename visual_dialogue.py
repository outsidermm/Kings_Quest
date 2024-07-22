import pygame, pygame_gui
from pygame_gui.elements import UITextBox, UIPanel
from ability import Ability
import random
from pygame_gui.core import ObjectID


class VisualDialogue:

    __dialogue_life_time: int = 0
    __initial_dialogue_life_time: int = 20

    def __init__(self, ui_manager: pygame_gui.UIManager, container: UIPanel) -> None:
        self.__ui_manager = ui_manager
        self.__container = container
        self.__dialogue = UITextBox(
            "",
            pygame.Rect((0, 35), (self.__container.relative_rect.width*0.8, -1)),
            self.__ui_manager,
            container=self.__container,
            anchors={"centerx": "centerx"},
            object_id=ObjectID(object_id="#visual_dialogue_text"),
        )
        self.__dialogue.hide()

    def set_dialogue(
        self,
        player_name:str,enemy_name:str,
        health_points: int,
        mana_points: int,
        total_damage: int,
        is_stunned: bool,
        ability: Ability,
    ) -> None:
        
        player_dialogue_output = ""
        enemy_dialogue_output = ""
        final_dialogue_output = ""
        
        player_dialogues = ["It's my turn to attack!",
        "Brace yourself, here they come!"]

        enemy_dialogues = ["Let's see what you've got!",
        "Prepare to be crushed!"]
        # Based on health points
        if health_points < 50:
            player_dialogues.append("I'm not done yet!")
            player_dialogues.append("I can still fight!")
            enemy_dialogues.append("You're barely standing. Just give up!")
        elif health_points < 200:
            player_dialogues.append("I need to be careful.")
            enemy_dialogues.append("Your end is near!")
            player_dialogues.append("I won't go down easily!")
            enemy_dialogues.append("You can't win this!")

        # Based on mana points
        if mana_points < 20:
            player_dialogues.append("I need more mana!")
            enemy_dialogues.append("Running out of tricks, are we?")
            player_dialogues.append("I'm running low on magic.")
            enemy_dialogues.append("Your magic is weakening!")

        # Based on stun status
        if is_stunned:
            player_dialogues.append("I can't move!")
            enemy_dialogues.append("You're helpless now!")
            player_dialogues.append("I'm paralyzed!")
            enemy_dialogues.append("I have you where I want you!")

        # Based on ability used
        if ability is not None:
            player_dialogues.append(f"Take this! {ability.get_name()}!")
            player_dialogues.append(f"Feel my power! {ability.get_name()}!")
            enemy_dialogues.append(f"Your {ability.get_name()} is too easy!")
            enemy_dialogues.append(f"Your {ability.get_name()} is no match for me!!")

        # Based on damage dealt
        if total_damage > 100:
            player_dialogues.append("That was a powerful hit!")
            player_dialogues.append("I won't let you get away with that!")
            enemy_dialogues.append("You'll pay for that!")
            enemy_dialogues.append("That won't happen again!")
        
        player_dialogue_number, enemy_dialogue_number = random.choice([(1,1),(2,0),(0,2),(1,0),(0,1)])
        for _ in range(player_dialogue_number):
            player_dialogue = random.choice(player_dialogues)
            player_dialogues.pop(player_dialogues.index(player_dialogue))
            player_dialogue_output += f"{player_name}: {player_dialogue}\n"
        
        for _ in range(enemy_dialogue_number):
            enemy_dialogue = random.choice(enemy_dialogues)
            enemy_dialogues.pop(enemy_dialogues.index(enemy_dialogue))
            enemy_dialogue_output += f"{enemy_name}: {enemy_dialogue}\n"
        
        if player_dialogue_output != "":
            final_dialogue_output += player_dialogue_output
        if enemy_dialogue_output != "":
            final_dialogue_output += enemy_dialogue_output
            
        self.__dialogue.set_text(final_dialogue_output)
        self.__dialogue.show()
        self.__dialogue_life_time = self.__initial_dialogue_life_time


    def update(self) -> None:
        if self.__dialogue_life_time > 0:
            self.__dialogue_life_time -= 1

    def is_done(self) -> bool:
        return self.__dialogue_life_time <= 0