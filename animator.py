import pygame

BASE_IMG_PATH = "assets/"


class Animation:
    __is_flipped: bool = False
    __is_done: bool = False
    __frame: int = 0
    __is_loop: bool = True
    __images: list[pygame.Surface] = []
    __image_duration: int = 5

    def __init__(
        self,
        images: list[pygame.Surface],
        image_duration=5,
        loop=True,
        is_flipped=False,
    ) -> None:
        self.__images = images
        self.__is_loop = loop
        self.__image_duration = image_duration
        self.__is_flipped = is_flipped

    # copy the instant of itself to decrease memory usage
    def copy(self):
        return Animation(
            self.__images, self.__image_duration, self.__is_loop, self.__is_flipped
        )

    def update(self) -> None:
        if self.__is_loop:
            self.__frame = (self.__frame + 1) % (
                self.__image_duration * len(self.__images)
            )
        else:
            self.__frame = min(
                self.__frame + 1, self.__image_duration * len(self.__images) - 1
            )
            if self.__frame >= self.__image_duration * len(self.__images) - 1:
                self.__is_done = True
        return

    def img(self) -> pygame.Surface:
        return (
            pygame.transform.flip(
                self.__images[
                    int(self.__frame / self.__image_duration)
                ].convert_alpha(),
                True,
                False,
            )
            if self.__is_flipped
            else self.__images[
                int(self.__frame / self.__image_duration)
            ].convert_alpha()
        )

    def is_done(self) -> bool:
        return self.__is_done
