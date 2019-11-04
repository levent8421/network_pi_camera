from io import BytesIO

STATE_FRAME_START = 0x00
STATE_FRAME_LENGTH = 0x01
STATE_FRAME_DATA = 0x02

FRAME_START_SIZE = 2
FRAME_LENGTH_SIZE = 8

FRAME_START = [0xBF, 0xCC]


class UnWrapper(object):
    def __init__(self, cb):
        self._cb = cb
        self._state = STATE_FRAME_START
        self._frame_start_offset = 0
        self._frame_length_offset = 0
        self._frame_data_offset = 0
        self._buffer = BytesIO()
        self._frame_start = []
        self._frame_length = []
        self._package_length = 0

    def write(self, data):
        if data:
            for b in data:
                self._resolve_byte(b)

    def _resolve_byte(self, b):
        if self._state == STATE_FRAME_START:
            self._frame_start_offset += 1
            self._frame_start.append(b)
            if self._frame_start_offset >= FRAME_START_SIZE:
                self._frame_start_offset = 0
                self._state = STATE_FRAME_LENGTH
                self._check_frame_start()
        elif self._state == STATE_FRAME_LENGTH:
            self._frame_length.append(b)
            self._frame_length_offset += 1
            if self._frame_length_offset >= FRAME_LENGTH_SIZE:
                self._resolve_frame_length()
        elif self._state == STATE_FRAME_DATA:
            self._frame_data_offset += 1
            self._buffer.write(bytearray([b]))
            if self._frame_data_offset >= self._package_length:
                self._on_package_end()

    def _resolve_frame_length(self):
        self._state = STATE_FRAME_DATA
        self._frame_length_offset = 0
        length = 0
        for b in self._frame_length:
            length += b
            length *= 256
        length /= 256
        self._package_length = length
        print('package length%s=>[%d]' % (self._frame_length, length))
        self._frame_length = []

    def _on_package_end(self):
        self._state = STATE_FRAME_START
        self._frame_data_offset = 0
        data = self._buffer.getvalue()
        self._cb(data)
        self._buffer.seek(0)

    def _check_frame_start(self):
        if not self._frame_start == FRAME_START:
            print('Invalidate Frame Start [%s]', self._frame_start)
            self._state = STATE_FRAME_START
        self._frame_start = []
