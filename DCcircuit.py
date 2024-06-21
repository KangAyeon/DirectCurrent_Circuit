from tkinter import *          #i like tkinter
from tkinter import ttk
tk = Tk()

tk.title('DCCOMICStm')           # 회로를 구현할 장(張) 만들기
tk.geometry("1200x600+0+0")
tk.resizable(False,False)


inputjeo1=Frame(tk, relief = "solid", width = 150, height = 600)
inputjeo1.place(x=0, y=0)
inputjeo2=Frame(tk, relief = "solid", width = 146, height = 600)
inputjeo2.place(x=150, y=0)

dp=Frame(tk, relief = "solid", bd = 2, width = 600, height = 600)    #divide window
dp.place(x = 296, y = 0)
ui=Frame(tk, relief = "solid", width = 300, height = 600)
ui.place(x = 900, y = 0)


display = Canvas(dp, bd=0, bg='whitesmoke')             #make display(canvas) Disupulayee Saing Seong
display.place(x = 0, y = 0, width = 600, height = 600)


rows = 20                #Making maplist Maeb Risutu Saing Seong
cols = 20 
mapl = []

for i in range(rows):
    row = []
    for j in range(cols):
        row.append(0)
    mapl.append(row)

rows1 = 20                #Making electron list
cols1 = 20 
electron = []

for i in range(rows1):
    rowa = []
    for j in range(cols1):
        rowa.append(0)
    electron.append(rowa)


userx = 0          #func
usery = 0

def draw_window():
    display.delete('all')
    for i in range(20):                                          #draw display
        display.create_line(30*i, 0, 30*i, 600, fill = "gray")
    for i in range(40):
        display.create_line(0, 30*i, 600, 30*i, fill = "gray")

draw_window()



#이동 커서 지우기(움직임)
def dehighlight():
    global userx, usery
    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30, outline = "gray")


#이동 커서 표시(움직임)
def highlight():
    global userx, usery
    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30, outline = "red")

#이동: 상하좌우
def GO_UP():
    global usery
    dehighlight()
    usery = usery - 1
    if usery == -1:
        usery = 19
    highlight()

def GO_DOWN():
    global usery
    dehighlight()
    usery = usery + 1
    if usery == 20:
        usery = 0
    highlight()

def GO_LEFT():
    global userx
    dehighlight()
    userx = userx-1
    if userx == -1:
        userx = 19
    highlight()

def GO_RIGHT():    
    global userx
    dehighlight()
    userx = userx + 1
    if userx == 20:
        userx = 0 
    highlight()

#지우기
def MAKE_VOID():    
    global mapl, userx, usery
    mapl[usery][userx] = 0
    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30,outline='gray', fill='whitesmoke')

# 저항값 설정
def SELECT_RESISTANCE():
    global mapl, userx, usery
    if mapl[usery][userx] == 'Rlr' or 'Rud':
        if R1spinbox == 0: 


            print('')



def doit():
    print('TRUELY')

#회전
def ROTATE():
    global mapl, userx, usery
    if mapl[usery][userx] == 'lr' :
        MAKE_VOID()
        MAKE_WIRE_UD()
    elif mapl[usery][userx] == 'ud' :
        MAKE_VOID()
        MAKE_WIRE_LR()

    elif mapl[usery][userx] == 'lu' :
        MAKE_VOID()
        MAKE_WIRE_RU()
    elif mapl[usery][userx] == 'ru' :
        MAKE_VOID()
        MAKE_WIRE_RD()
    elif mapl[usery][userx] == 'rd' :
        MAKE_VOID()
        MAKE_WIRE_LD()
    elif mapl[usery][userx] == 'ld' :
        MAKE_VOID()
        MAKE_WIRE_LU()

    elif mapl[usery][userx] == 'lur' :
        MAKE_VOID()
        MAKE_WIRE_URD()
    elif mapl[usery][userx] == 'urd' :
        MAKE_VOID()
        MAKE_WIRE_LDR()
    elif mapl[usery][userx] == 'ldr' :
        MAKE_VOID()
        MAKE_WIRE_ULD()
    elif mapl[usery][userx] == 'uld' :
        MAKE_VOID()
        MAKE_WIRE_LUR()

    elif mapl[usery][userx] == 'Rlr' :
        MAKE_VOID()
        MAKE_RESISTOR_UD()
    elif mapl[usery][userx] == 'Rud' :
        MAKE_VOID()
        MAKE_RESISTOR_LR()

