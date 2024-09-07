import pygame as pg
import os

BACKGROUND_COLOR = (255, 77, 77)
SCREEN_SIZE = (600, 800)
TILE_COLOR = (240, 240, 240)
PRIMARY_COLOR = (74, 74, 74)
ACCENT_COLOR = (255, 102, 102)
FONT_COLOR = (51, 51, 51)

# initialization
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()
