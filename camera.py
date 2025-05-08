import pygame as pg
from settings import *


class Camera():
    def __init__(self, width, height):
        
        # super().__init__(group)

        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    
    def get_view(self, sprite_object):
        return sprite_object.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + VIEW_WIDTH / 2
        y = -target.rect.y + VIEW_HEIGHT / 2

        x = min(0, x)
        y = min(0, y)

        x = max(-1 * (self.width - VIEW_WIDTH), x)
        y = max(-1 * (self.height - VIEW_HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)