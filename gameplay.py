from state import State
import pygame as pg
import config


class GamePlay(State):
    def __init__(self):
        super().__init__()
        self.grid = Grid(2)

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                pass
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            clicked = self.grid.get_clicked(pg.mouse.get_pos())
            if clicked is not None:
                self.grid.slide(clicked)

    def update(self):
        pass

    def render(self, surface):
        surface.fill((77, 77, 77))
        self.grid.draw(surface)


class Tile:
    def __init__(self, tile_id, pos, rect):
        # initialized in helper
        self.surface = None

        self.pos = pos
        self.rect = rect
        self.tile_id = tile_id
        self.font = pg.font.Font(config.FONT_PATH, 20)
        self.label = self.font.render(str(self.tile_id), False, config.FONT_COLOR)

        self.create_surface()

    def create_surface(self):
        surface = pg.surface.Surface((self.rect.width, self.rect.height))
        surface.fill(config.TILE_COLOR)
        surface.blit(self.label, self.label.get_rect().move(10, 10))
        self.surface = surface

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def swap(self, other):
        self.pos, other.pos = other.pos, self.pos
        self.rect, other.rect = other.rect, self.rect

    def is_clicked(self, point):
        return self.rect.collidepoint(point)


class Grid:
    def __init__(self, size: int):
        self.surface = pg.Surface((config.SCREEN_RECT.width, config.SCREEN_RECT.width))
        self.rect = self.surface.get_rect(bottom=(config.SCREEN_RECT.bottom - 100))
        self.size = size
        self.gap = 4
        self.tiles = []
        self.squares = []
        self.empty_tile = None
        self.generate_tiles()

    def generate_tiles(self):
        tile_width = (self.rect.width - (self.gap * self.size) - self.gap) // self.size
        for y in range(0, self.size):
            self.tiles.append([])
            for x in range(0, self.size):
                tile_id = (y * self.size + x) + 1
                coords = (self.gap + (x*(tile_width+self.gap)), self.gap + (y*(tile_width+self.gap)))
                self.tiles[y].append(Tile(tile_id, (x, y), pg.rect.Rect(coords, (tile_width, tile_width))))
        self.empty_tile = self.tiles[-1][-1]

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                if tile is not self.empty_tile:
                    tile.draw(self.surface)

    def slide(self, p):
        if not self.can_move(p):
            return
        p_x, p_y = p.pos
        e_x, e_y = self.empty_tile.pos
        self.tiles[p_y][p_x], self.tiles[e_y][e_x] = self.tiles[e_y][e_x], self.tiles[p_y][p_x]
        self.empty_tile.swap(p)
        print(self.empty_tile.rect, p.rect)

    def get_clicked(self, point):
        offset = self.rect.top
        print(offset)
        for row in self.tiles:
            for tile in row:
                if tile.is_clicked((point[0], point[1]-offset)):
                    return tile
        return None

    def can_move(self, p):
        # cannot move diagonally to the empty tile
        x, y = p.pos
        print(p.pos)
        e_x, e_y = self.empty_tile.pos
        print(self.empty_tile.pos)
        if x == e_x:
            if y - 1 == e_y or y + 1 == e_y:
                return True
        elif y == e_y:
            if x - 1 == e_x or x + 1 == e_x:
                return True
        return False

    def valid_moves(self):
        x, y = self.empty_tile.pos
        adj = []
        if y - 1 >= 0:
            adj.append((x, y - 1))
        if y + 1 < self.size:
            adj.append((x, y + 1))
        if x - 1 >= 0:
            adj.append((x - 1, y))
        if x + 1 < self.size:
            adj.append((x + 1, y))
        return adj

    def draw(self, surface):
        self.surface.fill((0, 0, 0))
        self.draw_tiles()
        surface.blit(self.surface, self.rect)
