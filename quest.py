from utilities.json_utility import read_json, write_json


class Quest:
    """
    Quest class representing a quest with various attributes such as name, description, reward, aim, and progress.
    """

    __name: str = ""
    __description: str = ""
    __reward: int = 0
    __aim: int = 0
    __progress: int = 0
    __is_claimed: bool = False
    __is_temporary: bool = False

    def __init__(
        self,
        name: str,
        description: str,
        aim: int,
        reward: int,
        is_temporary: bool = False,
    ) -> None:
        """
        Initializes the Quest class.

        :param name: Name of the quest.
        :param description: Description of the quest.
        :param aim: The aim/goal of the quest.
        :param reward: The reward for completing the quest.
        :param is_temporary: Whether the quest is temporary.
        """
        self.set_name(name)
        self.set_description(description)
        self.set_reward(reward)
        self.set_aim(aim)
        self.set_is_temporary(is_temporary)
        if not is_temporary:
            user_settings = read_json("settings/user_settings.json")
            self.set_progress(user_settings["quest_progress"].get(name, 0))
            self.set_is_claimed(user_settings["quest_claimed"].get(name, False))

    def copy(self) -> "Quest":
        """
        Creates a copy of the quest instance.

        :return: A new instance of Quest with the same attributes.
        """
        return Quest(
            self.get_name(),
            self.get_description(),
            self.get_aim(),
            self.get_reward(),
            self.get_is_temporary(),
        )

    def increment_progress(self, increment: int) -> None:
        """
        Increments the progress of the quest.

        :param increment: The amount to increment the progress by.
        """
        self.set_progress(self.get_progress() + increment)
        if not self.get_is_temporary():
            user_settings = read_json("settings/user_settings.json")
            user_settings["quest_progress"][self.get_name()] = self.get_progress()
            write_json("settings/user_settings.json", user_settings)

    def is_done(self) -> bool:
        """
        Checks if the quest is done.

        :return: True if the progress is greater than or equal to the aim, False otherwise.
        """
        return self.get_progress() >= self.get_aim()

    def claim(self) -> None:
        """
        Marks the quest as claimed.
        """
        self.set_is_claimed(True)
        if not self.get_is_temporary():
            user_settings = read_json("settings/user_settings.json")
            user_settings["quest_claimed"][self.get_name()] = self.get_is_claimed()
            write_json("settings/user_settings.json", user_settings)

    # Getters and setters with docstrings

    def get_name(self) -> str:
        """
        Gets the name of the quest.

        :return: The name of the quest.
        """
        return self.__name

    def set_name(self, name: str) -> None:
        """
        Sets the name of the quest.

        :param name: The new name of the quest.
        """
        self.__name = name

    def get_description(self) -> str:
        """
        Gets the description of the quest.

        :return: The description of the quest.
        """
        return self.__description

    def set_description(self, description: str) -> None:
        """
        Sets the description of the quest.

        :param description: The new description of the quest.
        """
        self.__description = description

    def get_reward(self) -> int:
        """
        Gets the reward of the quest.

        :return: The reward of the quest.
        """
        return self.__reward

    def set_reward(self, reward: int) -> None:
        """
        Sets the reward of the quest.

        :param reward: The new reward of the quest.
        """
        self.__reward = reward

    def get_aim(self) -> int:
        """
        Gets the aim/goal of the quest.

        :return: The aim of the quest.
        """
        return self.__aim

    def set_aim(self, aim: int) -> None:
        """
        Sets the aim/goal of the quest.

        :param aim: The new aim of the quest.
        """
        self.__aim = aim

    def get_progress(self) -> int:
        """
        Gets the progress of the quest.

        :return: The progress of the quest.
        """
        return self.__progress

    def set_progress(self, progress: int) -> None:
        """
        Sets the progress of the quest.

        :param progress: The new progress of the quest.
        """
        self.__progress = progress

    def get_is_claimed(self) -> bool:
        """
        Gets the claimed status of the quest.

        :return: True if the quest is claimed, False otherwise.
        """
        return self.__is_claimed

    def set_is_claimed(self, is_claimed: bool) -> None:
        """
        Sets the claimed status of the quest.

        :param is_claimed: The new claimed status of the quest.
        """
        self.__is_claimed = is_claimed

    def get_is_temporary(self) -> bool:
        """
        Gets the temporary status of the quest.

        :return: True if the quest is temporary, False otherwise.
        """
        return self.__is_temporary

    def set_is_temporary(self, is_temporary: bool) -> None:
        """
        Sets the temporary status of the quest.

        :param is_temporary: The new temporary status of the quest.
        """
        self.__is_temporary = is_temporary