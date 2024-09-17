import random
from typing import Optional

from state import State
from title import Button
import pygame as pg
import config


class GamePlay(State):
    def __init__(self):
        super().__init__()
        self.img = None
        self.img_path = None
        self.grid = None
        self.next_state = 'Title'
        self.return_button = Button(
            self.switch_state,
            "Main Menu",
            self.font,
            (config.SCREEN_RECT.width // 2, 50),
            (20, 10),
            config.TILE_COLOR,
            config.FONT_COLOR
        )

    def events(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                pass
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.return_button.on_click(event)
            clicked = self.grid.get_clicked(pg.mouse.get_pos())
            if clicked is not None:
                self.grid.slide(clicked)

    def update(self):
        self.grid.update()

    def start_up(self, persistent):
        super().start_up(persistent)
        if self.grid is None or self.img_path != self.persistent["image_path"]:
            if self.persistent["image_path"]:
                self.img = pg.image.load(self.persistent["image_path"])
                self.img_path = self.persistent["image_path"]
            self.grid = Grid(self.img, 4)

    def render(self, surface: pg.surface.Surface):
        surface.fill((77, 77, 77))
        self.grid.draw(surface)
        self.return_button.draw(surface)


class Tile:
    def __init__(self, tile_id: int, image: Optional[pg.Surface], pos: tuple[int, int], rect: pg.rect.Rect):
        # initialized in helper
        self.surface = image
        self.image = image
        self.pos = pos
        self.rect = rect
        self.tile_id = tile_id
        self.font = pg.font.Font(config.FONT_PATH, 20)
        self.label = self.font.render(str(self.tile_id), False, config.FONT_COLOR)

        self.create_surface()

    def create_surface(self):
        if not self.surface:
            self.surface = pg.surface.Surface((self.rect.width, self.rect.height))
            self.surface.fill(config.TILE_COLOR)
        self.surface.blit(self.label, self.label.get_rect().move(10, 10))

    def draw(self, surface: pg.surface.Surface):
        surface.blit(self.surface, self.rect)

    def swap(self, other: 'Tile'):
        self.pos, other.pos = other.pos, self.pos
        self.rect, other.rect = other.rect, self.rect

    def is_clicked(self, point) -> bool:
        return self.rect.collidepoint(point)


class Grid:
    def __init__(self, image: Optional[pg.Surface], size: int):
        self.surface = pg.Surface((config.SCREEN_RECT.width, config.SCREEN_RECT.width))
        self.rect = self.surface.get_rect(bottom=(config.SCREEN_RECT.bottom - 100))
        self.size = size
        self.gap = 4

        self.tiles = []
        self.squares = []
        self.empty_tile = None
        self.last_switch: Optional[tuple[int, int]] = None
        self.image = image
        self.generate_tiles()

        self.solved = True
        self.scramble()

    def generate_tiles(self):
        tile_width = (self.rect.width - (self.gap * self.size) - self.gap) // self.size
        if self.image:
            self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
        for y in range(0, self.size):
            self.tiles.append([])
            for x in range(0, self.size):
                tile_id = (y * self.size + x) + 1
                coords = (self.gap + (x*(tile_width+self.gap)), self.gap + (y*(tile_width+self.gap)))
                rect = pg.rect.Rect(coords, (tile_width, tile_width))
                img = self.image.subsurface(rect) if self.image else None
                self.tiles[y].append(Tile(tile_id, img, (x, y), rect))
        self.empty_tile = self.tiles[-1][-1]
        self.last_switch = self.empty_tile.pos

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                if tile is not self.empty_tile:
                    tile.draw(self.surface)

    def slide(self, p: Tile):
        if not self.can_move(p):
            return
        self.last_switch = self.empty_tile.pos
        p_x, p_y = p.pos
        e_x, e_y = self.empty_tile.pos
        self.tiles[p_y][p_x], self.tiles[e_y][e_x] = self.tiles[e_y][e_x], self.tiles[p_y][p_x]
        self.empty_tile.swap(p)

    def get_clicked(self, point: tuple[int, int]) -> Optional[Tile]:
        offset = self.rect.top
        for row in self.tiles:
            for tile in row:
                if tile.is_clicked((point[0], point[1]-offset)):
                    return tile
        return None

    def update(self):
        self.solved = self.check_solved()

    def can_move(self, p: Tile):
        # cannot move diagonally to the empty tile
        x, y = p.pos
        e_x, e_y = self.empty_tile.pos
        if x == e_x:
            if y - 1 == e_y or y + 1 == e_y:
                return True
        elif y == e_y:
            if x - 1 == e_x or x + 1 == e_x:
                return True
        return False

    def check_solved(self):
        tile_num = 0
        for y in range(self.size):
            for x in range(self.size):
                tile_num += 1
                if self.tiles[y][x].tile_id != tile_num:
                    return False
        return True

    def valid_moves(self) -> list[tuple[int, int]]:
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

    def scramble(self, steps: int = 50):
        # must use valid moves to scramble the board to guarentee solve-ability
        for i in range(steps):
            choices = self.valid_moves()
            if self.last_switch in choices:
                choices.remove(self.last_switch)
            x, y = random.choice(choices)
            self.slide(self.tiles[y][x])

    def draw(self, surface: pg.surface.Surface):
        if self.solved:
            self.surface.fill((0, 255, 0))
        else:
            self.surface.fill((244, 11, 55))
        self.draw_tiles()
        surface.blit(self.surface, self.rect)
