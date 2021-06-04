import socket, pygame, pickle
from threading import Thread
from queue import Empty, Queue
from tw_game_engine import GameEngine as tw_ge
from concurrent.futures import ThreadPoolExecutor

tp = ThreadPoolExecutor(10)  # max 10 threads

def threaded(fn):
    def wrapper(*args, **kwargs):
        return tp.submit(fn, *args, **kwargs)  # returns Future object
    return wrapper

class TinyWorld:
    def __init__(self):
        self.byte_length = 4096

    @threaded
    def _threaded_client(self, conn):
        my_id = pickle.loads(conn.recv(self.byte_length))
        print('Player id:', my_id)
        player_data = {'new':my_id}
        self.to_engine.put(player_data)
        # send initial data to new connection
        starting_data = self.game_engine.send_object
        conn.send(pickle.dumps(starting_data))
        while True:
            try:
                keys = pickle.loads(conn.recv(self.byte_length))
                if not keys:
                    print('Connection closed')
                    break
                player_data = {'keys':(my_id, keys)}
                self.to_engine.put(player_data)
            except socket.error as e:
                print(e)
                break
            # send new game data to player connection
            data_to_send = self.game_engine.send_object
            conn.send(pickle.dumps(data_to_send))
        print("Lost connection")
        conn.close()

    @threaded
    def connection_to_engine(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.game_engine = tw_ge()
        while True:
            self.to_engine.join()
            task_list = []
            try:
                while True:
                    player_data = self.to_engine.get()
                    if player_data['new']:
                        self.game_engine.add_player(player_data['new'])
                    elif player_data['keys']:
                        self.game_engine.move_player(player_data['keys'])
            except Empty:
                pass
            self.game_engine.move_ai()
            self.game_engine.prepare_send_object()
            clock.tick(60)

    def main(self):
        # set up our queue
        self.to_engine = Queue()
        # start our game engine connection thread
        self.connection_to_engine, ()
        # local ip address
        server = ""
        port = 5555
        #set up our socket object 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((server, port))
        except socket.error as e:
            print(e)
        s.listen()
        print("Waiting for a connection, Server Started")        
        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)
            self.threaded_client, (con,)

if __name__ == '__main__':
    tiny_world = TinyWorld()
    tiny_world.main()