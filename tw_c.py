import pygame

# rgb colours
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
YELLOW, CYAN, MAGENTA, PURPLE = (255, 255, 50), (255, 50, 255), (200,0, 200), (200, 165, 0)
COLOURS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, PURPLE]

WORLD_SIZE = 10000
TILE_SIZE = 100
OFFSET = 25
BLUE_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
BLUE_IMAGE.fill(pygame.Color('lightskyblue2'))
GRAY_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
GRAY_IMAGE.fill(pygame.Color('slategray4'))