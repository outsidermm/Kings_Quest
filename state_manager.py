class GameStateManager:
    __current_state = None

    def __init__(self, current_state):
        self.__current_state = current_state

    def set_state(self, new_state):
        self.__current_state = new_state

    def get_state(self):
        return self.__current_state
