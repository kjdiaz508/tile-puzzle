import pygame as pg
import os


class State:
    def __init__(self):
        # done signals to change the state
        self.done = False
        # signals to quit completely
        self.quit = False
        self.next_state: str | None = None
        self.previous_state: str | None = None
        self.persistent = None
        self.font = pg.font.Font(os.path.join("press-start-2p-font", "PressStart2P-vaV7.ttf"), 30)

    def update(self):
        pass

    def events(self, event: pg.event.Event):
        pass

    def render(self, surface: pg.Surface):
        pass

    def switch_state(self):
        self.done = True

    def start_up(self, persistent):
        # in case a state is being re-entered
        self.persistent = persistent
        self.done = False

    def draw_text(self, text: str, surface: pg.Surface, center: tuple[int, int], color):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = center
        surface.blit(text_surface, text_rect)
