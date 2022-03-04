import pygame
from os import path, system
from pprint import pprint
import time
from pygame import mixer
mixer.init() 
pygame.init()
clock = pygame.time.Clock()

################# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 64
pygame.mouse.set_visible(True)

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.display.set_caption("CHESS BOARD")

assets_dir = path.join(path.dirname(__file__), "assets_dir")
