import tkinter 
import os, pdb 
import pyscreenshot as ImageGrab
from PIL import ImageEnhance 
from time import sleep 

# from capture import Capture, root#, l, t, w, h 

root = tkinter.Tk()
root.title('snipaste')
#指定窗口的大小
root.geometry('100x50+400+300')
#不允许改变窗口大小
root.resizable(False,False)
p = []

class PicPaste:
    def __init__(self, capture, p):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.X.set(capture.X.get())
        self.Y.set(capture.Y.get())
        # self.pic = capture.pic 
        # pdb.set_trace()
        print(p)
        # self.position = capture.position
        # self.Width = capture.pw 
        # self.Height = capture.ph
        #创建顶级窗口
        
        


class Capture:
    def __init__(self, png, p):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.sel = False
        #屏幕尺寸
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()
        #创建顶级组件容器
        self.toplevel = tkinter.Toplevel(root, width=self.screenWidth, height=self.screenHeight)
        #不显示最大化、最小化按钮
        self.toplevel.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.toplevel,bg='white', width=self.screenWidth, height=self.screenHeight)
        #显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(self.screenWidth//2, self.screenHeight//2, image=self.image)
        self.canvas.pack()

        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            # pdb.set_trace()
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel =True
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        #鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            # pdb.set_trace()
            global lastDraw, r, c
            try:
                #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass
            #没有点击左键时绘制十字线
            r = self.canvas.create_line(0, event.y, self.screenWidth, event.y, fill='white')
            c = self.canvas.create_line(event.x, 0, event.x, self.screenHeight, fill='white')
            if not self.sel:
                # print(event.x, event.y, self.screenWidth, self.screenHeight)
                pass
            else:
                lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='orange')
                # print(event.x, event.y, self.scrself.eenWidth, self.screenWidth)
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)
        def onMouseMove(event):
            #不点击时的鼠标移动，绘制十字线
            global  r, c
            try:
                #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass
            #没有点击左键时绘制十字线
            r = self.canvas.create_line(0, event.y, self.screenWidth, event.y, fill='white')
            c = self.canvas.create_line(event.x, 0, event.x, self.screenHeight, fill='white')
        self.canvas.bind('<Motion>', onMouseMove)

        def onEscPressd(event):
            self.toplevel.destroy()
        self.canvas.bind('<Cancel>', onEscPressd)

        #获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel =False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic =ImageGrab.grab((left+1, top+1, right, bottom))
            p.append(left)
            p.append(top)
            p.append( right - left - 1)  #减去边缘线1px
            p.append( bottom - top - 1)
            print('onLeftButtonUp --> ', p)
            sleep(1)
            if pic:
                pic.save('./temp.gif')
                # 关闭当前窗口
                self.toplevel.destroy()
            

        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)


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
    w =Capture(filename, p)
    # pdb.set_trace()
    print(p)
    top = tkinter.Toplevel(root)
    top.overrideredirect(True)
    pdb.set_trace()
    positon = '{}x{}+{}+{}'.format(p[0], p[1], p[2], p[3])  
    print(positon)
    top.geometry(positon)
    c = tkinter.Canvas(top, width=p[2], height=p[3])
    pic = tkinter.PhotoImage(file='./temp.gif')
    c.create_image(p[2]//2, p[3]//2, image=pic)
    c.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    def doubleButtonClick(event):
        top.destroy()
    top.bind('<Double-Button-1>', doubleButtonClick)
    # p = PicPaste(w, position)
    buttonCapture.wait_window(w.toplevel)
    # pdb.set_trace()
    #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    root.state('normal')
    # os.remove(filename)
buttonCapture = tkinter.Button(root, text='截图', command=buttonCaptureClick)
buttonCapture.place(x=10, y=10, width=80, height=30)
#启动消息主循环
try:
    root.mainloop()
except:
    root.destroy()


