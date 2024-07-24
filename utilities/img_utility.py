import pygame
import os

BASE_IMG_PATH = "assets/"


# load a image from a given path into a pygame surface
def load_image(path: str) -> pygame.Surface:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


# load a group of images from a given folder into a list of pygame surfaces
def load_images(path: str) -> list[pygame.Surface]:
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images
