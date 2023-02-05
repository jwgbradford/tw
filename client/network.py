from json import dumps, loads
from socket import socket, error, AF_INET, SOCK_STREAM
from settings import ADDR, BUFSIZ

class Network:
    def __init__(self) -> None:
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect(ADDR)

    def send(self, data) -> None:
        json_data = dumps(data)
        try:
            self.client.send(json_data.encode())
        except error as e:
            print(e)

    def receive(self):
        try:
            return loads(self.client.recv(BUFSIZ))
        except error as e:
            print(e)
            return e 