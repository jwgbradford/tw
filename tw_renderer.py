import pygame, math, tw_c

class MyScreen:
    def __init__(self, width, height):
        pygame.init()
        self.cw = width / 2
        self.ch = height / 2
        self.game_window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TW - Client")

        # we're not storing objects for all the players in tw
        # just their id & images
        self.image_cache = {}
    
    def set_image_cache(self, player_data):
        for id in player_data:
            self.image_cache[id] = self.make_image()

    def redraw_window(self, player_data, my_id):
        self.game_window.fill((128,128,128))
        my_pos, my_dir = player_data[my_id]
        # if we have a background / scenery they must come first in our list
        for id in player_data:
            # unpack image_data except for our data
            if id != my_id:
                image = self.image_cache[id] 
                pos, angle = player_data[id]
                centered_pos = self.screen_offset(pos, my_pos)
                # rotating surfaces is a bit tricky so we use a separate function
                rotated_image, new_rect = self.image_rotate(image, centered_pos, angle)
                self.game_window.blit(rotated_image, new_rect)

        # now we draw the player - always last so always on the top 'layer'
        # the player is also always at the centre of the screen
        rotated_image, new_rect = self.image_rotate(self.image_cache[my_id], (self.cw, self.ch), my_dir)
        self.game_window.blit(rotated_image, new_rect)

        pygame.display.flip()

    def make_image(self):
        image = pygame.Surface((50, 25))
        image.set_colorkey(tw_c.BLACK)  # Black colors will not be blit.
        pygame.draw.rect(image, tw_c.RED, (0, 5, 50, 20))
        pygame.draw.circle(image, tw_c.GREEN, (25, 10), 10)
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


# code to test renderer #

if __name__ == '__main__':
    my_game = MyScreen(500, 500)
