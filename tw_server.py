import socket, json, pygame, threading
from _thread import start_new_thread
from tw_game_engine import GameEngine as tw_ge

class TinyWorld:
    def __init__(self):
        self.game_engine = tw_ge()
        self.ns = threading.local() # namespace for thread local data

    def threaded_client(self, conn):
        pygame.init()
        self.ns.clock = pygame.time.Clock()

        # get player id from new connection
        self.ns.my_id = json.loads(conn.recv(2048))
        print('Player id:', self.ns.my_id)
        self.game_engine.add_player(self.ns.my_id)

        # send initial data to new connection
        self.ns.starting_data = self.game_engine.update_objects()
        self.ns.json_data = json.dumps(self.ns.starting_data)
        conn.send(self.ns.json_data.encode())
        self.print_lock.release()

        while True:
            self.print_lock.acquire()

            try:
                self.ns.data = conn.recv(2048)
                keys = {}
                if len(self.ns.data) > 0:
                    keys = json.loads(self.ns.data)
                if not keys:
                    True # print('Connection closed')
                else:
                    self.game_engine.move_player(self.ns.my_id, keys)
                    self.game_engine.move_ai()

                    # send new game data to player connection
                    self.ns.data = self.game_engine.update_objects()
                    self.ns.json_data = json.dumps(self.ns.data)
                    conn.send(self.ns.json_data.encode())
            except socket.error as e:
                print(e)
                break
            self.print_lock.release()
            self.ns.clock.tick(60)
        self.print_lock.release()
        print("Lost connection")
        conn.close()

    def main(self):
        # local ip address
        server = "localhost"
        port = 5555
        # set up threading lock
        self.print_lock = threading.Lock()
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
            # lock acquired by client
            self.print_lock.acquire()
            print("Connected to:", addr)
            start_new_thread(self.threaded_client, (conn,))
        s.close()

if __name__ == '__main__':
    tiny_world = TinyWorld()
    tiny_world.main()