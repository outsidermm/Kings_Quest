import pygame
from pygame_gui.elements import  UITextBox, UIImage
from pygame_gui.core import ObjectID
import pygame_gui
from characters.base_character import BaseCharacter
from gui.health_bar import HealthBar


class CombatHUD:
    __ui_manager: pygame_gui.UIManager = None
    __player: BaseCharacter = None
    __container = None
    __is_flipped: bool = False
    __health_bar: HealthBar = None
    __HUD_text: dict[str, UITextBox] = {}
    

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
        ui_manager: pygame_gui.UIManager,
        player: BaseCharacter,
        container,
        is_flipped: bool = False,
        HUD_init_text_y: int = 20,
        HUD_text_x: int = 75,
        HUD_step: int = 30,
    ) -> None:
        self.__ui_manager = ui_manager
        self.__player = player
        self.__container = container
        self.__is_flipped = is_flipped

        health_bar_rect = pygame.Rect((0, 20), (225, 30))
        if self.__is_flipped:
            health_bar_rect.right = 240
        else:
            health_bar_rect.left = 85
        
        self.__health_bar = HealthBar(
            self.__ui_manager,
            self.__container,
            health_bar_rect,
            self.__player.get_statistics()["health_points"],
            self.__player.get_statistics()["health_points"],
            is_flipped=self.__is_flipped,
        )

        player_icon_rect = pygame.Rect((0, 60), (48, 48))
        if self.__is_flipped:
            player_icon_rect.right = -35
        else:
            player_icon_rect.left = 35
            
        UIImage(
            player_icon_rect,
            image_surface=pygame.transform.scale(
            pygame.image.load("assets/icons_18/health_points.png"), (48, 48)
        ),
            anchors={"right":"right"} if self.__is_flipped else {"left":"left"},
            manager=self.__ui_manager,
            container=self.__container,
        )

        for statistic_count, statistic_name in enumerate(self.__CHARACTER_MAX_VAL.keys()):
            if statistic_name not in self.__player.get_statistics().keys():
                self.__player.get_statistics()[statistic_name] =0
    
            if statistic_name != "health_points":
                statistic_rect = pygame.Rect((0, HUD_init_text_y + statistic_count * HUD_step),(225,30))
                if self.__is_flipped:
                    statistic_rect.right = -HUD_text_x
                else:
                    statistic_rect.left = HUD_text_x
                    
                self.__HUD_text[statistic_name] = UITextBox(
                    html_text=f'<img src="assets/icons_18/{statistic_name}.png"> '
                    f"{" ".join(word.capitalize() for word in statistic_name.split("_"))}: {self.__player.get_statistics()[statistic_name]}",
                    relative_rect=statistic_rect,
                    manager=self.__ui_manager,
                    anchors={"right":"right"} if self.__is_flipped else {"left":"left"},
                    object_id=ObjectID(object_id="#HUD-text"),
                    container=self.__container,
                )
                
    def update(self):
        self.__health_bar.update(self.__player.get_statistics()["health_points"])
        for statistic_name in self.__CHARACTER_MAX_VAL.keys():
            if statistic_name not in self.__player.get_statistics().keys():
                self.__player.get_statistics()[statistic_name] =0
    
            if statistic_name != "health_points":
                self.__HUD_text[statistic_name].set_text(
                    html_text=f'<img src="assets/icons_18/{statistic_name}.png"> '
                    f"{" ".join(word.capitalize() for word in statistic_name.split("_"))}: {self.__player.get_statistics()[statistic_name]}"
                )