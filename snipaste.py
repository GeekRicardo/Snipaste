import tkinter 
import tkinter.filedialog 
import os, pdb 
import pyscreenshot as ImageGrab
from PIL import ImageEnhance 
from time import sleep 

from capture import Capture, root, l, t, w, h 


class PicPaste:
    def __init__(self, capture):
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.X.set(capture.X.get())
        self.Y.set(capture.Y.get())
        # self.pic = capture.pic 
        # pdb.set_trace()
        self.Width = w 
        self.Height = h 
        #创建顶级窗口
        self.top = tkinter.Toplevel(root)
        self.top.overrideredirect(True)
        positon = str(self.Width) + "x" + str(self.Height) + '+' + str(l) + '+' + str(t)
        print(positon)
        self.top.geometry(positon)
        self.canvas = tkinter.Canvas(self.top, bg='white')
        self.canvas.create_image(0,0, image=tkinter.PhotoImage(file='./temp.gif'))
        self.canvas.pack()

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
    buttonCapture.wait_window(w.toplevel)
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

