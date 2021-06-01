import pygame, tw_c, math

class Player:
    def __init__(self, id, pos, dir):
        self.id = id
        self.x, self.y = pos
        self.dir = dir
        self.vel = 1
        self.turn = math.pi / 180
        self.player_image = self.make_image()

    def update(self, keys):
        self.move(keys)

    def move(self, keys):
        print(pygame.K_LEFT)
        if keys[pygame.K_LEFT]:
            self.dir += self.turn
            if self.dir > 2 * math.pi:
                self.dir -= 2 * math.pi
        if keys[pygame.K_RIGHT]:
            self.dir -= self.turn
            if self.dir < 0:
                self.dir += 2 * math.pi
        if keys[pygame.K_UP]:
            self.y -= self.vel * math.cos(self.dir)
            self.x -= self.vel * math.sin(self.dir)
        if keys[pygame.K_DOWN]:
            self.y += self.vel * math.cos(self.dir)
            self.x += self.vel * math.sin(self.dir)

    def make_image(self):
        image = pygame.Surface((50, 25))
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        pygame.draw.rect(image, tw_c.RED, (0, 5, 50, 20))
        pygame.draw.circle(image, tw_c.GREEN, (25, 10), 10)
        return image