import json, pygame
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from tw_game_engine import GameEngine as tw_ge

class TinyWorld:
    def __init__(self):
        HOST = ''
        PORT = 5555
        ADDR = (HOST, PORT)
        self.game_engine = tw_ge()
        self.clients = {} # empty dictionary for client list
        # set up our server socket
        self.BUFSIZ = 2048
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(ADDR)
        self.SERVER.listen(5)
        print("Waiting for a connection, Server Started")

    # our threaded function to accept new players
    def accept_new_players(self):
        while True:
            player, player_addr = self.SERVER.accept()
            # start the player handler Thread
            Thread(target=self.handle_player, args=(player,)).start()

    # each player has a handler thread
    def handle_player(self, player_conn):
        player_data  = json.loads(player_conn.recv(self.BUFSIZ))
        # add new connection to clients
        my_id  = player_data["id"]
        self.clients[player_conn] = my_id
        self.game_engine.add_player(my_id)
        while True:
            # our main loop is to receive the keypresses from players
            try:
                data = json.loads(player_conn.recv(self.BUFSIZ))
                if not data:
                    print('Connection closed')
                    break
            except socket.error as e:
                print(e)
                break
            keys = data["keys"]
            self.game_engine.move_player((my_id, keys))

    # threaded code to run the game
    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        while True:
            self.game_engine.move_ai()
            self.game_engine.prepare_send_object()
            json_data = json.dumps(self.game_engine.send_object)
            for sock in self.clients:
                sock.send(json_data.encode())
            clock.tick(60)


    # send msg to all clients
    def broadcast(self, msg):
        for sock in self.clients:
            sock.send(msg.encode())

    def main(self):
        RUN_GAME = Thread(target=self.run_game)
        RUN_GAME.start()
        ACCEPT_THREAD = Thread(target=self.accept_new_players)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()

if __name__ == '__main__':
    tiny_world = TinyWorld()
    tiny_world.main()