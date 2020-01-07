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
import psutil, pdb

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


pasteImg = None

class PastWindow(tk.Tk):

    def __init__(self, *args, **kw):
        super().__init__()
        self.configure(background='black')
        self.overrideredirect(True)
        self.width, self.height = 200, 100
        self.p_x, self.p_y = 100, 130
        self.isShow = True  # 是否隐藏
        self.wm_attributes("-alpha", 0.55)      # 透明度
        # self.wm_attributes("-toolwindow", True)  # 置为工具窗口
        self.wm_attributes("-topmost", True)  # 永远处于顶层
        self.bind('<B1-Motion>', self._on_move)
        self.bind('<ButtonPress-1>', self._on_tap)   # 设置窗口最大化大小
        self.bind('<Double-Button-1>', self.quit)
        self.bind('<Button-4>', self.zoom_up)
        self.bind('<Button-5>', self.zoom_down)
        self.resizable(width=False, height=True)    # 设置窗口宽度不可变，高度可变
        self.canvas = None
        
        # 缩放比例
        self.zoom, self.zoom = 1.0, 1.0
        # 
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tk.IntVar(value=0)
        self.Y = tk.IntVar(value=0)
        
        filename = 'all.gif'
        im = ImageGrab.grab()
        im = ImageEnhance.Brightness(im).enhance(0.8)
        im.save(filename)
        im.close()
        time.sleep(0.1)
        # 创建顶级组件容器
        self.top = tk.Toplevel(
            self, width=self.screenWidth, height=self.screenHeight)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)

        self.topcanvas = tk.Canvas(
            self.top,
            bg='white',
            width=self.screenWidth,
            height=self.screenHeight)

        # 绑定鼠标事件
        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            # pdb.set_trace()
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.sel = True
        self.topcanvas.bind('<Button-1>', onLeftButtonDown)

        # 鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            # pdb.set_trace()
            global lastDraw, r, c
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.topcanvas.delete(lastDraw)
                self.topcanvas.delete(r)
                self.topcanvas.delete(c)
            except Exception as e:
                pass
            # 没有点击左键时绘制十字线
            r = self.topcanvas.create_line(
                0, event.y, self.screenWidth, event.y, fill='white')
            c = self.topcanvas.create_line(
                event.x, 0, event.x, self.screenHeight, fill='white')
            if not self.sel:
                # print(event.x, event.y, self.screenWidth, self.screenHeight)
                pass
            else:
                lastDraw = self.topcanvas.create_rectangle(
                    self.X.get(),
                    self.Y.get(),
                    event.x, event.y,
                    outline='orange')
                # print(event.x, event.y, self.screenWidth, self.screenWidth)
        self.topcanvas.bind('<B1-Motion>', onLeftButtonMove)

        def onMouseMove(event):
            # 不点击时的鼠标移动，绘制十字线
            global r, c
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.topcanvas.delete(r)
                self.topcanvas.delete(c)
            except Exception as e:
                pass
            # 没有点击左键时绘制十字线
            r = self.topcanvas.create_line(
                0, event.y, self.screenWidth, event.y, fill='white')
            c = self.topcanvas.create_line(
                event.x, 0, event.x, self.screenHeight, fill='white')
        self.topcanvas.bind('<Motion>', onMouseMove)

        def onEscPressd( event):
            self.top.destroy()
        self.topcanvas.bind('<Cancel>', onEscPressd)

        # 获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            try:
                self.topcanvas.delete(lastDraw)
            except Exception as e:
                pass
            time.sleep(0.1)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            self.position = (left , top + 1, right, bottom)
            print(self.position)
            self.p_x, self.p_y = left + 2, top + 2
            self.width, self.height = right - left -1, bottom - top -1
            self.pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
            # 关闭顶级容器
            self.top.destroy()
            # 弹出保存截图对话框
            # fileName = tk.filedialog.asksaveasfilename(title='保存截图',
            #                           filetypes=[('image','*.jpg *.png')])
            if self.pic:
                self.pic.save("cut.gif")
        
        self.topcanvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.topcanvas.pack(fill=tk.BOTH, expand=tk.YES)


        # 显示全屏截图，在全屏截图上进行区域截图
        self.image = tk.PhotoImage(file=filename)
        self.topcanvas.create_image(
            self.screenWidth // 2, self.screenHeight // 2, image=self.image)
        self.topcanvas.pack()

        self.wait_window(self.top)


        
        
        self.run()


        self.geometry("%sx%s" % (self.width, self.height))
        self.geometry("+%s+%s" % (self.p_x, self.p_y))

        self.refresh_data()
        self.mainloop()

    def refresh_data(self):

        # self.canvas.delete("all")
        # 刷新
        self.update()
        self.after(1000, self.refresh_data)   # 这里的单位为毫秒

    def draw(self):
        # 初始化
        if(self.canvas):
            self.canvas['width'] = self.zoom_width
            self.canvas['height'] = self.zoom_height
        self.zoom_width = int(self.width * self.zoom)
        self.zoom_height = int(self.height  * self.zoom)
        self.canvas = tk.Canvas(self, width=self.zoom_width,
                                height=self.zoom_height, bg='white')
        self.img = ImageTk.PhotoImage(Image.open("./cut.gif").resize((self.zoom_width, self.zoom_height),Image.ANTIALIAS))
        self.canvas.create_image(self.zoom_width // 2, self.zoom_height // 2, image=self.img)
        self.canvas.place(x=-1, y=-1)

    def run(self):
        # 启动时运行
        # 开始截图
        self.draw()

    def quit(self, event):
        self.destroy()

    def switch_icon(self, _sysTrayIcon, icons='favicon.ico'):
        self.sysTrayIcon.icon = icons
        self.sysTrayIcon.refresh_icon()
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon

    def _on_move(self, event):
        # self.root_x/y  窗口左上角相对屏幕左上角的距离
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        abs_x = self.abs_x + offset_x
        abs_y = self.abs_y + offset_y

        # if self.width and self.height:
        #     geo_str = "%sx%s+%s+%s" % (self.width, self.height,
        #                                abs_x,
        #                                abs_y)
        # else:
        geo_str="+%s+%s" % (abs_x, abs_y)
        self.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y=event.x_root, event.y_root
        self.abs_x, self.abs_y=self.winfo_x(), self.winfo_y()

    def zoom_up(self, event):
        self.zoom += 0.1 
        self.draw()
        # self.run()
        self.geometry('%sx%s' % (int(self.width * self.zoom), int(self.height * self.zoom)))
    
    def zoom_down(self, event):
        self.zoom -= 0.1 
        self.draw()
        # self.run()
        self.geometry('%sx%s' % (int(self.width * self.zoom), int(self.height * self.zoom)))
    



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
    pastw=PastWindow()