class XP:
    def __init__(self, initial_xp: int) -> None:
        self.xp = initial_xp

    def gain_xp(self, new_xp: int) -> None:
        self.xp += new_xp

    def get_xp(self) -> int:
        return self.xp

    def set_xp(self, new_xp: int) -> None:
        self.xp = new_xp

    def lose_xp(self, lost_xp: int) -> None:
        if self.xp - lost_xp >= 0:
            self.xp -= lost_xp
        else:
            raise ValueError("Not Enough XP!")
