import pygame as pg


class State:
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def events(self, event):
        pass

    def render(self, display):
        pass

    def enter_state(self):
        self.game.state = self


class Title(State):
    def __init__(self, game):
        super().__init__(game)

    def events(self, event):
        pass

    def update(self):
        pass

    def render(self, display):
        display.fill(c.BACKGROUND_COLOR)


class GamePlay(State):
    def __init__(self, game):
        super().__init__(game)

    def events(self, event):
        pass
    def update(self):
        pass

    def render(self, display):
        display.fill(c.PRIMARY_COLOR)


class Game:
    def __init__(self):
        pg.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.BACKGROUND_COLOR = (255, 77, 77)
        self.canvas = pg.Surface((self.WIDTH, self.HEIGHT))
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.running, self.playing = True, True
        self.state = Title(self)

    def game_loop(self):
        while self.running:
            self.get_events()
            self.state.events()
            self.update()
            self.render()

    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.state.events(event)

    def update(self):
        self.state.update()

    def render(self):
        self.state.render(self.canvas)
        self.screen.blit(self.canvas, (0, 0))
        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    g.game_loop()

