import pygame, tw_c, math

class Player:
    def __init__(self, id, pos, dir):
        self.id = id
        self.x, self.y = pos
        self.dir = dir
        self.vel = 1
        self.turn = math.pi / 180
        self.player_image = self.make_image()
        self.WORLD_BOUNDARY = (tw_c.WORLD_SIZE / 2) - 500

    def update(self, keys):
        self.move(keys)

    def move(self, keys):
        # the json converstion strips out the object wrapping
        # so we can't use pygame built-in CONSTANT values
        # remember we are also moving the 'world' relative to our player
        # so pressing the up key makes the 'world' move down
        if keys[79]: # right
            self.dir -= self.turn
            if self.dir < 0:
                self.dir += 2 * math.pi
        if keys[80]: # left
            self.dir += self.turn
            if self.dir > 2 * math.pi:
                self.dir -= 2 * math.pi
        if keys[81]: # down
            self.y += self.vel * math.cos(self.dir)
            self.x += self.vel * math.sin(self.dir)
        if keys[82]: # up
            self.y -= self.vel * math.cos(self.dir)
            self.x -= self.vel * math.sin(self.dir)
        # if we 'cross' the world boundary, bounce back
        if self.y > self.WORLD_BOUNDARY:
            self.y -= self.vel + 1
        elif self.y < self.WORLD_BOUNDARY * -1:
            self.y += self.vel + 1
        if self.x > self.WORLD_BOUNDARY:
            self.x -= self.vel + 1
        elif self.x < self.WORLD_BOUNDARY * -1:
            self.x += self.vel + 1

    def make_image(self):
        image = pygame.Surface((50, 25))
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        pygame.draw.rect(image, tw_c.RED, (0, 5, 50, 20))
        pygame.draw.circle(image, tw_c.GREEN, (25, 10), 10)
        return image