import socket, json, pygame
from _thread import start_new_thread
from tw_game_engine import GameEngine as tw_ge

class TinyWorld:
    def __init__(self):
        self.game_engine = tw_ge()
        server = "192.168.0.92"
        port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((server, port))
        except socket.error as e:
            print(e)
        self.s.listen()
        print("Waiting for a connection, Server Started")

    def main(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            start_new_thread(self.threaded_client, (conn,))

    def threaded_client(self, conn):
        pygame.init()
        clock = pygame.time.Clock()

        # get player id from new connection
        my_id = json.loads(conn.recv(2048))
        print('Player id:', my_id)
        self.game_engine.add_player(my_id)

        # send initial data to new connection
        starting_data = self.game_engine.update_objects()
        json_data = json.dumps(starting_data)
        conn.send(json_data.encode())

        while True:
            try:
                keys = json.loads(conn.recv(2048))
                print(keys)
                self.game_engine.move_player(my_id, keys)
                self.game_engine.move_ai()

                # send new game data to player connection
                data = self.game_engine.update_objects()
                json_data = json.dumps(data)
                conn.send(json_data.encode())
            except socket.error as e:
                print(e)
                break
            clock.tick(60)

        print("Lost connection")
        conn.close()

if __name__ == '__main__':
    tiny_world = TinyWorld()
    tiny_world.main()