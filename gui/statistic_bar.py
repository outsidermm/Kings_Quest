from pygame_gui.elements import UIStatusBar

class StatisticBar(UIStatusBar):
    """
    Custom UIStatusBar class to represent a statistic bar with text.

    Attributes:
        bar_text (str): Text to display on the bar.
    """

    def __init__(
        self,
        text: str = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the StatisticBar with a text and other arguments.

        :param text: Text to display on the bar.
        """
        self.set_bar_text(text)  # Set the initial bar text
        super().__init__(*args, **kwargs)

    def status_text(self) -> str:
        """
        Returns the text of the bar.

        :return: The bar text.
        """
        return self.get_bar_text()  # Return the current text of the bar

    def set_text(self, text: str) -> None:
        """
        Sets the text of the bar.

        :param text: Text to set.
        """
        self.set_bar_text(text)  # Update the text of the bar

    def get_bar_text(self) -> str:
        """
        Gets the current text of the bar.

        :return: The bar text.
        """
        return self.__bar_text  # Return the bar text

    def set_bar_text(self, text: str) -> None:
        """
        Sets the text of the bar.

        :param text: Text to set.
        """
        self.__bar_text = text  # Set the bar text