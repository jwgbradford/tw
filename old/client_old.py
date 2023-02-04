import pygame
from tw_renderer import MyScreen
from tw_network import Network
from tw_game_engine import GameEngine as tw_ge

class MyGame:
    def __init__(self):
        width = 500
        height = 500
        self.game_window = MyScreen(width, height)
        self.game_engine = tw_ge()

    def main(self):
        run = True
        #n = Network()
        keys = pygame.key.get_pressed()
        temp_id = 0
        starting_data = self.game_engine.update_objects(keys, temp_id)
        self.game_window.set_image_cache(starting_data)
        clock = pygame.time.Clock()

        while run:
            my_id = next(iter(self.game_engine.object_dict))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            keys = pygame.key.get_pressed()
            player_data = self.game_engine.update_objects(keys, my_id)
            '''
            n.send(keys)
            print(n.receive())
            player_data = n.receive()
            '''
            self.game_window.redraw_window(player_data, my_id)
            clock.tick(60)

if __name__ == '__main__':
    my_game = MyGame()
    my_game.main()