import tkinter
from _thread import start_new_thread
from io import BytesIO

from PIL import Image, ImageTk

from client.socket_client import SocketClient
from client.unwrapper import UnWrapper


def handler_new_image(application):
    def handler(data):
        application.set_image(data)

    return handler


class Application(tkinter.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._init_master()
        self._client = self._init_client()
        self._init_widgets()

    def _init_client(self):
        self._unwrapper = UnWrapper(handler_new_image(self))
        return SocketClient(('192.168.2.105', 8088))

    def _init_widgets(self):
        self._init_master()
        self._label = tkinter.Label(self.master)
        # self._label.pack()

    def _init_master(self):
        master = self.master
        master.title('Raspberry Pi Remote Camera')

    def set_image(self, data):
        buffer = BytesIO(data)
        image = Image.open(buffer)
        bm = ImageTk.PhotoImage(image)
        self._label.destroy()
        self._label = tkinter.Label(self.master, image=bm)
        self._label.pack()
        self._client.send_fetch_command()

    def start_recv(self):
        self._client.send_fetch_command()
        while True:
            self._client.recv_if_available(self._unwrapper)


if __name__ == '__main__':
    app = Application()
    start_new_thread(lambda: app.start_recv(), ())
    app.mainloop()
