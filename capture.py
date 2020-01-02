import tkinter as tk
import tkinter.filedialog
import os
# import pdb
import time
from aip import AipOcr
from PIL import ImageEnhance
client = AipOcr('10684055', 'Y15dcjjkq2dLHB1NmdCN9ODI',
                'keOYEXKG1RXnLyGLa4wfCr003kKE1zhh')
import platform
osName = platform.system()
tail = ''   #换行尾部符
if(osName == 'Windows'):
    tail = '\r\n'
    from PIL import ImageGrab
    # 设置任务栏图标
    import ctypes
    myappid = 'Ricardo.Capture2Text.subproduct.V1.02'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
elif(osName == 'Linux'):
    tail = '\n'
    import pyscreenshot as ImageGrab
elif(osName == 'Darwin'):
    pass


from queue import Queue

from PIL import Image, ImageTk
# from pasw import PastWindow

root = tk.Tk()
# 指定窗口的大小
root.geometry('200x60+500+400')
# 不允许改变窗口大小
root.resizable(False, False)
root.title("OCR")
# root.overrideredirect(True)
# root.iconbitmap('./icon.ico')
# root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage('icon.ico'))
resultboxes = []  # 前面识别的结果窗口


class PastWindow(tk.Tk):

    def __init__(self, capture, png, *args, **kw):
        super().__init__()
        self.configure(background='black')
        # self.imgPath = capture.src
        self.overrideredirect(True)
        self.capture = capture
        self.width, self.height = self.capture.width, self.capture.height
        self.p_x, self.p_y = self.capture.position[0], self.capture.position[1]
        self.isShow = True  # 是否隐藏
        self.contentType = 'img'    # 默认为图片
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
        # self.im = tk.PhotoImage(file=png)
        # pdb.set_trace()
        img = Image.open("./cut.gif")
        self.im = ImageTk.PhotoImage(img)
        self.img = self.canvas.create_image(self.p_x // 2, self.p_y // 2, image=self.im)
        # self.img.image=self.im
        self.canvas.pack()

        self.geometry("%sx%s" % (self.width, self.height))
        self.geometry("+%s+%s" % (self.p_x, self.p_y))


        self.run()
        self.refresh_data()
        self.mainloop()

    def refresh_data(self):
        # self.canvas.delete("all")
        # # 分割线
        # 刷新
        self.update()
        self.after(100, self.refresh_data)   # 这里的单位为毫秒

    def run(self):
        # 启动时运行
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


class Capture:

    def __init__(self, png):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tk.IntVar(value=0)
        self.Y = tk.IntVar(value=0)
        self.sel = False
        # 屏幕尺寸
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()
        # 创建顶级组件容器
        self.top = tk.Toplevel(
            root, width=self.screenWidth, height=self.screenHeight)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.sniptop = None
        self.canvas = tk.Canvas(
            self.top,
            bg='white',
            width=self.screenWidth,
            height=self.screenHeight)
        # 显示全屏截图，在全屏截图上进行区域截图
        self.image = tk.PhotoImage(file=png)
        self.canvas.create_image(
            self.screenWidth // 2, self.screenHeight // 2, image=self.image)
        self.canvas.pack()
        self.sni_list = []

        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            # pdb.set_trace()
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        # 鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            # pdb.set_trace()
            global lastDraw, r, c
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass
            # 没有点击左键时绘制十字线
            r = self.canvas.create_line(
                0, event.y, self.screenWidth, event.y, fill='white')
            c = self.canvas.create_line(
                event.x, 0, event.x, self.screenHeight, fill='white')
            if not self.sel:
                # print(event.x, event.y, self.screenWidth, self.screenHeight)
                pass
            else:
                lastDraw = self.canvas.create_rectangle(
                    self.X.get(),
                    self.Y.get(),
                    event.x, event.y,
                    outline='orange')
                # print(event.x, event.y, self.screenWidth, self.screenWidth)
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        def onMouseMove(event):
            # 不点击时的鼠标移动，绘制十字线
            global r, c
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass
            # 没有点击左键时绘制十字线
            r = self.canvas.create_line(
                0, event.y, self.screenWidth, event.y, fill='white')
            c = self.canvas.create_line(
                event.x, 0, event.x, self.screenHeight, fill='white')
        self.canvas.bind('<Motion>', onMouseMove)

        def onEscPressd( event):
            self.top.destroy()
        self.canvas.bind('<Cancel>', onEscPressd)

        # 获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp( event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            time.sleep(0.1)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            self.position = (left , top + 1, right, bottom)
            print(self.position)
            self.width , self.height = right - left, bottom - top
            self.pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
            # 关闭顶级容器
            self.top.destroy()
            # 弹出保存截图对话框
            # fileName = tk.filedialog.asksaveasfilename(title='保存截图',
            #                           filetypes=[('image','*.jpg *.png')])
            if self.pic:
                # global sni_list
                # src = './cut' + str(len(sni_list) + 1) + '.gif'
                # sni_list.append(src)
                self.pic.save("cut.gif")
                # PastWindow(self, "cut.gif")
                # 关闭当前窗口
                # self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    # def paste(self, png):
    #     snip = tk.Toplevel(root, width=self.width, height=self.height)
    #     snip.overrideredirect(True)
    #     self.sni_list.append(snip)
    #     geo = "%sx%s+%s+%s"%(self.position[0], self.position[1], self.width, self.height)
    #     snip.geometry(geo)
    #     canvas = tk.Canvas(
    #         snip,
    #         bg='white',
    #         width=self.width,
    #         height=self.height)
    #     im = tk.PhotoImage(file=png)
    #     canvas.create_image(self.width //2, self.height//2, image=im)
    #     canvas.pack()

    #     def _on_move(event):
    #         # self.root_x/y  窗口左上角相对屏幕左上角的距离
    #         offset_x = event.x_root - root.root_x
    #         offset_y = event.y_root - root.root_y

    #         # if self.width and self.height:
    #         #     geo_str = "%sx%s+%s+%s" % (self.width, self.height,
    #         #                                abs_x,
    #         #                                abs_y)
    #         # else:
    #         geo_str="+%s+%s" % (offset_x, offset_y)
    #         snip.geometry(geo_str)
    #     snip.bind('<B1-Motion>', _on_move)

    #     def quit(event):
    #         snip.destroy()
    #     snip.bind('<Double-Button-1>', quit)





# 开始截图
sni_list = []

def buttonCaptureClick():
    global sni_list
    # 最小化主窗口
    root.state('icon')
    for box in resultboxes:
        try:
            box.state('icon')
        except Exception as e:
            pass
    time.sleep(0.2)
    filename = 'all.gif'
    im = ImageGrab.grab()
    im = ImageEnhance.Brightness(im).enhance(0.8)
    im.save(filename)
    im.close()

    savepath = 'cut' + str(len(sni_list) + 1) + '.gif'

    # 显示全屏幕截图
    w = Capture(filename)
    buttonCapture.wait_window(w.top)

    # 创建贴图对象
    pastew = PastWindow(w, savepath)
    sni_list.append(pastew)

    root.state('normal')
    os.remove(filename)




def key(event):
    buttonCaptureClick()
root.bind('<Control-Alt-f>', key)

def quit(event):
    exit(0)
root.bind('<Double-Button-1>', quit)

buttonCapture = tk.Button(root, text='截图', command=buttonCaptureClick)
buttonCapture.place(x=60, y=15, width=80, height=30)
# 启动消息主循环
try:
    root.mainloop()
except Exception as e:
    root.destroy()

# buttonCaptureClick()