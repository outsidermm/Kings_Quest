import pygame
import pygame_gui
from state_manager import GameStateManager
from states.menu import Menu


class Game:

    __screen = None
    __ui_manager = None
    __game_state_manager = None
    __clock = None

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        #TODO Shift to Setting file
        self.__SCREEN_WIDTH = 1280
        self.__SCREEN_HEIGHT = 720
        self.__FPS = 60

        self.set_screen(pygame.display.set_mode(
            (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT)
        ))
        self.set_ui_manager(pygame_gui.UIManager(
            (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT)
        ))

        self.set_clock(pygame.time.Clock())

        self.set_game_state_manager(GameStateManager("menu"))

        self.__menu = Menu(self.__screen, self.__ui_manager, self.__game_state_manager)

        self.states = {"menu": self.__menu}

    def run(self) -> None:
        while True:
            time_delta = self.__clock.tick_busy_loop(self.__FPS)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.states[self.get_game_state_manager().get_state()].handle_events(event)
                
                self.get_ui_manager().process_events(event)
                
            
            self.states[self.get_game_state_manager().get_state()].run()
            
            self.get_ui_manager().update(time_delta)

            self.states[self.get_game_state_manager().get_state()].render()
            self.get_screen().blit(
                pygame.Surface((self.__SCREEN_HEIGHT, self.__SCREEN_WIDTH)), (0, 0)
            )
            self.get_ui_manager().draw_ui(self.get_screen())
            pygame.display.update()


    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def get_ui_manager(self) -> pygame_gui.UIManager:
        return self.__ui_manager

    def get_game_state_manager(self) -> GameStateManager:
        return self.__game_state_manager

    def set_screen(self, screen : pygame.Surface) -> None:
        self.__screen = screen

    def set_ui_manager(self, ui_manager : pygame_gui.UIManager) -> None:
        self.__ui_manager = ui_manager

    def set_game_state_manager(self, game_state_manager:GameStateManager) -> None:
        self.__game_state_manager = game_state_manager

    def set_clock(self, clock: pygame.time.Clock) -> None:
        self.__clock = clock