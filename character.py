class Character:

    __name: str = None
    __statistics: dict = None
    __powerup: dict = None

    def __init__(self, name, statistics, powerup) -> None:
        self.__name = name
        self.__statistics = statistics
        self.__powerup = powerup

    def get_name(self) -> str:
        return self.__name

    def get_statistics(self) -> dict:
        return self.__statistics

    def get_powerup(self) -> dict:
        return self.__powerup

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_statistics(self, statistics: dict) -> None:
        self.__statistics = statistics

    def set_powerup(self, powerup: dict) -> None:
        self.__powerup = powerup
