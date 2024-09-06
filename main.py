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
        self.game.push_state(self)

    def exit_state(self):
        self.game.pop_state()


class Title(State):
    def __init__(self, game):
        super().__init__(game)

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                new_state = GamePlay(self.game)
                new_state.enter_state()

    def update(self):
        pass

    def render(self, display):
        display.fill(self.game.BACKGROUND_COLOR)


class GamePlay(State):
    def __init__(self, game):
        super().__init__(game)

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.exit_state()

    def update(self):
        pass

    def render(self, display):
        display.fill((77, 77, 77))


class Game:
    def __init__(self):
        pg.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.BACKGROUND_COLOR = (255, 77, 77)
        self.canvas = pg.Surface((self.WIDTH, self.HEIGHT))
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.running, self.playing = True, True
        self.state_stack = [Title(self)]

    def get_state(self):
        return self.state_stack[-1]

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        self.state_stack.pop()

    def game_loop(self):
        while self.running:
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.get_state().events(event)

    def update(self):
        self.get_state().update()

    def render(self):
        self.get_state().render(self.canvas)
        self.screen.blit(self.canvas, (0, 0))
        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    g.game_loop()

