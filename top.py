import tkinter as tk

# root = tk.Tk()
# # 指定窗口的大小
# root.geometry('200x60+500+400')
# # 不允许改变窗口大小
# root.resizable(False, False)
# root.title("OCR")

top = tk.Toplevel( width=200, height=80)

top.geometry("+600+500")
top.overrideredirect(True)
self = None

def _on_move( event):
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
    top.geometry(geo_str)
top.bind('<B1-Motion>', _on_move)

def _on_tap(event):
    self.root_x, self.root_y=event.x_root, event.y_root
    self.abs_x, self.abs_y=self.snip_top.winfo_x(), self.snip_top.winfo_y()
top.bind("<Button-1>", _on_tap)

# root.mainloop()
top.mainloop()