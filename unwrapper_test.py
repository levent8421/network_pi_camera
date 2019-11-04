from io import BytesIO

from client.unwrapper import UnWrapper
from server.wrapper import ImageWrapper


def cb(data):
    print(data)


def main():
    with BytesIO() as buffer:
        wrapper = ImageWrapper(b'1234567890')
        wrapper.write_to(buffer)
        data = buffer.getvalue()
        print('wrap result ', data)
        unwrapper = UnWrapper(cb)
        unwrapper.write(data)


if __name__ == '__main__':
    main()
