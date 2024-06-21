# KeyCode Checker

import tkinter
key=0
def key_down(e):
    global key
    key = e.keysym
    print(str(key))



Tk = tkinter.Tk()
Tk.title("키코드 확인기. 디버그 창에서 확인 가능")
Tk.resizable(False, False)
image = tkinter.PhotoImage(file="kufufufu.PNG")
tkinter.Label.image = image
label = tkinter.Label(Tk, image = image, compound = "top")
label.pack()


Tk.bind("<KeyPress>", key_down)
Tk.mainloop()