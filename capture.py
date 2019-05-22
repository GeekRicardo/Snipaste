import tkinter
import tkinter.filedialog
import os, pdb
import pyscreenshot as  ImageGrab
from aip import AipOcr
from PIL import ImageEnhance
client = AipOcr('10684055', 'Y15dcjjkq2dLHB1NmdCN9ODI', 'keOYEXKG1RXnLyGLa4wfCr003kKE1zhh')

from time import sleep
root = tkinter.Tk()
#指定窗口的大小
root.geometry('100x50+400+300')
#不允许改变窗口大小
root.resizable(False,False)

class MyCapture:
    def __init__(self, png):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.sel = False
        #屏幕尺寸
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()
        #创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=self.screenWidth, height=self.screenHeight)
        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top,bg='white', width=self.screenWidth, height=self.screenHeight)
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
                # print(event.x, event.y, self.screenWidth, self.screenWidth)
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
            self.top.destroy()
        self.canvas.bind('<Cancel>', onEscPressd)

        #获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel =False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            sleep(0.1)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic =ImageGrab.grab((left+1, top+1, right, bottom))
            #关闭顶级容器
            self.top.destroy()
            #弹出保存截图对话框
            # fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image','*.jpg *.png')])
            if pic:
                pic.save('./temp.bmp')
                #关闭当前窗口
                # self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    def getText(self):
        with open('./temp.bmp', 'rb') as img:
            img = img.read()
            result = client.basicGeneral(img)
            return result
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
    w =MyCapture(filename)
    buttonCapture.wait_window(w.top)
    # pdb.set_trace()
    result = w.getText()
    printresult(result)
    #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    root.state('normal')
    os.remove(filename)

def printresult(json):
    print('\n' + '-'*20)
    if(json['words_result_num'] > 0):
        for i in range(0,json['words_result_num'] ):
            print(json['words_result'][i]['words'])
    else:
        print('+'* 5 + '  请重试！  ' + '+'*5)
    print('\n' + '-'*20)

buttonCapture = tkinter.Button(root, text='截图', command=buttonCaptureClick)
buttonCapture.place(x=10, y=10, width=80, height=30)
#启动消息主循环
try:
    root.mainloop()
except:
    root.destroy()

