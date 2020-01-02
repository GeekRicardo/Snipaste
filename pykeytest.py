import pyxhook

keys = ['Control_L', 'Alt_L', 'f']
# 监听键盘
ctrl , alt, f = False, False, False
def onkeypress(e):
    global ctrl, alt, f
    if(ctrl and alt and f):
        print('c+a+f')
        ctrl, alt, f = False, False, False
    k = e.Key
    print('--- ', e)
    if(k in keys):
        if(k == keys[0]):
            ctrl = True
        elif(k == keys[1]):
            alt = True
        elif(k == keys[2]):
            f = True

new_hook=pyxhook.HookManager()
new_hook.KeyDown=onkeypress
new_hook.HookKeyboard()
new_hook.start()
print('aaa234')