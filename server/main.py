import pygame
from threading import Thread
from network import Network
from settings import GAME_SPEED
#from tw_game_engine import GameEngine as tw_ge
#from tw_c import GAME_SPEED

class TinyWorld:
    def __init__(self) -> None:
        #self.game_engine = tw_ge()
        self.clients = {} # empty dictionary for client list
        # set up our server socket
        self.network = Network()
        self.network.SERVER.listen(5) # limit to 5 concurrent players
        print("Waiting for a connection, Server Started")

    # our threaded function to accept new players
    def accept_new_players(self):
        while True:
            player, player_addr = self.network.SERVER.accept()
            # start each player handler Thread
            Thread(target=self.handle_player, args=(player,)).start()

    # each player has a handler thread
    def handle_player(self, player_conn):
        player_data  = player_conn.get_data()
        my_id  = player_data["id"]
        # add new connection to clients
        self.clients[player_conn] = my_id
        #self.game_engine.add_player(my_id)
        while True:
            # our main loop is to receive the keypresses
            try:
                data = player_conn.get_data()
            except:
                print('Connection lost')
                break
            #keys = data["keys"]
            #update_data = (my_id, keys)
            #self.game_engine.update_player(update_data)
            print(data)
        # clean up our registries
        #del self.game_engine.player_dict[my_id]
        #del self.clients[player_conn]
        player_conn.close()

    # threaded code to run the game
    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        msg_id = 1
        while True:
            #data_to_send = self.game_engine.prepare_send_object()
            data_to_send = {"data" : msg_id}
            for sock in self.clients:
                sock.send_data(data_to_send)
            msg_id += 1
            clock.tick(GAME_SPEED)

    def main(self):
        RUN_GAME = Thread(target=self.run_game)
        RUN_GAME.start()
        ACCEPT_THREAD = Thread(target=self.accept_new_players)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.network.close()

if __name__ == '__main__':
    tiny_world = TinyWorld()
    tiny_world.main()