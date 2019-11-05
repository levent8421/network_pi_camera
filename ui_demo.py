from io import BytesIO
from tkinter import Frame, PhotoImage, Label, Button

from PIL import Image, ImageTk


class Application(Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.pack()
        self._init_widgets()

    def _init_widgets(self):
        self._init_master()
        # 创建Label对象，第一个参数指定该Label放入root
        w = Label(self)
        # 创建一个位图
        with open('E:/private/python/network_pi_camera/img/1.png', 'rb') as f:
            bts = f.read()
            buffer = BytesIO(bts)
            image = Image.open(buffer)
            bm = ImageTk.PhotoImage(image)
        # 必须用一个不会被释放的变量引用该图片，否则该图片会被回收
        w.x = bm
        # 设置显示的图片是bm
        w['image'] = bm
        w.pack()
        # 创建Button对象，第一个参数指定该Button放入root
        btn = Button(self, text="确定")
        btn['background'] = 'yellow'
        btn.configure(background='yellow')
        btn.pack()

    def _init_master(self):
        master = self.master
        master.title('Raspberry Pi Remote Camera')
        master.geometry('500x500')


if __name__ == '__main__':
    app = Application()
    print(app)
    app.mainloop()
