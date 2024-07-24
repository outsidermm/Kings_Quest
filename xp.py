from utilities.json_utility import read_json, write_json


class XP:
    """
    XP class to manage experience points for a user, including gaining, losing, and setting XP.
    """

    def __init__(self, initial_xp: int) -> None:
        """
        Initializes the XP class with an initial amount of XP.

        :param initial_xp: The initial amount of XP.
        """
        self.set_xp(initial_xp)

    def gain_xp(self, new_xp: int) -> None:
        """
        Increases the user's XP by the specified amount and updates the settings file.

        :param new_xp: The amount of XP to gain.
        """
        self.set_xp(self.get_xp() + new_xp)

    def lose_xp(self, lost_xp: int) -> None:
        """
        Decreases the user's XP by the specified amount if sufficient XP is available.
        Updates the settings file. Raises an error if not enough XP.

        :param lost_xp: The amount of XP to lose.
        :raises ValueError: If not enough XP is available.
        """
        if self.get_xp() - lost_xp >= 0:
            self.set_xp(self.get_xp() - lost_xp)
        else:
            raise ValueError("Not Enough XP!")

    def get_xp(self) -> int:
        """
        Gets the current amount of XP.

        :return: The current amount of XP.
        """
        return self.__xp

    def set_xp(self, new_xp: int) -> None:
        """
        Sets the current amount of XP and updates the settings file.

        :param new_xp: The new amount of XP.
        """
        self.__xp = new_xp
        user_setting = read_json("settings/user_settings.json")
        user_setting["xp"] = self.__xp
        write_json("settings/user_settings.json", user_setting)
