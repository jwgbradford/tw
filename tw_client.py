import pygame
from random import randint
from tw_renderer import MyScreen
from tw_network import Network
from tw_game_engine import GameEngine as tw_ge

class MyGame:
    def __init__(self):
        width = 500
        height = 500
        self.game_window = MyScreen(width, height)
        # local config
        self.game_engine = tw_ge()

    def main(self):
        run = True
        
        my_id = str(randint(0, 64000))
        print('sending', my_id)

        # local config
        '''
        self.game_engine.add_player(my_id)
        keys = pygame.key.get_pressed()
        clock = pygame.time.Clock()
        starting_data = self.game_engine.update_objects()
        '''
        #end local config

        # network config
        n = Network()
        n.send(my_id)
        starting_data = n.receive()
        # end network config

        self.game_window.set_image_cache(starting_data)
        print('received', starting_data)


        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            keys = pygame.key.get_pressed()
            # local config
            '''
            self.game_engine.move_player(my_id, keys)
            self.game_engine.move_ai()
            player_data = self.game_engine.update_objects()
            '''
            #end local 

            # network config
            n.send(keys)
            player_data = n.receive()
            # end network

            self.game_window.redraw_window(player_data, my_id)
            # local clock tick
            #clock.tick(60)

if __name__ == '__main__':
    my_game = MyGame()
    my_game.main()