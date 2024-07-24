import pygame

BASE_IMG_PATH = "assets/"


class Animation:
    """
    Animation class to handle sprite animations.
    """

    __is_flipped: bool = False
    __is_done: bool = False
    __frame: int = 0
    __is_loop: bool = True
    __imgs: list[pygame.Surface] = []
    __img_duration: int = 5

    def __init__(
        self,
        images: list[pygame.Surface],
        image_duration=5,
        loop=True,
        is_flipped=False,
    ) -> None:
        """
        Initializes the Animation class.

        :param images: List of images for the animation.
        :param image_duration: Duration each image is displayed.
        :param loop: Whether the animation should loop.
        :param is_flipped: Whether the animation should be flipped horizontally.
        """
        self.set_imgs(images)
        self.set_is_loop(loop)
        self.set_img_duration(image_duration)
        self.set_is_flipped(is_flipped)

    def copy(self) -> "Animation":
        """
        Creates a copy of the animation instance.

        :return: A new instance of Animation with the same attributes.
        """
        return Animation(
            self.get_imgs(),
            self.get_img_duration(),
            self.get_is_loop(),
            self.get_is_flipped(),
        )

    def update(self) -> None:
        """
        Updates the current frame of the animation.
        """
        if self.get_is_loop():
            self.set_frame(
                (self.get_frame() + 1)
                % (self.get_img_duration() * len(self.get_imgs()))
            )
        else:
            self.set_frame(
                min(
                    self.get_frame() + 1,
                    self.get_img_duration() * len(self.get_imgs()) - 1,
                )
            )
            if self.get_frame() >= self.get_img_duration() * len(self.get_imgs()) - 1:
                self.set_is_done(True)

    def img(self) -> pygame.Surface:
        """
        Returns the current image of the animation.

        :return: The current pygame.Surface image.
        """
        current_img = self.get_imgs()[
            int(self.get_frame() / self.get_img_duration())
        ].convert_alpha()
        if self.get_is_flipped():
            return pygame.transform.flip(current_img, True, False)
        else:
            return current_img

    def is_done(self) -> bool:
        """
        Checks if the animation is done.

        :return: True if the animation is done, False otherwise.
        """
        return self.get_is_done()

    def get_is_flipped(self) -> bool:
        """
        Gets the flipped status of the animation.

        :return: True if the animation is flipped, False otherwise.
        """
        return self.__is_flipped

    def set_is_flipped(self, value: bool) -> None:
        """
        Sets the flipped status of the animation.

        :param value: The new flipped status.
        """
        self.__is_flipped = value

    def get_is_loop(self) -> bool:
        """
        Gets the loop status of the animation.

        :return: True if the animation loops, False otherwise.
        """
        return self.__is_loop

    def set_is_loop(self, value: bool) -> None:
        """
        Sets the loop status of the animation.

        :param value: The new loop status.
        """
        self.__is_loop = value

    def get_img_duration(self) -> int:
        """
        Gets the image duration of the animation.

        :return: The duration each image is displayed.
        """
        return self.__img_duration

    def set_img_duration(self, value: int) -> None:
        """
        Sets the image duration of the animation.

        :param value: The new image duration.
        """
        self.__img_duration = value

    def get_frame(self) -> int:
        """
        Gets the current frame of the animation.

        :return: The current frame.
        """
        return self.__frame

    def set_frame(self, value: int) -> None:
        """
        Sets the current frame of the animation.

        :param value: The new frame.
        """
        self.__frame = value

    def get_imgs(self) -> list[pygame.Surface]:
        """
        Gets the list of images for the animation.

        :return: The list of images.
        """
        return self.__imgs

    def set_imgs(self, value: list[pygame.Surface]) -> None:
        """
        Sets the list of images for the animation.

        :param value: The new list of images.
        """
        self.__imgs = value

    def get_is_done(self) -> bool:
        """
        Gets the done status of the animation.

        :return: True if the animation is done, False otherwise.
        """
        return self.__is_done

    def set_is_done(self, value: bool) -> None:
        """
        Sets the done status of the animation.

        :param value: The new done status.
        """
        self.__is_done = value
