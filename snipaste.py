import tkinter 
import tkinter.filedialog 
import os, pdb 
import pyscreenshot as ImageGrab
from PIL import ImageEnhance 
from time import sleep 


root = tkinter.Tk()
root.geometry('100x60+400+400')


class Capture:
    def __init__(self, png):
        #x，y记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.sel = False
        #屏幕尺寸
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()
        #创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=self.screenWidth, height = self.screenHeight)
        #顶级容器不显示最大化，最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width = self.screenWidth, height = self.screenHeight)
        #显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(self.screenWidth//2, self.screenHeight//2, image=self.image)
        self.canvas.pack()


        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #标识开始截图
            self.sel = True 
        #绑定左键按下函数
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        #鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            global lastDraw, r, c
            try:
                #删除刚画完的图形，不然先前绘制的在一起是黑黑的叠在一起的矩形
                self.canvas.delete(lastDraw)
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass 
            #绘制点击左键时的十字线
            r = self.canvas.create_line(0, event.y, self.screenWidth, event.y, fill='orange')
            c = self.canvas.create_line(event.x, 0, event.x, self.screenHeight, fill='orange')
            if(not self.sel):
                pass 
            else:
                #开始选区绘制矩形
                lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='white')
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        def onMouseMove(event):
            #不点击时鼠标移动，绘制十字线
            global r, c
            try:
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass 
            r = self.canvas.create_line(0, event.y, self.screenWidth, event.y, fill='orange')
            c = self.canvas.create_line(event.x, 0, event.x, self.screenHeight, fill='orange')
        self.canvas.bind('<Montion>', onMouseMove)

        def onEscPressd(event):
            self.top.destroy()
        self.canvas.bind('<Cancel>', onEscPressd)

        #鼠标抬起，保存截图区域
        def onLeftButtonUp(event):
            self.sel = False 
            try:
                self.canvas.delete(lastDraw)
            except:
                pass 
            sleep(0.1)
            #考虑鼠标从右下按下从左上抬起, 进行排序
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            self.pic = ImageGrab.grab((left+1, top+1, right, bottom))
            self.pw = right - left 
            self.ph = top - bottom 
            #关闭顶级容器
            self.top.destroy()

class PicPaste:
    def __init__(self, capture):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.X.set(capture.X.get())
        self.Y.set(capture.Y.get())
        self.pic = capture.pic 
        self.Width = capture.pw 
        self.Height = capture.ph 
        #创建顶级窗口
        self.top = tkinter.Toplevel()
        self.top.overrideredirect(True)
        positon = self.Width + "x" + self.Height + '+' + self.X.get() + '+' + self.Y.get()
        print(positon)
        self.top.geometry(positon)

        def doubleButtonClick(event):
            self.top.destroy()
        self.top.bind('<Double-Button-1>', doubleButtonClick)



#开始截图
def buttonCaptureClick():
    #最小化主窗口
    root.state('icon')
    sleep(0.2)
    filename ='temp.gif'
    im =ImageGrab.grab()
    im = ImageEnhance.Brightness(im).enhance(0.8)
    im.save(filename)
    im.close()
    #显示全屏幕截图
    w =Capture(filename)
    p = PicPaste(w)
    buttonCapture.wait_window(w.top)
    # pdb.set_trace()
    #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    root.state('normal')
    os.remove(filename)


buttonCapture = tkinter.Button(root, text='截图', command=buttonCaptureClick)
buttonCapture.place(x=10, y=10, width=80, height=30)
#启动消息主循环
try:
    root.mainloop()
except:
    root.destroy()