#전선 놓기
def MAKE_WIRE_LR():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'lr'
        display.create_line(userx*30, usery*30+15, userx*30+30, usery*30+15, fill="black")
    else:
        MAKE_VOID()
        MAKE_WIRE_LR()

def MAKE_WIRE_UD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        print('iwant!!')
        mapl[usery][userx] = 'ud'
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+30, fill="black")
def MAKE_WIRE_LU():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'lu'
        display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black")
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black")

def MAKE_WIRE_RU():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'ru'
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black")
        display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black")

def MAKE_WIRE_RD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'rd'
        display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black")
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black")

def MAKE_WIRE_LD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'ld'
        display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black")
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black")

def MAKE_WIRE_LUR():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'lur'
        display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black") #LEFT
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black") #UP
        display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black") #RIGHT
        
def MAKE_WIRE_URD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'urd'
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black") #UP
        display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black") #RIGHT
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black") #DOWN

def MAKE_WIRE_LDR():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'ldr'
        display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black") #LEFT
        display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black") #RIGHT
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black") #DOWN

def MAKE_WIRE_ULD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'uld'
        display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black") #LEFT
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black") #UP
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black") #DOWN

def MAKE_WIRE_LRUD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'quad'
        display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black") #LEFT
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black") #UP
        display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black") #RIGHT
        display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black") #DOWN

#저항 놓기
def MAKE_RESISTOR_LR():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'Rlr'
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15)

        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25)
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5)
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25)
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5)
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25)
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5)
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15)

        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15)
        
def MAKE_RESISTOR_UD():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'Rud'
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3)

        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5)
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9)
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13)
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17)
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21)
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25)
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27)

        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30)

#전지 놓기
def MAKE_BATTERY():
    global mapl, userx, usery
    if mapl[usery][userx] == 0 :
        mapl[usery][userx] = 'B'
        display.create_line(userx*30, usery*30+15, userx*30+11, usery*30+15)
        display.create_line(userx*30+11, usery*30+25, userx*30+11, usery*30+5)
        display.create_line(userx*30+19, usery*30+20, userx*30+19, usery*30+11, width=3)
        display.create_line(userx*30+19, usery*30+15, userx*30+30, usery*30+15)

#나중에할거있으면여기다추가하기
def 나중에할거있으면여기다추가():
    NONE


def keypressed(event):        #when keypressed ~~

    if event.keysym == 'Up' :
        GO_UP()

    elif event.keysym == 'Left' :
        GO_LEFT()

    elif event.keysym == 'Down' :
        GO_DOWN()

    elif event.keysym == 'Right' :
        GO_RIGHT()

    elif event.keysym == 'Return' :
        tempwarn()

    elif event.keysym == 'Escape' :
        closewarn()

    elif event.keysym == 'space' : # 회전
        ROTATE()

    elif event.keysym == 'm' : # 'ㅡ'자
        MAKE_WIRE_LR()

    elif event.keysym == 's' : # 'ㄴ'자
        MAKE_WIRE_RU()

    elif event.keysym == 'n' : # 'ㅜ'자
        MAKE_WIRE_LDR()

    elif event.keysym == 'equal' : # '+'자
        MAKE_WIRE_LRUD()

    elif event.keysym == 'b' : # 밧데리
        MAKE_BATTERY()

    elif event.keysym == 'r' : # 저항
        MAKE_RESISTOR_LR()

    elif event.keysym == 'e' : # erase
        MAKE_VOID()

    # elif event.keysym == 'r' : # start(run) module
    #     amugeona()

    else:                      #Lee Sang Han Button Press >>> 비정의 커맨드 경고 창
        unknowntext = event.keysym,'is not a valid key'  #  위쪽에 정의되지 않은 키 입력들을 unknowntext로 간주, <입력된 키값, 'is not a valid key'>로써 나타냄
        toplevel = Toplevel(tk)
        toplevel.geometry("320x200+820+100")
        toplevel.resizable(False, False)
        toplevel.title("ERROR: not a valid key")  # 창 이름
        label = Label(toplevel, text = unknowntext, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "error", compound = "top")  #  unknowntext출력, i마크 표시(붉은색) 할 창 생성
        label.pack()

        button = Button(toplevel, width = 10, text = "ok", overrelief = "solid", command = toplevel.destroy)  #  ok버튼 누르면 경고 창 삭제
        button.pack()
    # if event.keysym == 'z' + 'ctrl' :  
    #     undo()

