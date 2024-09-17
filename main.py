import sys
import tkinter as tk
import pygame as pg
import config
from title import Title
from gameplay import GamePlay


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.get_surface()
        self.canvas = pg.Surface((self.screen.get_width(), self.screen.get_height()))
        self.font_color = config.FONT_COLOR
        self.clock = pg.time.Clock()
        self.fps = 60
        self.running, self.playing = True, True

        self.state_dict = {
            "Title": Title(),
            "GamePlay": GamePlay()
        }
        self.state_name = "Title"
        self.state = self.state_dict[self.state_name]
        self.persistent = {
            "image_path": None,
        }
        self.state.start_up(self.persistent)

    def game_loop(self):
        while self.running:
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.state.events(event)

    def update(self):
        if self.state.quit:
            self.running = False
        elif self.state.done:
            self.change_state()
        self.state.update()

    def change_state(self):
        # switching the state
        old_state = self.state_name
        self.state_name = self.state.next_state
        self.state = self.state_dict[self.state_name]
        # setting up the new state
        self.state.previous_state = old_state
        self.state.start_up(self.persistent)

    def render(self):
        self.state.render(self.canvas)
        self.screen.blit(self.canvas, (0, 0))
        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    g.game_loop()
    pg.quit()
    sys.exit()
