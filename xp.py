class XP:
    def __init__(self):
        self.xp = 1000

    def gain_xp(self, new_xp: int):
        self.xp += new_xp

    def get_xp(self):
        return self.xp

    def set_xp(self, new_xp: int):
        self.xp = new_xp

    def lose_xp(self, lost_xp: int):
        if self.xp - lost_xp >= 0:
            self.xp -= lost_xp
        else:
            raise ValueError("Not Enough XP!")