def clear():           # 19   clear the window
    global userx, usery, mapl

    dehighlight()
    userx = 0
    usery = 0
    highlight()

    for musaku in range(1, 20):
        for misaku in range(20):
            mapl[misaku][musaku] = 0

    draw_window()

def temp():            # 00   clear()와 경고 창 삭제를 동시에
    global areyouokaytoclear
    clear()
    # deselectall()
    areyouokaytoclear.destroy()

def tempwarn():        # 00   clear, clear경고 창. 비정의 커맨드 경고 창 코드 참고.
    global areyouokaytoclear
    AYOC = "Are You Okay To Clear This Work?"
    areyouokaytoclear = Toplevel(tk)
    areyouokaytoclear.geometry("320x200+820+100")
    areyouokaytoclear.resizable(False, False)
    areyouokaytoclear.title("Are You Okay To Clear This Work?")
    entlabel = Label(areyouokaytoclear, text = AYOC, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "info", compound = "top")
    entlabel.pack()
    yentbutton = Button(areyouokaytoclear, width = 10, text = "yes", overrelief = "solid", command = temp)  #  yes 누르면 경고 창 삭제, clear실행
    noentbutton = Button(areyouokaytoclear, width = 10, text = "no", overrelief = "solid", command = areyouokaytoclear.destroy)  #  no 누르면 경고 창만 삭제
    yentbutton.pack()
    noentbutton.pack()

def close():           # 18   close the window
    tk.quit()
    tk.destroy()

def closewarn():       # 00   close the window with warnning window \ tempwarn 참고
    AYOE = "Are You Okay To Exit This Program?"
    areyouokaytoexit = Toplevel(tk)
    areyouokaytoexit.geometry("320x200+820+100")
    areyouokaytoexit.resizable(False, False)
    areyouokaytoexit.title("Are You Okay To Exit This Program?")
    esclabel = Label(areyouokaytoexit, text = AYOE, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "info", compound = "top")
    esclabel.pack()
    yescbutton = Button(areyouokaytoexit, width = 10, text = "yes", overrelief = "solid", command = close)
    noescbutton = Button(areyouokaytoexit, width = 10, text = "no", overrelief = "solid", command = areyouokaytoexit.destroy)
    yescbutton.pack()
    noescbutton.pack()
# def redo():
# def undo(): 응~ 어차피 지우기 기능 있으니 안 할꺼야~

def aboutlc():
    AYOE = "About DirectCurrent Circuit \n Visualizing DirectCurrent Circuit And Experience It \n \n \n Editors: JunSeok.S HyunJune.J \n email: rkddkdus05@gmail.com"
    aboutLC = Toplevel(tk)
    aboutLC.geometry("320x200+820+100")
    aboutLC.resizable(False, False)
    aboutLC.title("About DirectCurrent Circuit")
    lclabel = Label(aboutLC, text = AYOE, width = 300, height = 150, fg = "medium purple", relief = "solid", bitmap = "info", compound = "top")
    lclabel.pack()
    lcbutton = Button(aboutLC, width = 10, text = "close", overrelief = "solid", command = aboutLC.destroy)
    lcbutton.pack()

def lchelp():
    AYOE = "DirectCurrent Circuit Help \n Commands \n \n \n [m] > [fill 'ㅡ'wire] \n [n] > [fill 'ㅜ'wire] \n [s] > [fill 'ㄴ'wire] \n [+] > [fill '+'wire] \n [b] > [set battery]  \n [r] > [set resistance]  \n [space] > [rotate wire] \n [Esc] > [Exit] \n [Enter] > [Clear] \n [e] > [Erase]"
    LCHelp = Toplevel(tk)
    LCHelp.geometry("320x500+820+100")
    LCHelp.resizable(False, False)
    LCHelp.title("DirectCurrent Circuit Help")
    lclabel = Label(LCHelp, text = AYOE, width = 300, height = 450, fg = "gold4", relief = "solid", bitmap = "info", compound = "top")
    lclabel.pack()
    lcbutton = Button(LCHelp, width = 10, text = "close", overrelief = "solid", command = LCHelp.destroy)
    lcbutton.pack()

def showlist():
    global mapl
    Showlist = Toplevel(tk)
    Showlist.geometry("8000x400")
    Showlist.resizable(False, False)
    Showlist.title("Let's check about it")
    Showlabel = Label(Showlist, text = mapl)
    Showlabel.pack()
    print("Show my walkie talkie man")


