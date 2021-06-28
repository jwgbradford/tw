import pygame
pygame.init()
game_window = pygame.display.set_mode((100, 100))

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    keys = pygame.key.get_pressed()
    print(keys)
    clock.tick(1)