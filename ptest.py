# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter.messagebox import *
import psutil
import os
import atexit
import threading
import time
import sys
import psutil

from PIL import Image, ImageTk

from pasw import PastWindow as pw


tkimg = None

class PastWindow(tk.Tk):

    def __init__(self,  *args, **kw):
        super().__init__()
        self.configure(background='black')
        self.overrideredirect(True)
        position = (552, 491, 1238, 643)
        self.width, self.height = position[2] - position[0], position[3] - position[1]
        self.p_x, self.p_y = position[0], position[1]
        self.isShow = True  # 是否隐藏
        self.contentType = 'img'	# 默认为图片
        # self.wm_attributes("-alpha", 0.55)      # 透明度
        # self.wm_attributes("-toolwindow", True)  # 置为工具窗口
        self.wm_attributes("-topmost", True)  # 永远处于顶层
        self.bind('<B1-Motion>', self._on_move)
        self.bind('<ButtonPress-1>', self._on_tap)   # 设置窗口最大化大小
        self.bind('<Double-Button-1>', self.quit)
        self.resizable(width=False, height=True)    # 设置窗口宽度不可变，高度可变
        # self.label = tk.Label(self, width=100, height=60)
        self.canvas = tk.Canvas(self, width=self.width,
                                height=self.height, bg='white')
        self.canvas.place(x=-2, y=-1)
        
        
        # self.img.pack()

        self.geometry("%sx%s" % (self.width, self.height))
        self.geometry("+%s+%s" % (self.p_x, self.p_y))

        # q_tk.put(self)

        self.run()
        self.refresh_data()
        self.mainloop()

    def refresh_data(self):        
        # 刷新
        self.update()
        self.after(100, self.refresh_data)   # 这里的单位为毫秒

    def run(self):
        # 启动时运行
        self.canvas.create_line(
            0, 35, self.width, 35, fill='#bfbfbf')
        print(self.width, self.height)
        global tkimg
        tkimg = ImageTk.PhotoImage(Image.open("./cut.gif"))
        self.img = self.canvas.create_image(self.width / 2 + 1, self.height / 2 + 1, image=tkimg)
        # self.img = self.canvas.create_image(0, 0, image=tk.PhotoImage(file='./cut.gif'))

    def quit(self, event):
        self.destroy()

    def _on_move(self, event):
        # self.root_x/y  窗口左上角相对屏幕左上角的距离
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        abs_x = self.abs_x + offset_x
        abs_y = self.abs_y + offset_y

        # 超出屏幕不能移出去
        # if(abs_x >= 1920 - self.width):
        #     abs_x = 1920 - self.width
        # if(abs_x <= 0):
        #     # abs_x = 0
        #     pass
        # if(abs_y <= 0):
        #     abs_y = 0
        # if(abs_y >= self.winfo_screenwidth):
        #     abs_y = self.winfo_screenwidth

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

p = pw()