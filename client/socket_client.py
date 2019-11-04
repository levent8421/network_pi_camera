import socket
import time
from io import BytesIO

FETCH_COMMAND = b'<?capture'


class SocketClient(object):
    def __init__(self, addr):
        self._server = addr
        self._socket = self._init_socket()
        self._buffer = BytesIO()

    def _init_socket(self):
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect(self._server)
        sc.setblocking(False)
        return sc

    def send_fetch_command(self):
        self._socket.send(FETCH_COMMAND)

    def recv_if_available(self, unwrapper):
        try:
            while True:
                data = self._socket.recv(1024)
                unwrapper.write(data)
        except BlockingIOError:
            pass
        time.sleep(0.2)

    def close(self):
        self._socket.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self
