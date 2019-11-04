from server.socket_server import SocketServer, ConnectionHandler


def main():
    server_addr = ('0.0.0.0', 8088)
    server = SocketServer(server_addr)
    handler = ConnectionHandler()
    print('Starting %s success %s' % (server, server_addr))
    server.start(handler)


if __name__ == '__main__':
    main()
