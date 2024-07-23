from states.base_state import BaseState
from state_manager import GameStateManager
import pygame, pygame_gui
from pygame_gui.elements import UIButton, UITextBox, UIPanel
from pygame_gui.core import ObjectID
from xp import XP
from quest import Quest


class QuestMenu(BaseState):

    __quests: list[Quest] = None
    __quit_button_pressed: bool = False
    __show_quest_info: int = -1
    __quest_buttons: list[UIButton] = None
    __GUI_background: pygame.Surface = None
    __navigate_level_selection_button: UIButton = None
    __navigate_level_selection: bool = False
    __exit_quest_button: UIButton = None
    __quest_overview: UIPanel = None
    __static_panel_wrapper: UIPanel = None
    __quest_name: UITextBox = None
    __quest_description: UITextBox = None
    __claim_quest_button: UIButton = None
    __claim_quest: bool = False
    __xp: XP = None

    def __init__(
        self,
        screen: pygame.Surface,
        ui_manager: pygame_gui.UIManager,
        game_state_manager: GameStateManager,
        quests: list[Quest],
        xp: XP,
    ):
        super().__init__(
            "quest_menu",
            screen,
            ui_manager,
            "level_selection_menu",
            game_state_manager,
        )
        self.__quests = quests
        self.__quest_buttons = [None] * len(self.__quests)
        self.__xp = xp

    def start(self) -> None:
        self.set_outgoing_transition_data(self.get_incoming_transition_data())

        self.__GUI_background = pygame.transform.scale(
            pygame.image.load("assets/GUIBackground.png"),
            (self.get_screen().width, self.get_screen().height),
        )

        self.__static_panel_wrapper = UIPanel(
            pygame.Rect((0, 0), (self.get_screen().width, self.get_screen().height)),
            manager=self.get_ui_manager(),
            object_id=ObjectID(object_id="#transparent_panel"),
        )

        UITextBox(
            "Quests",
            pygame.Rect((0, -self.get_screen().height * 0.3), (1000, 200)),
            self.get_ui_manager(),
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@title", object_id="#game_title"),
            container=self.__static_panel_wrapper,
        )

        navigate_level_selection_button_rect = pygame.Rect((75, 0), (300, 100))
        navigate_level_selection_button_rect.bottom = -75
        self.__navigate_level_selection_button = UIButton(
            relative_rect=navigate_level_selection_button_rect,
            text="← Level Selection",
            manager=self.get_ui_manager(),
            anchors=({"bottom": "bottom"}),
            object_id=ObjectID(class_id="@level_selection_button"),
            container=self.__static_panel_wrapper,
        )

        quest_button_width = 300
        quest_button_height = 200
        quest_button_gap = (
            self.get_screen().get_width() - quest_button_width * len(self.__quests)
        ) / (len(self.__quests) + 1)
        for quest_button_count, quest in enumerate(self.__quests):
            self.__quest_buttons[quest_button_count] = UIButton(
                relative_rect=pygame.Rect(
                    (
                        quest_button_gap * (quest_button_count + 1)
                        + quest_button_width * quest_button_count,
                        0,
                    ),
                    (quest_button_width, quest_button_height),
                ),
                text=f"{quest_button_count+1}: {quest.get_name()}",
                anchors=({"centery": "centery"}),
                manager=self.get_ui_manager(),
                object_id=ObjectID(class_id="@level_selection_button"),
                container=self.__static_panel_wrapper,
            )
            if self.__quests[quest_button_count].is_claimed():
                self.__quest_buttons[quest_button_count].set_text("CLAIMED")
                self.__quest_buttons[quest_button_count].disable()

        self.__quest_overview = UIPanel(
            pygame.Rect(
                (0, 0), (self.get_screen().width * 0.4, self.get_screen().height * 0.7)
            ),
            manager=self.get_ui_manager(),
            starting_height=2,
            anchors=({"center": "center"}),
            object_id=ObjectID(class_id="@ability_menu"),
            visible=False,
        )

        self.__quest_name = UITextBox(
            self.__quests[0].get_name(),
            pygame.Rect((0, 25), (300, 75)),
            self.get_ui_manager(),
            container=self.__quest_overview,
            anchors=({"centerx": "centerx"}),
            object_id=ObjectID(class_id="@level_selection_text"),
        )

        self.__quest_description = UITextBox(
            f"{self.__quests[0].get_description()}\n Current Progress: {self.__quests[0].get_progress()}/{self.__quests[0].get_aim()}\nReward: {self.__quests[0].get_reward()} XP",
            pygame.Rect((0, 100), (400, -1)),
            self.get_ui_manager(),
            container=self.__quest_overview,
            anchors=({"centerx": "centerx"}),
            object_id=ObjectID(class_id="#enemy_statistic"),
        )

        self.__claim_quest_button = UIButton(
            relative_rect=pygame.Rect((0, 75), (300, 50)),
            text="CLAIM",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__quest_overview,
            object_id=ObjectID(class_id="@level_selection_button"),
        )

        self.__exit_quest_button = UIButton(
            relative_rect=pygame.Rect((0, 175), (300, 50)),
            text="CANCEL",
            manager=self.get_ui_manager(),
            anchors=({"center": "center"}),
            container=self.__quest_overview,
            object_id=ObjectID(class_id="@level_selection_button"),
        )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_button_pressed = True
            self.get_ui_manager().process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__navigate_level_selection_button:
                    self.__navigate_level_selection = True
                if event.ui_element == self.__claim_quest_button:
                    self.__claim_quest = True
                if event.ui_element == self.__exit_quest_button:
                    self.__show_quest_info = -1
                for quest_button_index in range(len(self.__quests)):
                    if event.ui_element == self.__quest_buttons[quest_button_index]:
                        self.__show_quest_info = quest_button_index

    def run(self) -> None:
        if self.__quit_button_pressed:
            self.set_time_to_quit_app(True)
            return

        if self.__navigate_level_selection:
            self.set_target_state_name("level_selection_menu")
            self.set_time_to_transition(True)
            return

        if self.__claim_quest:
            self.__xp.gain_xp(self.__quests[self.__show_quest_info].get_reward())
            self.__quest_buttons[self.__show_quest_info].set_text("CLAIMED")
            self.__quests[self.__show_quest_info].claim()
            self.__quest_buttons[self.__show_quest_info].disable()
            self.__show_quest_info = -1

    def render(self, time_delta: int) -> None:
        if self.__show_quest_info != -1:
            self.__quest_name.set_text(self.__quests[self.__show_quest_info].get_name())

            self.__quest_description.set_text(
                f"{self.__quests[self.__show_quest_info].get_description()}\n Current Progress: {self.__quests[self.__show_quest_info].get_progress()}/{self.__quests[0].get_aim()}\nReward: {self.__quests[self.__show_quest_info].get_reward()} XP",
            )
            if self.__quests[self.__show_quest_info].is_done():
                self.__claim_quest_button.show()
            else:
                self.__claim_quest_button.hide()
            self.__quest_overview.show()
            self.__static_panel_wrapper.hide()
        else:
            self.__quest_overview.hide()
            self.__static_panel_wrapper.show()

        self.get_ui_manager().update(time_delta)
        self.get_screen().blit(self.__GUI_background, (0, 0))

        self.get_ui_manager().draw_ui(self.get_screen())
        pygame.display.update()

    def reset_event_polling(self) -> None:
        self.__quit_button_pressed = False
        self.__navigate_level_selection = False
        self.__claim_quest = False

    def end(self) -> None:
        [
            self.__quest_buttons[quest_button_index].kill()
            for quest_button_index in range(len(self.__quests))
        ]
        self.__navigate_level_selection_button.kill()
        self.__claim_quest_button.kill()
        self.__exit_quest_button.kill()
        self.__quest_overview.kill()
        self.__static_panel_wrapper.kill()
        self.__quest_name.kill()
        self.__quest_description.kill()
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

    def set_target_state_name(self, target_state_name: str) -> None:
        super().set_target_state_name(target_state_name)

    def get_target_state_name(self) -> str:
        return super().get_target_state_name()
