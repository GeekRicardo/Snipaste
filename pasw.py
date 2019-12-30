# -*- coding: utf-8 -*-
# @Author: Ricardo
# @Date:   2019-11-03 16:48:28
# @Last Modified by:   Ricardo
# @Last Modified time: 2019-11-15 21:27:03


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

pasteImg = None

class PastWindow(tk.Tk):

    def __init__(self, capture, png, *args, **kw):
        super().__init__()
        self.configure(background='black')
        self.imgPath = capture.src
        self.overrideredirect(True)
        self.capture = capture
        self.width, self.height = self.capture.width, self.capture.height
        self.p_x, self.p_y = self.capture.position[0], self.capture.position[1]
        self.isShow = True  # 是否隐藏
        self.contentType = 'img'	# 默认为图片
        # self.wm_attributes("-alpha", 0.55)      # 透明度
        # self.wm_attributes("-toolwindow", True)  # 置为工具窗口
        self.wm_attributes("-topmost", True)  # 永远处于顶层
        self.bind('<B1-Motion>', self._on_move)
        self.bind('<ButtonPress-1>', self._on_tap)   # 设置窗口最大化大小
        self.bind('<Double-Button-1>', self.quit)
        self.resizable(width=False, height=True)    # 设置窗口宽度不可变，高度可变
        # self.top = tk.Toplevel(self, width=self.width, height=self.height)
        # self.top.overrideredirect(True)
        self.canvas = tk.Canvas(self, width=self.width,
                                height=self.height, bg='white')
        # self.canvas.place(x=-1, y=-1)
        self.im = tk.PhotoImage(file=png)
        self.img = self.canvas.create_image(self.p_x // 2, self.p_y // 2, image=self.im)
        self.canvas.pack()

        self.geometry("%sx%s" % (self.width, self.height))
        self.geometry("+%s+%s" % (self.p_x, self.p_y))


        self.run()
        self.refresh_data()
        self.mainloop()

    def refresh_data(self):
        
        # self.wm_attributes("-topmost", True)  # 永远处于顶层

        # self.canvas.delete("all")
        # # 分割线
        # self.canvas.create_line(
        #     0, 20, self.width, 20, fill='#bfbfbf')
        # self.canvas.create_line(
        #     0, 35, self.width, 35, fill='#bfbfbf')
        # self.canvas.create_line(
        #     0, 50, self.width, 50, fill='#bfbfbf')
        # self.canvas.create_line(
        #     self.width / 2, 50, self.width / 2, self.height, fill='#bfbfbf')
        # 刷新
        self.update()
        self.after(100, self.refresh_data)   # 这里的单位为毫秒

    def run(self):
        # 启动时运行
        # global pasteImg
        # pasteImg = ImageTk.PhotoImage(file=self.capture.pic)
        # self.img = self.canvas.create_image(self.width / 2 + 1, self.height / 2 + 1, image=pasteImg)
        pass

    def quit(self, event):
        self.destroy()
        # 窗口隐藏
        # self.withdraw()
        # 窗口显示
        # self.deiconify()
        # self.sysTrayIcon.show_icon()

    def _on_move(self, event):
        # self.root_x/y  窗口左上角相对屏幕左上角的距离
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        abs_x = self.abs_x + offset_x
        abs_y = self.abs_y + offset_y

        # # 超出屏幕不能移出去
        # if(abs_x >= 1920 - self.width):
        #     abs_x = 1920 - self.width
        # if(abs_x <= 0):
        #     # abs_x = 0
        #     pass
        # if(abs_y <= 0):
        #     abs_y = 0
        # if(abs_y >= self.p_y):
        #     abs_y = self.p_y

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




lock = './lock.lock'
isrun = False


@atexit.register
def exit():
    # q_tk.queue.clear()
    # global wintemp
    # del(wintemp)
    if((not isrun) and os.path.exists(lock)):
        os.remove(lock)


if __name__ == '__main__':
    pid=0
    if(os.path.exists(lock)):
        with open(lock, 'r', encoding = 'utf-8') as f:
            pid=int(f.read())
        if(psutil.pid_exists(pid)):
            print('已有实例运行')
            isrun=True
            m=tk.Tk()
            m.withdraw()
            tk.messagebox.showerror('错误', '已有实例在运行')
            m.destroy()
            sys.exit(0)
        else:
            print('运行实例失效')
    else:
        # print('未在运行')
        pass
    pid=os.getpid()
    with open(lock, 'w', encoding = 'utf-8') as f:
        f.write(str(pid))
    pastw=PastWindow((10,10, 40, 40), '')