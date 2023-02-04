import pygame, tw_c, math

class GameObject(pygame.sprite.Sprite):
    def __init__(self, id, pos, dir):
        super().__init__()
        self.id = id
        self.x, self.y = pos
        self.dir = dir

    def make_image(self, design):
        surf = design["surface"]
        image = pygame.Surface(surf)
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        for element in design["design"]:
            element_colour = element["colour"]
            if element["shape"] == "poly":
                pygame.draw.polygon(image, element_colour, [(0,0), (20, 2.5), (0, 5)])
            elif element["shape"] == "rect":
                pygame.draw.rect(image, element_colour, (0, 5, 50, 20))
            elif element["shape"] == "circle":
                pygame.draw.circle(image, element_colour, (25, 10), 10)
        return image

class Character(GameObject):
    def __init__(self, id, pos, dir):
        super().__init__(id, pos, dir)
        self.vel = 1
        self.turn = math.pi / 180
        self.player_image = self.make_image()
        self.gcd = 0
        self.design_update = True

    def make_image(self):
        image = pygame.Surface((50, 25))
        head_colour = self.char_design["head_colour"]
        body_colour = self.char_design["body_colour"]
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        return image

class Player(Character):
    def __init__(self, id, pos, dir):
        self.char_design = {"head_colour" : tw_c.CYAN, "body_colour" : tw_c.PURPLE}
        super().__init__(id, pos, dir)
        self.WORLD_BOUNDARY = (tw_c.WORLD_SIZE / 2) - 500

    def update(self, keys):
        # the json converstion strips out the object wrapping
        # so we can't use pygame built-in CONSTANT values
        if keys[79] or keys[80] or keys[81] or keys[82]:
            self.move(keys)
        if keys[5] or keys[6]:
            self.change_costume(keys)
    
    def change_costume(self, keys):
        if self.gcd == 0:
            self.gcd = 2
            if keys[5]:
                body_colour = self.char_design["body_colour"]
                next_colour = next(tw_c.COLOURS)
                while body_colour != next_colour:
                    next_colour = next(tw_c.COLOURS)
                self.char_design["body_colour"] = next(tw_c.COLOURS)
                self.design_update = True
        if self.gcd == 0:
            self.gcd = 2
            if keys[6]:
                head_colour = self.char_design["head_colour"]
                next_colour = next(tw_c.COLOURS)
                while head_colour != next_colour:
                    next(tw_c.COLOURS)
                self.char_design["head_colour"] = next(tw_c.COLOURS)
                self.design_update = True

    def move(self, keys):
        # remember we are moving the 'world' relative to our player
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

class NPC(Character):
    def __init__(self, id, pos, dir):
        self.char_design = {"head_colour" : tw_c.MAGENTA, "body_colour" : tw_c.GREEN}
        super().__init__(id, pos, dir)

    def move(self):
        # not the most I of AI but walk in a circle
        self.dir += self.turn
        if self.dir > 2 * math.pi:
            self.dir -= 2 * math.pi
        self.y -= self.vel * math.cos(self.dir)
        self.x -= self.vel * math.sin(self.dir)

class Weapon(GameObject):
    def __init__(self, id, pos, dir):
        super().__init__(id, pos, dir)
        self.description = "a weapon"
        self.image = self.make_image()
        self.obj_design = {"name" : "small knife"}

    def make_image(self):
        image = pygame.Surface((20, 5))
        blade_colour = tw_c.YELLOW
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        pygame.draw.polygon(image, blade_colour, [(0,0), (20, 2.5), (0, 5)])
        return image