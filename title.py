from state import State
import pygame as pg
import config


class Title(State):
    def __init__(self):
        super().__init__()
        self.BACKGROUND_COLOR = (255, 77, 77)
        self.TEXT_COLOR = (51, 51, 51)
        self.next_state = "GamePlay"

        self.play_button = Button(
            self.switch_state,
            "Play Game",
            self.font,
            (config.SCREEN_RECT.centerx, config.SCREEN_RECT.centery),
            (10, 5),
            config.TILE_COLOR,
            self.TEXT_COLOR,
        )

    def events(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                pass
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.play_button.on_click(event)

    def render(self, surface: pg.surface.Surface):
        display_rect = surface.get_rect()
        surface.fill(self.BACKGROUND_COLOR)
        self.draw_text(
            "Tile Slider",
            surface,
            (display_rect.width // 2, display_rect.height * 0.20),
            self.TEXT_COLOR
        )
        self.play_button.draw(surface)


class Button:
    def __init__(self, command, text: str, font: pg.font.Font, center: tuple[int, int],
                 padding: tuple[int, int], bg_color: tuple[int, int, int], text_color: tuple[int, int, int]):
        self.command = command
        self.text = text
        self.surface = None
        self.rect = None
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

        self._generate_surface(center, padding)

    def _generate_surface(self, center, padding):
        text_surface = self.font.render(self.text, False, self.text_color)
        full_surface = pg.Surface(
            (text_surface.get_width() + 2 * padding[0], text_surface.get_height() + 2 * padding[1])
        )
        full_surface.fill(self.bg_color)
        full_surface.blit(text_surface, text_surface.get_rect(center=full_surface.get_rect().center))
        self.surface = full_surface
        self.rect = full_surface.get_rect(center=center)

    def draw(self, surface: pg.Surface):
        surface.blit(self.surface, self.rect)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.command()


