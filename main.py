import pygame as pg


class Game:
    def __init__(self):
        pg.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.BACKGROUND_COLOR = (255, 77, 77)
        self.canvas = pg.Surface((self.WIDTH, self.HEIGHT))
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pg.font.Font(None, 20)
        self.clock = pg.time.Clock()
        self.running, self.playing = True, True
        self.state_stack: list[State] = [Title(self)]

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
            self.state_stack[-1].events(event)

    def update(self):
        self.state_stack[-1].update()

    def render(self):
        self.state_stack[-1].render(self.canvas)
        self.screen.blit(self.canvas, (0, 0))
        pg.display.flip()

    def draw_text(self, surface: pg.Surface, text: str, position: tuple[int, int]):
        pass


class State:
    def __init__(self, game: Game):
        self.game = game

    def update(self):
        pass

    def events(self, event: pg.event.Event):
        pass

    def render(self, display: pg.Surface):
        pass

    def enter_state(self):
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()


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


if __name__ == "__main__":
    g = Game()
    g.game_loop()
