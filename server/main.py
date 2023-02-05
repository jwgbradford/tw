import pygame
from time import sleep
from threading import Thread
from network import Network
from settings import GAME_SPEED

class TinyWorld:
    def __init__(self) -> None:
        self.clients = [] # empty dictionary for client list
        # set up our server socket
        self.network = Network()
        self.network.Connection.listen(5) # limit to 5 concurrent players
        print("Waiting for a connection, Server Started")

    # our threaded function to accept new players
    def accept_new_players(self):
        while True:
            player, player_addr = self.network.Connection.accept()
            # start each player handler Thread
            Thread(target=self.handle_player, args=(player,)).start()

    # each player has a handler thread
    def handle_player(self, player_conn):
        receive_msg_id = 1
        send_msg_id = 0
        while True:
            # our main loop 
            try:
                new_data = self.network.get_data(player_conn)
            except:
                print('Connection lost')
                break
            if receive_msg_id == 1:
                my_id  = str(list(new_data.keys())[0])
                # add new connection to clients
                self.clients.append(my_id)
            elif new_data[my_id]['msg_id'] == receive_msg_id:
                print('correpted connection')
                break
            else:
                print('data received', new_data)
                receive_msg_id = new_data[my_id]['msg_id']
            try: # to load the data to send from the output buffer
                my_data = {my_id : self.output_buffer[my_id]}
            except: # if it doesn't exist, make up some dummy data
                my_data = {my_id : {'send_msg_id' : 1, 'send_data' : 'pending'}}
            print(my_data, send_msg_id)
            while send_msg_id == my_data[my_id]['send_msg_id']:
                try:
                    my_data = {my_id : self.output_buffer[my_id]}
                    sleep(0.1) # nasty horrible code, but think of better way right now
                except: # keep checking until the server updates the output buffer
                    my_data = {my_id : {'send_msg_id' : 1, 'send_data' : 'pending'}}
            print('send', my_data)
            self.network.send_data(player_conn, my_data)
            send_msg_id = my_data[my_id]['send_msg_id']
        player_conn.close()
        del self.clients[my_id]

    # threaded code to run the game
    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        msg_id = 1
        self.output_buffer = {}
        while True:
            self.output_buffer = {} # clear output buffer each cycle
            for player_id in self.clients:
                # build output data for each player
                self.output_buffer[player_id] = {}
                self.output_buffer[player_id]['send_msg_id'] = msg_id
                '''
                player_conn = self.clients[player_id]
                self.network.send_data(player_conn, data_to_send)
                '''
            print(self.output_buffer)
            msg_id += 1
            clock.tick(GAME_SPEED)

    # main simply launches the run_game Thread, and accept_new_players Thread
    def main(self):
        Thread(target=self.run_game).start()
        ACCEPT_THREAD = Thread(target=self.accept_new_players)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.network.close()

if __name__ == '__main__':
    tiny_world = TinyWorld()
    tiny_world.main()