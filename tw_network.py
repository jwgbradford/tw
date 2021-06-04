import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.81"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.byte_length = 2048

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return pickle.loads(self.client.recv(self.byte_length))
        except socket.error as e:
            print(e)
            return e