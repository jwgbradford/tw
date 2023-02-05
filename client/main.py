from random import randint
from network import Network
from threading import Thread

class MyGame:
    def __init__(self) -> None:
        self.send_data = {}
        self.receive_data = {}


    # our threaded function to accept new players
    def talk_to_server(self, my_id):
        n = Network()
        msg_id = 1
        self.send_data[my_id] = {}
        while True:
            self.send_data[my_id]['msg_id'] = msg_id
            #print('sent ',self.send_data)
            n.send(self.send_data)
            self.receive_data = n.receive()
            #print('received ',self.receive_data)
            msg_id += 1

    def main(self):
        run = True
        self.send_data = {}
        # we don't bother will full user identification / verification just yet
        my_id = str(randint(0, 64000))
        Thread(target=self.talk_to_server, args=(my_id,)).start()
        while run:
            self.send_data[my_id]["send"] = input('data to send')


if __name__ == '__main__':
    my_game = MyGame()
    my_game.main()