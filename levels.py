import pygame as pg
from settings import *
import random
import pytmx

class Tiled_Map(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos) # sets top left corner equal to the x and y passed in // short cut for self.rect.x, and self.rect.y