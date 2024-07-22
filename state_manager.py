import copy


class GameStateManager:

    __active_state = None
    __states = {}

    def __init__(self) -> None:
        pass

    def register_state(self, new_state) -> None:
        if new_state.get_state_name() not in self.__states:
            self.__states[new_state.get_state_name()] = new_state

    def run(self, time_delta: int) -> None:
        if self.__active_state is not None:
            self.__active_state.handle_events()
            self.__active_state.run()
            self.__active_state.render(time_delta)
            self.__active_state.reset_event_polling()

            if self.__active_state.get_time_to_transition():
                self.__active_state.set_time_to_transition(False)
                new_state_name = self.__active_state.get_target_state_name()
                self.__active_state.end()
                outgoing_data_copy = copy.deepcopy(
                    self.__active_state.get_outgoing_transition_data()
                )
                self.__active_state = self.__states[new_state_name]
                self.__active_state.set_incoming_transition_data(outgoing_data_copy)
                self.__active_state.start()

            if self.__active_state.get_time_to_quit_app():
                return False

        return True

    def set_initial_state(self, initial_state_name) -> None:
        if initial_state_name in self.__states:
            self.__active_state = self.__states[initial_state_name]
            self.__active_state.start()
