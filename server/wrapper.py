from math import pow

FRAME_START = b'\xBF\xCC'
LENGTH_SIZE = 8


class ImageWrapper(object):
    def __init__(self, image_bytes):
        self._image_bytes = image_bytes

    def write_to(self, buffer):
        buffer.write(FRAME_START)
        length_bytes = self.get_length()
        print('length bytes ', length_bytes)
        buffer.write(length_bytes)
        buffer.write(self._image_bytes)

    def send_to(self, buffer):
        buffer.send(FRAME_START)
        buffer.send(self.get_length())
        buffer.send(self._image_bytes)

    def get_length(self) -> bytes:
        length = len(self._image_bytes)
        nums = []
        for weight in range(0, LENGTH_SIZE * 8, 8):
            base = pow(2, weight)
            one_byte = int(length / base % 256)
            nums.append(one_byte)
        nums.reverse()
        return bytes(nums)
