import pygame, math, tw_c, itertools

class MyScreen:
    def __init__(self, width, height):
        pygame.init()
        self.cw = width / 2
        self.ch = height / 2
        self.game_window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TW - Client")
        # we're not storing objects for all the players in tw
        # just their id & images
        self.player_image_cache = {}
        self.item_image_cache = {}
        self.background = self.make_background()
        self.origin = (-5000, -5000)
        self.update_rect = pygame.Rect(0, 0, width, height)
    
    def set_image_cache(self, player_data):
        for id in player_data:
            self.player_image_cache[id] = self.make_image()
        
    def add_player_image(self, id, image_data):
        self.player_image_cache[id] = self.make_image(image_data)

    def redraw_window(self, display_data, my_id):
        # background first
        my_pos = display_data["players"][my_id]["pos_data"][0]
        background_offset = self.screen_offset(self.origin, my_pos)
        self.game_window.blit(self.background, background_offset)
        # then game objects
        game_items = display_data["items"]
        self.display_items(game_items, my_pos)
        # then players
        player_data = display_data["players"]
        self.display_players(player_data, my_id)
        pygame.display.update(self.update_rect)

    def display_items(self, game_items, my_pos):
        for id in game_items:
            if id not in self.player_image_cache or player_data[id]["char_design"]["update"]:
                image_data = player_data[id]["char_design"]
                self.add_player_image(id, image_data)
            # unpack image_data except for our data
            if id != my_id:
                image = self.player_image_cache[id] 
                pos, angle = player_data[id]["pos_data"]
                centered_pos = self.screen_offset(pos, my_pos)
                # rotating surfaces is a bit tricky so we use a separate function
                rotated_image, new_rect = self.image_rotate(image, centered_pos, angle)
                self.game_window.blit(rotated_image, new_rect)

    def display_players(self, player_data, my_id):
        my_pos, my_dir = player_data[my_id]["pos_data"]
        for id in player_data:
            if id not in self.player_image_cache or player_data[id]["char_design"]["update"]:
                image_data = player_data[id]["char_design"]
                self.add_player_image(id, image_data)
            # unpack image_data except for our data
            if id != my_id:
                image = self.player_image_cache[id] 
                pos, angle = player_data[id]["pos_data"]
                centered_pos = self.screen_offset(pos, my_pos)
                # rotating surfaces is a bit tricky so we use a separate function
                rotated_image, new_rect = self.image_rotate(image, centered_pos, angle)
                self.game_window.blit(rotated_image, new_rect)
        # now we draw the player - always last so always on the top 'layer'
        # the player is also always at the centre of the screen
        rotated_image, new_rect = self.image_rotate(
            self.player_image_cache[my_id], 
            (self.cw, self.ch), 
            my_dir)
        self.game_window.blit(rotated_image, new_rect)

    def make_image(self, image_data):
        body_colour = image_data["body_colour"]
        head_colour = image_data["head_colour"]
        image = pygame.Surface((50, 25))
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        pygame.draw.rect(image, body_colour, (0, 5, 50, 20))
        pygame.draw.circle(image, head_colour, (25, 10), 10)
        return image

    def image_rotate(self, image, topleft, rad_angle):
        # our angles are in radians, need to convert to degrees
        deg_angle = rad_angle * (180 / math.pi)
        rotated_image = pygame.transform.rotate(image, deg_angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
        return rotated_image, new_rect
    
    def screen_offset(self, pos, player_pos):
        abs_x, abs_y = pos
        player_x, player_y = player_pos
        # work out relative position of each image to the player
        rel_x = abs_x - player_x
        rel_y = abs_y - player_y
        # player is now (0, 0)
        # then centre everything on the player
        centered_x = rel_x + self.cw
        centered_y = rel_y + self.ch
        return (centered_x, centered_y)

    def make_background(self): # this function creates a single image background
        # set up a simple list of images that we can iterate through
        images = itertools.cycle((tw_c.BLUE_IMAGE, tw_c.GRAY_IMAGE))
        background = pygame.Surface((tw_c.WORLD_SIZE, tw_c.WORLD_SIZE))
        TILES = int(tw_c.WORLD_SIZE / tw_c.TILE_SIZE)
        # Use two nested for loops to get the coordinates.
        for row in range(TILES):
            for column in range(TILES):
                # This alternates between the blue and gray image.
                image = next(images)
                # Blit one image after the other at their respective coords
                background.blit(
                    image, 
                    ((row * tw_c.TILE_SIZE) + tw_c.OFFSET, 
                        (column * tw_c.TILE_SIZE) + tw_c.OFFSET)
                    )
            next(images)
        #returns a surface, ready to be sent to the screen
        return background