import json_utility


class XP:
    def __init__(self, initial_xp: int) -> None:
        self.xp = initial_xp

    def gain_xp(self, new_xp: int) -> None:
        self.xp += new_xp
        user_setting = json_utility.read_json("settings/user_settings.json")
        user_setting["xp"] = self.xp
        json_utility.write_json("settings/user_settings.json", user_setting)

    def get_xp(self) -> int:
        return self.xp

    def set_xp(self, new_xp: int) -> None:
        self.xp = new_xp
        user_setting = json_utility.read_json("settings/user_settings.json")
        user_setting["xp"] = self.xp
        json_utility.write_json("settings/user_settings.json", user_setting)

    def lose_xp(self, lost_xp: int) -> None:
        if self.xp - lost_xp >= 0:
            self.xp -= lost_xp
            user_setting = json_utility.read_json("settings/user_settings.json")
            user_setting["xp"] = self.xp
            json_utility.write_json("settings/user_settings.json", user_setting)
        else:
            raise ValueError("Not Enough XP!")
