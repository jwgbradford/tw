from json import dumps, loads
from socket import socket, error, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from settings import ADDR, BUFSIZ

class Network:
    def __init__(self) -> None:
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.SERVER.bind(ADDR)

    def send_data(self, data) -> None:
        json_data = dumps(data)
        try:
            self.SERVER.send(json_data.encode())
        except error as e:
            print(e)

    def get_data(self):
        try:
            return loads(self.SERVER.recv(BUFSIZ))
        except error as e:
            print(e)
            return e