import socket
import time

from camera import get_camera
from .wrapper import ImageWrapper


class ConnectionHandler(object):
    def __init__(self):
        self._clients = []
        self._camera = get_camera()

    def on_connected(self, client):
        addr = client[1]
        sc = client[0]
        sc.setblocking(False)
        self._clients.append(client)
        print('New Client Connected ip=[%s], port=[%d]' % (addr[0], addr[1]))

    def _remove_client(self, client):
        addr = client[1]
        print('Remove Client [%s]:[%d]' % (addr[0], addr[1]))
        self._clients.remove(client)

    def run(self):
        for client in self._clients:
            sc = client[0]
            addr = client[1]
            try:
                message = sc.recv(1024)
                print('Client [%s] readable [%s]!' % (addr, message))
                self._send_image(sc)
            except (ConnectionAbortedError, ConnectionResetError):
                self._remove_client(client)
            except BlockingIOError:
                pass
        time.sleep(0.2)

    def _send_image(self, client_socket):
        image_bytes = self._camera.capture()
        wrapper = ImageWrapper(image_bytes)
        wrapper.send_to(client_socket)


class SocketServer(object):
    def __init__(self, addr):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._init_socket(addr)

    def _init_socket(self, addr):
        self._socket.setblocking(False)
        self._socket.bind(addr)
        self._socket.listen(5)

    def start(self, handler):
        while True:
            try:
                client = self._socket.accept()
                handler.on_connected(client)
                print(client)
            except BlockingIOError:
                pass
            handler.run()
