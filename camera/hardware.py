import os
from io import BytesIO


class MockPiCamera(object):
    def capture(self, *args, **kwargs):
        return b''

    def capture_continuous(self, *args, **kwargs):
        yield b''


try:
    from picamera import PiCamera
except ImportError:
    PiCamera = MockPiCamera


def is_raspberry_pi():
    return PiCamera != MockPiCamera


class Camera(object):
    def __init__(self):
        self._buffer = BytesIO()

    def close(self):
        self._buffer.close()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class MockCamera(Camera):
    def __init__(self, mock_file_dir):
        super().__init__()
        file_list = os.listdir(mock_file_dir)
        self._mock_files = [os.path.join(mock_file_dir, file) for file in file_list]
        self._mock_file_index = 0

    def capture(self):
        file = self._mock_files[self._mock_file_index]
        self._mock_file_index += 1
        self._mock_file_index %= len(self._mock_files)
        self._buffer.seek(0)
        with open(file, 'rb') as output_file:
            file_content = output_file.read()
            self._buffer.write(file_content)
        return self._buffer.getvalue()


class RaspiCamera(Camera):
    def __init__(self):
        super().__init__()
        self._camera = self._init_camera()
        self._capture_generator = self._camera.capture_continuous(self._buffer, format='jpeg')

    @staticmethod
    def _init_camera():
        return PiCamera()

    def capture(self):
        self._buffer.seek(0)
        self._capture_generator.__next__()
        return self._buffer.getvalue()


def get_camera():
    if is_raspberry_pi():
        return RaspiCamera()
    else:
        return MockCamera('D:\\dev\python\\network_pi_camera\\img')
