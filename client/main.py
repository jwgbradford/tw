from random import randint
from network import Network

class MyGame:
    def __init__(self) -> None:
        pass

    def main(self):
        run = True
        send_data = {}
        my_id = str(randint(0, 64000))
        send_data[my_id] = {}
        n = Network()
        while run:
            send_data[my_id]["send"] = input('data to send')
            print(send_data)
            n.send(send_data)
            receive_data = n.receive()
            print(receive_data)

if __name__ == '__main__':
    my_game = MyGame()
    my_game.main()