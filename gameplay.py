from state import State
import pygame as pg
import config


class GamePlay(State):
    def __init__(self):
        super().__init__()
        self.grid = Grid(4)

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                pass

    def update(self):
        pass

    def render(self, surface):
        surface.fill((77, 77, 77))
        self.grid.draw(surface)


class Tile:
    def __init__(self, tile_id, size):
        self.tile_id = tile_id
        self.size = size
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect()
        self.font = pg.font.Font(config.FONT_PATH, 20)
        self.label = self.font.render(str(self.tile_id), False, config.FONT_COLOR)
        self.create_surface()

    def update(self):
        pass

    def create_surface(self):
        self.surface.fill(config.TILE_COLOR)
        self.surface.blit(self.label, self.label.get_rect().move(10, 10))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Grid:
    def __init__(self, size: int):
        self.surface = pg.Surface((config.SCREEN_RECT.width, config.SCREEN_RECT.width))
        self.rect = self.surface.get_rect(bottom=(config.SCREEN_RECT.bottom - 100))
        self.size = size
        self.gap = 4

        # TODO: rework the logic here to use the rects of the tiles instead of subsurfaces
        self.tiles = []
        self.surfaces = []
        self.generate_tiles()

    def generate_tiles(self):
        tile_width = (self.rect.width - (self.gap * self.size) - self.gap) // self.size
        for i in range(0, self.size):
            for j in range(0, self.size):
                tile_id = (j * self.size + i) + 1
                coords = (self.gap + (i*(tile_width+self.gap)), self.gap + (j*(tile_width+self.gap)))
                self.tiles.append(Tile(tile_id, (tile_width, tile_width)))
                self.surfaces.append(self.surface.subsurface(pg.rect.Rect(coords, (tile_width, tile_width))))
        self.tiles.pop()

    def draw_tiles(self):
        for i, tile in enumerate(self.tiles):
            tile.draw(self.surfaces[i])

    def draw(self, surface):
        self.draw_tiles()
        surface.blit(self.surface, self.rect)