def nihahaha():  #  NiHaHaHa!!!!
    Nihahaha = Toplevel(tk)
    Nihahaha.geometry("400x400")
    Nihahaha.resizable(False, False)
    Nihahaha.title("NiHaHaHa!")
    imagenihaha = PhotoImage(file = "nihahaha.PNG")
    Label.image = imagenihaha #  because of Python gabagecollector works reference counting, so i have to 수동으로 참고 횟수 늘려주기.
    nilabel = Label(Nihahaha, image = imagenihaha, compound = "top")
    nilabel.pack(expand = 1, anchor = CENTER)
    print("Nihahaha!")

def amugeona():                   #Most Valuable Code
    global mapl, mapltf


    for minski in range(20):
        for manski in range(1, 20):
            mapltf[minski][manski] = 0

    for x in range(20):
        repeat=0
        repeatlimit=0
        for re in range(20):
            if mapl[re][x] > 1 :
                repeatlimit += 1
        while repeat <= repeatlimit :
            repeat+=1
            for y in range(20):
                if mapl[y][x] == 2 and mapltf[y][x] == 1 :       #wire
                    mapltf[y][x+1] = 1
                    # mapltf[y][x-1] = 1
                    mapltf[y+1][x] = 1
                    mapltf[y-1][x] = 1



def setresistance(self):
    explanationresistance.config(text = '저항 값을 입력하거나 선택')
    if self == '':
        return True
    
    valid = False
    
    if self.isdigit():
        if (int(self) >= 0 and int(self) <= 100):
            valid = True
    return valid

def errorsetresistance(self):
        unknowntext = str(self) + ' is invalid value \nvalid value: 0~100'  #  위쪽에 정의되지 않은 키 입력들을 unknowntext로 간주, <입력된 키값, 'is not a valid key'>로써 나타냄
        toplevel = Toplevel(tk)
        toplevel.geometry("320x200+820+100")
        toplevel.resizable(False, False)
        toplevel.title("ERROR: not a valid key")  # 창 이름
        label = Label(toplevel, text = unknowntext, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "error", compound = "top")  #  unknowntext출력, i마크 표시(붉은색) 할 창 생성
        label.pack()

        button = Button(toplevel, width = 10, text = "ok", overrelief = "solid", command = toplevel.destroy)  #  ok버튼 누르면 경고 창 삭제
        button.pack()
    # explanationresistance.config(text = str(self) + "is invalid value \nvalid value: 0~100")

display.bind_all('<KeyPress>', keypressed)   #when keypressed >> call keypressed()


Button(ui, text = "UP[↑]", command = GO_UP).place(x = 110, y = 50, width = 80, height = 80)  #make 이동 ui

Button(ui, text = "LEFT[←]", command = GO_LEFT).place(x = 30, y = 130, width = 80, height = 80)

Button(ui, text = "RIGHT[→]", command = GO_RIGHT).place(x = 190, y = 130, width = 80, height = 80)

Button(ui, text = "DOWN[↓]", command = GO_DOWN).place(x = 110, y = 210, width = 80, height = 80)

Button(ui, text = 'EXIT[Esc]', command = closewarn).place(x = 120 , y = 500, width = 60, height = 60)

Button(ui, text = "CLEAR[Enter]", command = tempwarn).place(x = 190, y= 400, width = 80, height = 40)

# Button(ui, text = "RUN[r]", command = amugeona).place(x = 190, y= 350, width = 100, height = 40)

Button(ui, text = "WIRE[w]", command = MAKE_WIRE_LR).place(x = 30, y= 400, width = 80, height = 40)

# >> [Noreok]

# Resistance = [r+1 for r in range(0)]

# R1 = ttk.Combobox(inputjeo1, width = 10, height = 10, values = Resistance)
# R1.pack(padx=4)
# R1.set("첫 번째 저항 값 설정") 대충 이거 쓰는 것 보다 훨씬 좋은거 찾았다는 내용~

# I will make a MenuBar and Menu fuction
explanationresistance = Label(inputjeo1, text = "▼저항값을 입력하거나 선택▼", height = 3)
explanationresistance.pack(padx=4)

validate_command = (inputjeo1.register(setresistance), '%P')
invalid_command = (inputjeo1.register(errorsetresistance), '%P')

# for m in range(0, 11):
#     globals()['spinbox'{}.format(m)] = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
    
    # m.pack(padx=4)
