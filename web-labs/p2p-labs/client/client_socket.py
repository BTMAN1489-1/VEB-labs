import socket
import os


class ClientSocket:
    _connection = None

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create_connection(self):
        self._connection = socket.create_connection((self.host, self.port))

    def send_file(self, path: str):
        _, ext = os.path.splitext(path)
        with open(path, "rb") as f:
            self._connection.send(ext.encode())
            self._connection.sendfile(f)