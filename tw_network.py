import socket
import json

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
            json_data = json.dumps(data)
            self.client.send(json_data.encode())
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return json.loads(self.client.recv(self.byte_length))
        except socket.error as e:
            print(e)
            return e                  
