import json_utility


class Quest:
    __name: str = ""
    __description: str = ""
    __reward: int = 0
    __aim: int = 0
    __progress: int = 0
    __is_claimed: bool = False

    def __init__(
        self,
        name: str,
        description: str,
        aim: int,
        reward: int,
    ) -> None:
        self.__name = name
        self.__description = description
        self.__reward = reward
        self.__progress = json_utility.read_json("settings/user_settings.json")[
            "quest_progress"
        ][self.__name]
        self.__aim = aim
        self.__is_claimed = json_utility.read_json("settings/user_settings.json")[
            "quest_claimed"
        ][self.__name]

    def increment_progress(self, increment: int) -> None:
        self.__progress += increment
        user_setting = json_utility.read_json("settings/user_settings.json")
        user_setting["quest_progress"][self.__name] = self.__progress
        json_utility.write_json("settings/user_settings.json", user_setting)

    def is_done(self) -> bool:
        return self.__progress >= self.__aim

    def claim(self) -> None:
        self.__is_claimed = True
        user_setting = json_utility.read_json("settings/user_settings.json")
        user_setting["quest_claimed"][self.__name] = self.__is_claimed
        json_utility.write_json("settings/user_settings.json", user_setting)

    def is_claimed(self) -> bool:
        return self.__is_claimed

    def get_name(self) -> str:
        return self.__name

    def get_description(self) -> str:
        return self.__description

    def get_reward(self) -> int:
        return self.__reward

    def get_progress(self) -> int:
        return self.__progress

    def get_aim(self) -> int:
        return self.__aim

    def set_progress(self, progress: int) -> None:
        self.__progress = progress

    def set_aim(self, aim: int) -> None:
        self.__aim = aim

    def set_reward(self, reward: int) -> None:
        self.__reward = reward

    def set_description(self, description: str) -> None:
        self.__description = description

    def set_name(self, name: str) -> None:
        self.__name = name