R1spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R1spinbox.pack(padx=4)
R2spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R2spinbox.pack(padx=4)
R3spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R3spinbox.pack(padx=4)
R4spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R4spinbox.pack(padx=4)
R5spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R5spinbox.pack(padx=4)
R6spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R6spinbox.pack(padx=4)
R7spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R7spinbox.pack(padx=4)
R8spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R8spinbox.pack(padx=4)
R9spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R9spinbox.pack(padx=4)
R10spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R10spinbox.pack(padx=4)
# 그 더 좋은 방법은 하드코딩을 말하는 것입니다!!  하하하하....






resistancevalues = [r+1 for r in range(0)]

texts = Text(inputjeo2, width=15, height=2)
texts.insert(INSERT, "")
texts.pack(padx=4)



menubar = Menu(tk) # menubar is Menu

menu1 = Menu(menubar, tearoff = 0) # menu1은 첫 번째 Menu, tearoff = 0: 하위 메뉴 분리 기능 사용 유무 판단

menu1.add_command(label = "Clear", command = tempwarn)
menu1.add_separator()
menu1.add_command(label = "Exit", command = closewarn)
menubar.add_cascade(label = "File", menu = menu1)

menu2 = Menu(menubar, tearoff = 0, selectcolor = "green")

menu2.add_radiobutton(label = "Undo", state = "disable")
menu2.add_radiobutton(label = "Redo")
menu2.add_radiobutton(label = "Cut")
menubar.add_cascade(label = "Edit", menu = menu2)

menu3 = Menu(menubar, tearoff = 0)

menu3.add_checkbutton(label = "NA")
menu3.add_checkbutton(label = "mapl", command = showlist)
menu3.add_checkbutton(label = "nihahaha", command = nihahaha)
menubar.add_cascade(label = "Run", menu = menu3)

menu4 = Menu(menubar, tearoff = 0)

menu4.add_command(label = "About DirectCurrentCircuit", command = aboutlc)
menu4.add_separator()
menu4.add_command(label = "D.C. Help", command = lchelp)
menubar.add_cascade(label = "Help", menu = menu4)

tk.config(menu = menubar)

def whiletrue():                 #while True 마춤뻡좀지켜주새요;; 엊절
    global mapl, electron

    for garo in range(20):       #allocate new electron     //     list : [receive1, receive2, electron1, electron2(if exists)]
        for sero in range(20):   #   zz;                           receive : 1-right 2-up 3-left 4-down
            if mapl[garo][sero] != 0 and electron[garo][sero] == 0 :
                electron[garo][sero] = [0, 0, 1]


    for x in range(20):
        for y in range(20):
            if mapl[y][x] == 'B' :
                electron[y][x-1][0] = 1
                del electron[y][x][3]
                electron[y][x-1].append(1)

                isThisDone = False
                ex = x-1
                ey = y

                while isThisDone == False:  #눈앞이아득해진다눈앞이아득해진다눈앞이아득해진다눈앞이아득
                    if mapl[ey][ex] == 'lr' :
                        if electron[ey][ex][0] == 3 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ex+=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 3
                        if electron[ey][ex][0] == 1 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ex-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 1

                    if mapl[ey][ex] == 'ud' :
                        if electron[ey][ex][0] == 4 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ey-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 4
                        if electron[ey][ex][0] == 2 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ey+=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 2


                    if mapl[ey][ex] == 'lu' :
                        if electron[ey][ex][0] == 3 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ey-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 4
                        if electron[ey][ex][0] == 2 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ex-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 1

                    if mapl[ey][ex] == 'ru' :
                        if electron[ey][ex][0] == 1 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ey-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 4 #오늘은여기까지
                        if electron[ey][ex][0] == 2 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ex+=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 4

                    if mapl[ey][ex] == 'rd' :
                        if electron[ey][ex][0] == 1 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ex-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 1
                        if electron[ey][ex][0] == 4 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ey+=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 4

                    if mapl[ey][ex] == 'ld' :
                        if electron[ey][ex][0] == 1 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ex-=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 1
                        if electron[ey][ex][0] == 4 :
                            del electron[ey][ex][len(electron[ey][ex])-1]
                            ey+=1
                            electron[ey][ex].append(1)
                            electron[ey][ex][0] = 4




    tk.after(1000, whiletrue)

tk.after(1000, whiletrue)

tk.mainloop()    #i like thi