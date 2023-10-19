import socket
import selectors
import time

from config import HOST, PORT


selector = selectors.DefaultSelector()


def init_server():
    server_socket = socket.create_server((HOST, PORT))
    server_socket.listen()
    selector.register(server_socket, selectors.EVENT_READ, accept_connection)


def accept_connection(server_socket):
    client_socket, _ = server_socket.accept()
    selector.register(client_socket, selectors.EVENT_READ, recv_data)


def recv_data(client_socket):
    ext = client_socket.recv(1024)
    with open(f'{time.time()}{ext.decode()}', "wb") as f:
        while True:
            buff = client_socket.recv(4096)
            if buff:
                f.write(buff)
            else:
                break
    selector.unregister(client_socket)
    client_socket.close()


def server_run():
    init_server()
    while True:
        events = selector.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server_run()
