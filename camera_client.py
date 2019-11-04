from io import BytesIO

import matplotlib.pyplot as plt

from client.socket_client import SocketClient
from client.unwrapper import UnWrapper

client = None


def cb(data):
    plt.imshow(plt.imread(BytesIO(data), format='jpeg'))
    plt.show()
    client.send_fetch_command()


unwrapper = UnWrapper(cb)


def main():
    addr = ('localhost', 8088)
    global client
    with SocketClient(addr) as client:
        client.send_fetch_command()
        while True:
            client.recv_if_available(unwrapper)


if __name__ == '__main__':
    main()
