#import pygame
from random import randint
#from renderer import MyScreen
from network import Network

class MyGame:
    def __init__(self):
        width = 500
        height = 500
        #elf.game_window = MyScreen(width, height)

    def main(self):
        run = True
        data = {}
        my_id = str(randint(0, 64000))
        data["id"] = my_id
        n = Network()
        while run:
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            keys = pygame.key.get_pressed()
            data["keys"] = keys
            '''
            data["send"] = input('data to send')
            n.send(data)
            player_data = n.receive()
            print(player_data)
            #self.game_window.redraw_window(player_data, my_id)

if __name__ == '__main__':
    my_game = MyGame()
    my_game.main()