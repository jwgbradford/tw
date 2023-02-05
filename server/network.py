from json import dumps, loads
from socket import socket, error, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from settings import ADDR, BUFSIZ

class Network:
    def __init__(self) -> None:
        self.Connection = socket(AF_INET, SOCK_STREAM)
        self.Connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.Connection.bind(ADDR)

    def send_data(self, player_conn, data) -> None:
        json_data = dumps(data)
        try:
            player_conn.send(json_data.encode())
        except error as e:
            print(e)

    def get_data(self, player_conn):
        try:
            return loads(player_conn.recv(BUFSIZ))
        except error as e:
            print(e)
            return e