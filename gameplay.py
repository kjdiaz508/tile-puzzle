from state import State
import pygame as pg


class GamePlay(State):
    def __init__(self):
        super().__init__()

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                pass

    def update(self):
        pass

    def render(self, surface):
        surface.fill((77, 77, 77))