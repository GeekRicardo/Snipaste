# -*- coding: utf-8 -*-

import pdb
# pdb.set_trace()

import tkinter as tk
from tkinter.messagebox import *
import psutil
import os
import atexit
import threading
import time
import sys
import psutil

from PIL import Image, ImageTk, ImageEnhance

import platform
osName = platform.system()
tail = ''   #换行尾部符
if(osName == 'Windows'):
    tail = '\r\n'
    from PIL import ImageGrab
elif(osName == 'Linux'):
    tail = '\n'
    import pyscreenshot as ImageGrab
elif(osName == 'Darwin'):
    pass



# from pasw import PastWindow as pw
# from capture import Capture



class PastWindow(tk.Tk):

    def __init__(self,  *args, **kw):

        super().__init__()
        self.configure(background='black')

        self.overrideredirect(True)
        self.screen_width = super().winfo_screenwidth()
        self.screen_height = super().winfo_screenheight()
        
        self.isShow = True  # 是否隐藏
        self.contentType = 'img'	# 默认为图片
        self.zoom = 1   # 图片缩放大小
        # self.wm_attributes("-alpha", 0.55)      # 透明度
        # self.wm_attributes("-toolwindow", True)  # 置为工具窗口
        # 
        
        self.width, self.height = 600, 200
        self.p_x, self.p_y = 100, 100


        self.wm_attributes("-topmost", True)  # 永远处于顶层
        self.bind('<B1-Motion>', self._on_move)
        self.bind('<ButtonPress-1>', self._on_tap)   # 设置窗口最大化大小
        self.bind('<Double-Button-1>', self.quit)
        self.bind("<MouseWheel>", self.processWheel)
        self.resizable(width=False, height=True)    # 设置窗口宽度不可变，高度可变
        # self.label = tk.Label(self, width=100, height=60)
        self.canvas = tk.Canvas(self, width=self.width,
                                height=self.height, bg='white')
        self.canvas.place(x=-2, y=-1)
        
        self.run()
        
        # self.img.pack()

        self.geometry("%sx%s" % (self.width, self.height))
        self.geometry("+%s+%s" % (self.p_x, self.p_y))

        # q_tk.put(self)

        # self.run()
        self.refresh_data()
        self.mainloop()

    def refresh_data(self):        
        # 刷新
        self.update()
        self.after(100, self.refresh_data)   # 这里的单位为毫秒

    def run(self):
        # 启动时运行
        # self.w = Capture(self)
        # self.wait_window(self.w.top)

        tkimg = tk.PhotoImage(file="./cut.gif")
        self.img = self.canvas.create_image(self.width / 2 + 1, self.height / 2 + 1, image=tkimg)
        
        # self.img = self.canvas.create_image(0, 0, image=tk.PhotoImage(file='./cut.gif'))

    def quit(self, event):
        self.destroy()

    def _on_move(self, event):
        # self.root_x/y  窗口左上角相对屏幕左上角的距离
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y
        print(event.x_root, event.y_root, event.x, event.y)
        # pdb.set_trace()
        print(self.abs_x, self.abs_y)
        abs_x = self.abs_x + offset_x
        abs_y = self.abs_y + offset_y

        if self.width and self.height:
            geo_str = "%sx%s+%s+%s" % (self.width, self.height,
                                       abs_x,
                                       abs_y)
        else:
            geo_str="+%s+%s" % (abs_x, abs_y)
        self.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y=event.x_root, event.y_root
        self.abs_x, self.abs_y=self.winfo_x(), self.winfo_y()

    def processWheel(self, event):
        if event.delta > 0:
            # 滚轮往上滚动，放大
            pass
        else:
            # 滚轮往下滚动，缩小
            pass


# root = tk.Tk()
# # 指定窗口的大小
# root.geometry('200x60+500+400')
# # 不允许改变窗口大小
# root.resizable(False, False)
# root.title("OCR")

# def b():
#     p = PastWindow()

# def key(event):
#     p = PastWindow()
# root.bind('<Control-Alt-f>', key)

# def quit(event):
#     exit(0)
# root.bind('<Double-Button-1>', quit)

# buttonCapture = tk.Button(root, text='截图', command=b)
# buttonCapture.place(x=60, y=15, width=80, height=30)
# # 启动消息主循环
# try:
#     root.mainloop()
# except Exception as e:
#     root.destroy()
#     

# w= Capture()

p = PastWindow()



