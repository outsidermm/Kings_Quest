class GameStateManager:
    __current_state = None

    def __init__(self, current_state):
        self.__current_state = current_state
        self.__transition = False

    def set_state(self, new_state):
        self.__current_state = new_state
        self.__transition = True

    def get_state(self):
        if self.__transition:
            self.__transition = False
            return self.__current_state, True
        return self.__current_state, False
