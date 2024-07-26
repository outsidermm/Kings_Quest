import copy


class GameStateManager:
    """
    Manages the states of the game, allowing transitions between different game states.
    """

    __active_state = None
    __states = {}

    def __init__(self) -> None:
        """
        Initializes the GameStateManager with no active state and an empty state registry.
        """
        pass

    def register_state(self, new_state) -> None:
        """
        Registers a new state in the state manager if it's not already registered.

        :param new_state: The state to register.
        """
        # Check if the state is already registered by comparing state names
        if new_state.get_state_name() not in self.get_states():
            # If not registered, add the new state to the states dictionary
            self.get_states()[new_state.get_state_name()] = new_state

    def run(self, time_delta: int) -> bool:
        """
        Runs the active state, handling events, running the state logic, rendering, and
        managing state transitions.

        :param time_delta: The time delta for the current frame.
        :return: False if the application should quit, True otherwise.
        """
        # Check if there is an active state
        if self.get_active_state() is not None:
            # Handle events for the active state
            self.get_active_state().handle_events()
            # Run the logic for the active state
            self.get_active_state().run()
            # Render the active state
            self.get_active_state().render(time_delta)
            # Reset event polling to prepare for the next frame
            self.get_active_state().reset_event_polling()

            # Check if a state transition is required
            if self.get_active_state().get_time_to_transition():
                # Reset the transition flag
                self.get_active_state().set_time_to_transition(False)
                # Get the name of the target state for the transition
                new_state_name = self.get_active_state().get_target_state_name()
                # End the current state
                self.get_active_state().end()
                # Make a deep copy of the outgoing transition data
                outgoing_data_copy = copy.deepcopy(
                    self.get_active_state().get_outgoing_transition_data()
                )
                # Set the new active state
                self.set_active_state(self.get_states()[new_state_name])
                # Pass the transition data to the new active state
                self.get_active_state().set_incoming_transition_data(outgoing_data_copy)
                # Start the new active state
                self.get_active_state().start()

            # Check if the application should quit
            if self.get_active_state().get_time_to_quit_app():
                return False

        return True

    def set_initial_state(self, initial_state_name: str) -> None:
        """
        Sets the initial state of the game manager to the specified state name.

        :param initial_state_name: The name of the initial state.
        """
        # Check if the specified initial state is registered
        if initial_state_name in self.get_states():
            # Set the active state to the initial state
            self.set_active_state(self.get_states()[initial_state_name])
            # Start the initial state
            self.get_active_state().start()

    # Getters and setters with docstrings

    def get_active_state(self):
        """
        Gets the current active state.

        :return: The current active state.
        """
        return self.__active_state

    def set_active_state(self, state) -> None:
        """
        Sets the current active state.

        :param state: The state to set as active.
        """
        self.__active_state = state

    def get_states(self) -> dict:
        """
        Gets the dictionary of registered states.

        :return: The dictionary of registered states.
        """
        return self.__states

    def set_states(self, states: dict) -> None:
        """
        Sets the dictionary of registered states.

        :param states: The new dictionary of registered states.
        """
        self.__states = states
