from tkinter import *          #i like tkinter
tk = Tk()

tk.title('DCCOMICStm')           # 회로를 구현할 장(張) 만들기
tk.geometry("1200x600+0+0")
tk.resizable(False,False)


inputjeo1=Frame(tk, relief = "solid", width = 150, height = 300)
inputjeo1.place(x=0, y=0)
inputjeo2=Frame(tk, relief = "solid", width = 146, height = 300)
inputjeo2.place(x=150, y=0)
inputjeo3=Frame(tk, relief = "solid", width = 300, height = 300)
inputjeo3.place(x=0, y=300)

dp=Frame(tk, relief = "solid", bd = 2, width = 600, height = 600)    #divide window
dp.place(x = 296, y = 0)
ui=Frame(tk, relief = "solid", width = 300, height = 600)
ui.place(x = 900, y = 0)


display = Canvas(dp, bd=0, bg='whitesmoke')             #make display(canvas) Disupulayee Saing Seong
display.place(x = 0, y = 0, width = 600, height = 600)


rows = 20                #Making maplist Maeb Risutu Saing Seong
cols = 20 
mapl = []
resistors = []

for i in range(rows):
    row = []
    for j in range(cols):
        row.append('')
    mapl.append(row)

rows1 = 20
cols1 = 20 
electron = []

for i in range(rows1):
    rowa = []
    for j in range(cols1):
        rowa.append(0)
    electron.append(rowa)


userx = 0          #func
usery = 0
afteroperate=False

def draw_window():
    display.delete('all')
    for i in range(20):                                          #draw display
        display.create_line(30*i, 0, 30*i, 600, fill = "gray")
    for i in range(20):
        display.create_line(0, 30*i, 600, 30*i, fill = "gray")
    # for i in range(4):
    #     display.create_line(0, 150*i, 600, 150*i, fill = "black")
    # for i in range(4):
    #     display.create_line(150*i, 0, 150*i, 600, fill = "black")

draw_window()



#이동 커서 지우기(움직임)
def dehighlight():
    global userx, usery
    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30, outline = "gray")


#이동 커서 표시(움직임)
def highlight():
    global userx, usery, afteroperate
    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30, outline = "red")
    if afteroperate == True :
        resultDisplayer(userx, usery)
        #print('imgonnadi') # 걍 죽셈 ㅋㅋ


def resultDisplayer(x, y):
    global mapl, finalResult, resultDisplay, electricCurrent
    #print('맵앨 :', mapl[y][x])
    if mapl[y][x] == 'B':
        resultDisplay.config(text=f'X좌표 : {x+1}\nY좌표 : {y+1}\n전압 : {battery_value}\n전류 : {electricCurrent}')
        #print('im changed!!!!')
    elif "Rlr" in mapl[y][x] or "Rud" in mapl[y][x]:
        electricCurrentCalculation()
        #print(finalResult)
        if finalResult[y][x] != NONE :
            resultDisplay.config(text=f'X좌표 : {x+1}\nY좌표 : {y+1}\n전위차 : {finalResult[y][x][1]}\n전류 : {finalResult[y][x][2]}\n저항 : {finalResult[y][x][0]}\n소비전력 : {finalResult[y][x][3]}')
    else:
        resultDisplay.config(text='NONE')


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
    mapl[usery][userx] = ''
    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30,outline='gray', fill='whitesmoke')

# 저항값 설정
def SELECT_RESISTANCE1(): 
    global mapl, userx, usery 
    if mapl[usery][userx] == 'Rlr': 
        mapl[usery][userx] = 'Rlr1' 
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15, fill='red') 
        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25, fill='red') 
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5, fill='red') 
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25, fill='red') 
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5, fill='red') 
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25, fill='red') 
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5, fill='red') 
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15, fill='red') 
        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15, fill='red') 

    elif mapl[usery][userx] == 'Rud': 
        mapl[usery][userx] = 'Rud1' 
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3, fill='red') 
        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5, fill='red') 
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9, fill='red') 
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13, fill='red') 
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17, fill='red') 
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21, fill='red') 
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25, fill='red') 
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27, fill='red') 
        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30, fill='red') 

def SELECT_RESISTANCE2(): 
    global mapl, userx, usery 
    if mapl[usery][userx] == 'Rlr': 
        mapl[usery][userx] = 'Rlr2' 
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15, fill='DarkOrange1') 
        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25, fill='DarkOrange1') 
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5, fill='DarkOrange1') 
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25, fill='DarkOrange1') 
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5, fill='DarkOrange1') 
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25, fill='DarkOrange1') 
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5, fill='DarkOrange1') 
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15, fill='DarkOrange1') 
        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15, fill='DarkOrange1') 

    elif mapl[usery][userx] == 'Rud': 
        mapl[usery][userx] = 'Rud2' 
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3, fill='DarkOrange1') 
        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5, fill='DarkOrange1') 
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9, fill='DarkOrange1') 
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13, fill='DarkOrange1') 
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17, fill='DarkOrange1') 
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21, fill='DarkOrange1') 
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25, fill='DarkOrange1') 
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27, fill='DarkOrange1') 
        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30, fill='DarkOrange1') 

def SELECT_RESISTANCE3(): 
    global mapl, userx, usery 
    if mapl[usery][userx] == 'Rlr': 
        mapl[usery][userx] = 'Rlr3' 
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15, fill='gold') 
        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25, fill='gold') 
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5, fill='gold') 
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25, fill='gold') 
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5, fill='gold') 
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25, fill='gold') 
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5, fill='gold') 
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15, fill='gold') 
        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15, fill='gold') 

    elif mapl[usery][userx] == 'Rud': 
        mapl[usery][userx] = 'Rud3' 
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3, fill='gold') 
        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5, fill='gold') 
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9, fill='gold') 
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13, fill='gold') 
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17, fill='gold') 
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21, fill='gold') 
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25, fill='gold') 
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27, fill='gold') 
        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30, fill='gold') 

def SELECT_RESISTANCE4(): 
    global mapl, userx, usery 
    if mapl[usery][userx] == 'Rlr': 
        mapl[usery][userx] = 'Rlr4' 
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15, fill='green2') 
        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25, fill='green2') 
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5, fill='green2') 
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25, fill='green2') 
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5, fill='green2') 
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25, fill='green2') 
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5, fill='green2') 
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15, fill='green2') 
        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15, fill='green2') 

    elif mapl[usery][userx] == 'Rud': 
        mapl[usery][userx] = 'Rud4' 
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3, fill='green2') 
        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5, fill='green2') 
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9, fill='green2') 
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13, fill='green2') 
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17, fill='green2') 
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21, fill='green2') 
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25, fill='green2') 
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27, fill='green2') 
        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30, fill='green2') 

def SELECT_RESISTANCE5(): 
    global mapl, userx, usery 
    if mapl[usery][userx] == 'Rlr': 
        mapl[usery][userx] = 'Rlr5' 
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15, fill='RoyalBlue4') 
        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25, fill='RoyalBlue4') 
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5, fill='RoyalBlue4') 
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25, fill='RoyalBlue4') 
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5, fill='RoyalBlue4') 
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25, fill='RoyalBlue4') 
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5, fill='RoyalBlue4') 
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15, fill='RoyalBlue4') 
        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15, fill='RoyalBlue4') 

    elif mapl[usery][userx] == 'Rud': 
        mapl[usery][userx] = 'Rud5' 
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3, fill='RoyalBlue4') 
        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5, fill='RoyalBlue4') 
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9, fill='RoyalBlue4') 
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13, fill='RoyalBlue4') 
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17, fill='RoyalBlue4') 
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21, fill='RoyalBlue4') 
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25, fill='RoyalBlue4') 
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27, fill='RoyalBlue4') 
        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30, fill='RoyalBlue4') 

def SELECT_RESISTANCE6(): 
    global mapl, userx, usery 
    if mapl[usery][userx] == 'Rlr': 
        mapl[usery][userx] = 'Rlr6' 
        display.create_line(userx*30, usery*30+15, userx*30+3, usery*30+15, fill='purple3') 
        display.create_line(userx*30+3, usery*30+15, userx*30+5, usery*30+25, fill='purple3') 
        display.create_line(userx*30+5, usery*30+25, userx*30+9, usery*30+5, fill='purple3') 
        display.create_line(userx*30+9, usery*30+5, userx*30+13, usery*30+25, fill='purple3') 
        display.create_line(userx*30+13, usery*30+25, userx*30+17, usery*30+5, fill='purple3') 
        display.create_line(userx*30+17, usery*30+5, userx*30+21, usery*30+25, fill='purple3') 
        display.create_line(userx*30+21, usery*30+25, userx*30+25, usery*30+5, fill='purple3') 
        display.create_line(userx*30+25, usery*30+5, userx*30+27, usery*30+15, fill='purple3') 
        display.create_line(userx*30+27, usery*30+15, userx*30+30, usery*30+15, fill='purple3') 

    elif mapl[usery][userx] == 'Rud': 
        mapl[usery][userx] = 'Rud6' 
        display.create_line(userx*30+15, usery*30, userx*30+15, usery*30+3, fill='purple3') 
        display.create_line(userx*30+15, usery*30+3, userx*30+25, usery*30+5, fill='purple3') 
        display.create_line(userx*30+25, usery*30+5, userx*30+5, usery*30+9, fill='purple3') 
        display.create_line(userx*30+5, usery*30+9, userx*30+25, usery*30+13, fill='purple3') 
        display.create_line(userx*30+25, usery*30+13, userx*30+5, usery*30+17, fill='purple3') 
        display.create_line(userx*30+5, usery*30+17, userx*30+25, usery*30+21, fill='purple3') 
        display.create_line(userx*30+25, usery*30+21, userx*30+5, usery*30+25, fill='purple3') 
        display.create_line(userx*30+5, usery*30+25, userx*30+15, usery*30+27, fill='purple3') 
        display.create_line(userx*30+15, usery*30+27, userx*30+15, usery*30+30, fill='purple3') 


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
        
    elif mapl[usery][userx] == 'lur.' :
        MAKE_VOID()
        MAKE_WIRE_URD1()
    elif mapl[usery][userx] == 'urd.' :
        MAKE_VOID()
        MAKE_WIRE_LDR1()
    elif mapl[usery][userx] == 'ldr.' :
        MAKE_VOID()
        MAKE_WIRE_ULD1()
    elif mapl[usery][userx] == 'uld.' :
        MAKE_VOID()
        MAKE_WIRE_LUR1()

    elif mapl[usery][userx] == 'Rlr' :
        MAKE_VOID()
        MAKE_RESISTOR_UD()
    elif mapl[usery][userx] == 'Rud' :
        MAKE_VOID()
        MAKE_RESISTOR_LR()

#전선 놓기
def up(color):
    display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill=color)

def down(color):
    display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill=color)

def left(color):
    display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill=color)

def right(color):
    display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill=color)



def up1(color):
    display.create_line(ex*30+15, ey*30+15, ex*30+15, ey*30, fill=color)

def down1(color):
    display.create_line(ex*30+15, ey*30+15, ex*30+15, ey*30+30, fill=color)

def left1(color):
    display.create_line(ex*30, ey*30+15, ex*30+15, ey*30+15, fill=color)

def right1(color):
    display.create_line(ex*30+30, ey*30+15, ex*30+15, ey*30+15, fill=color)

def upArrow(ex, ey):
    display.create_polygon(ex*30+15, ey*30+3, ex*30+20, ey*30+8, ex*30+10, ey*30+8)

def downArrow(ex, ey):
    display.create_polygon(ex*30+15, ey*30+27, ex*30+19, ey*30+22, ex*30+11, ey*30+22)

def leftArrow(ex, ey):
    display.create_polygon(ex*30+3, ey*30+15, ex*30+8, ey*30+20, ex*30+8, ey*30+10)

def rightArrow(ex, ey):
    display.create_polygon(ex*30+27, ey*30+15, ex*30+22, ey*30+20, ex*30+22, ey*30+10)

def MAKE_WIRE_LR():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'lr'
        display.create_line(userx*30, usery*30+15, userx*30+30, usery*30+15, fill='black')
    else:
        MAKE_VOID()
        MAKE_WIRE_LR()

def MAKE_WIRE_UD():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        # print('iwant!!')
        mapl[usery][userx] = 'ud'
        up('black')
        down('black')

def MAKE_WIRE_LU():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'lu'
        left("black")
        up("black")

def MAKE_WIRE_RU():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'ru'
        right("black")
        up("black")

def MAKE_WIRE_RD():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'rd'
        right("black")
        down("black")

def MAKE_WIRE_LD():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'ld'
        left("black")
        down('black')

def MAKE_WIRE_LUR():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'lur'
        left("black")
        up("black")
        right("black")
        
def MAKE_WIRE_URD():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'urd'
        up("black")
        right("black")
        down("black")

def MAKE_WIRE_LDR():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'ldr'
        left("black")
        down("black")
        right("black")

def MAKE_WIRE_ULD():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'uld'
        up("black")
        left("black")
        down("black")

def MAKE_WIRE_LUR1():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'lur.'
        left("black")
        up("black")
        right("black")
        display.create_oval(userx*30+12, usery*30+12, userx*30+18, usery*30+18)
        
def MAKE_WIRE_URD1():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'urd.'
        up("black")
        right("black")
        down("black")
        display.create_oval(userx*30+12, usery*30+12, userx*30+18, usery*30+18)

def MAKE_WIRE_LDR1():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'ldr.'
        left("black")
        down("black")
        right("black")
        display.create_oval(userx*30+12, usery*30+12, userx*30+18, usery*30+18)

def MAKE_WIRE_ULD1():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
        mapl[usery][userx] = 'uld.'
        up("black")
        left("black")
        down("black")
        display.create_oval(userx*30+12, usery*30+12, userx*30+18, usery*30+18)

# def MAKE_WIRE_LRUD():
#     global mapl, userx, usery
#     if mapl[usery][userx] == 0 :
#         mapl[usery][userx] = 'quad'
#         display.create_line(userx*30, usery*30+15, userx*30+15, usery*30+15, fill="black") #LEFT
#         display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30, fill="black") #UP
#         display.create_line(userx*30+30, usery*30+15, userx*30+15, usery*30+15, fill="black") #RIGHT
#         display.create_line(userx*30+15, usery*30+15, userx*30+15, usery*30+30, fill="black") #DOWN

#저항 놓기
def MAKE_RESISTOR_LR():
    global mapl, userx, usery
    if mapl[usery][userx] == '' :
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
    if mapl[usery][userx] == '' :
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
    baddery = True
    for i in range(20):
        for j in range(20):
            if mapl[i][j] == 'B' :
                baddery = False
    if mapl[usery][userx] == '' and baddery == True:
        mapl[usery][userx] = 'B'
        display.create_line(userx*30, usery*30+15, userx*30+11, usery*30+15)
        display.create_line(userx*30+11, usery*30+25, userx*30+11, usery*30+5)
        display.create_line(userx*30+19, usery*30+20, userx*30+19, usery*30+11, width=3)
        display.create_line(userx*30+19, usery*30+15, userx*30+30, usery*30+15)

# 실행
def OPERATE():
    global batteryspinbox, afteroperate
    # 전압 0이면 실행 안되게.
    if battery_value == 0:
        toplevel = Toplevel(tk)
        toplevel.geometry("320x200+820+100")
        toplevel.resizable(False, False)
        toplevel.title("ERROR: not a valid battery값")  # 창 이름
        label = Label(toplevel, text = "battery is 0 please set battery값", width = 200, height = 50, fg = "red", relief = "solid", bitmap = "error", compound = "top")  #  unknowntext출력, i마크 표시(붉은색) 할 창 생성
        label.pack()

        button = Button(toplevel, width = 10, text = "ok", overrelief = "solid", command = toplevel.destroy)  #  ok버튼 누르면 경고 창 삭제
        button.pack()
    else:
        amugeona()
        print("전지 도달")
        #print(f"저항 리스트: {resistors}")
        #print(batteryspinbox)
        afteroperate=True
        

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

    elif event.keysym == 'm' or event.keysym == 'l': # 'ㅡ'or'ㅣ'자
        MAKE_WIRE_LR()

    elif event.keysym == 's' : # 'ㄴ'자
        MAKE_WIRE_RU()

    elif event.keysym == 'n' : # 갈라지는 삼발이:"ㅡ"계열. 'ㅜ'자
        MAKE_WIRE_LDR()

    elif event.keysym == 'h' : # 갈라지는 삼발이:"ㅡ"계열. 'ㅗ'자
        MAKE_WIRE_LUR()

    elif event.keysym == 'j': # 만나는 삼발이: "ㅣ"계열. 'ㅓ'자
        MAKE_WIRE_ULD1()

    elif event.keysym == 'k': # 만나는 삼발이: "ㅣ"계열. 'ㅏ'자
        MAKE_WIRE_URD1()

    # elif event.keysym == 'equal' : # '+'자
    #     MAKE_WIRE_LRUD()

    elif event.keysym == 'b' : # 밧데리
        MAKE_BATTERY()

    elif event.keysym == 'r' : # 저항
        MAKE_RESISTOR_LR()

    elif event.keysym == 'e' : # erase
        MAKE_VOID()

    elif event.keysym == '1' :
        SELECT_RESISTANCE1()

    elif event.keysym == '2' :
        SELECT_RESISTANCE2()

    elif event.keysym == '3' :
        SELECT_RESISTANCE3()

    elif event.keysym == '4' :
        SELECT_RESISTANCE4()

    elif event.keysym == '5' :
        SELECT_RESISTANCE5()

    elif event.keysym == '6' :
        SELECT_RESISTANCE6()

    elif event.keysym == 'o' :
        OPERATE()

    # elif event.keysym == 'g':
    #     print(battery_value)

    # 당신의 아무거나. 스타트로 대체되다. 불만 있습니까? Korean Heroes? !!!!!!!

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
            mapl[misaku][musaku] = ''

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
    AYOE = "About DirectCurrent Circuit \n Visualizing DirectCurrent Circuit And Experience It \n \n \n Editors: MinSu.L JunSeok.S HyunJune.J \n email: rkddkdus05@gmail.com"
    aboutLC = Toplevel(tk)
    aboutLC.geometry("320x200+820+100")
    aboutLC.resizable(False, False)
    aboutLC.title("About DirectCurrent Circuit")
    lclabel = Label(aboutLC, text = AYOE, width = 300, height = 150, fg = "medium purple", relief = "solid", bitmap = "info", compound = "top")
    lclabel.pack()
    lcbutton = Button(aboutLC, width = 10, text = "close", overrelief = "solid", command = aboutLC.destroy)
    lcbutton.pack()

def lchelp():
    AYOE = "DirectCurrent Circuit Help \n Commands \n \n \n [m(ㅡ)] > [fill 'ㅡ'wire] \n [l(ㅣ)] > [fill 'ㅣ'wire] \n \n derived from 'ㅡ' is fill Current Distribution wire \n [n(ㅜ)] > [fill 'ㅜ'wire] \n [h(ㅗ)] > [fill 'ㅗ'wire] \n \n derived from 'ㅣ' is fill Current Collecting wire \n [j(ㅓ)] > [fill 'ㅓ'wire] \n [k(ㅏ)] > [fill 'ㅏ'wire] \n \n [s(ㄴ)] > [fill 'ㄴ'wire] \n [b] > [set battery]  \n [r] > [set resistance]  \n [space] > [rotate wire] \n [Esc] > [Exit] \n [Enter] > [Clear] \n [e] > [Erase] \n [o] > [Operate] \n [1] > [Resistance1] \n [2] > [Resistance2] \n [3] > [Resistance3] \n [4] > [Resistance4] \n [5] > [Resistance5] \n [6] > [Resistance6] "
    LCHelp = Toplevel(tk)
    LCHelp.geometry("320x520+820+100")
    LCHelp.resizable(False, False)
    LCHelp.title("DirectCurrent Circuit Help")
    lclabel = Label(LCHelp, text = AYOE, width = 300, height = 470, fg = "gold4", relief = "solid", bitmap = "info", compound = "top")
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
    global mapl, electron, isThisDone, ex, ey, direction, isThisAllDone
    #print("아무거나함수 실행")

    for garo in range(20):       #allocate new electron     //     list : [receive1, receive2, electron1, electron2(if exists)]
        for sero in range(20):   #   zz;                           receive : 1-right 2-up 3-left 4-down
            if mapl[garo][sero] != 0 and electron[garo][sero] == 0 :
                electron[garo][sero] = [0, 0, 1]


    for x in range(20): 
        for y in range(20):
            if mapl[y][x] == 'B' :

                isThisDone = False
                isThisAllDone = False
                ex = x-1
                ey = y
                direction = 'l'

                ihatethisshit()

    resistorCalculation()

def printcurlocation():
    global ex, ey, mapl, direction
    print(f"전류의 현재위치: ({ex}, {ey}); 전류의 현재맵앨: {mapl[ey][ex]}; 전류의 현재방향: {direction}")

def ihatethisshit():                 #while True 마춤뻡좀지켜주새요;; 엊절;; 싫음ㅅㄱ
    global mapl, ex, ey, direction, isThisAllDone, resistors, isThisDone, resistorLocation
    #print("씠함수 실행")
    resistorLocation = []
    resistors = []
    
    while isThisDone == False and isThisAllDone == False:
        printcurlocation()

        if mapl[ey][ex] == 'B' :
            isThisAllDone = True
            isThisDone = True

        전선을만났을때이동()
        저항을만났을때이동(resistors, resistorLocation)
        삼발이를만났을때이동()
        
        if mapl[ey][ex][-1] == '.':    # When MEET SAMBARI END
            sambariEnd.append(direction)


def 전선을만났을때이동():
    global mapl, ex, ey, direction
    if mapl[ey][ex] == 'lr' :     #Just Straight Wire
        display.create_line(ex*30, ey*30+15, ex*30+30, ey*30+15, fill='deepskyblue')
        if direction == 'l' :
            ex-=1
            direction = 'l'
        elif direction == 'r' :
            ex+=1
            direction='r'
    if mapl[ey][ex] == 'ud' :
        up1('deepskyblue')
        down1('deepskyblue')
        if direction == 'u' :
            ey-=1
            direction = 'u'
        elif direction == 'd' :
            ey+=1
            direction = 'd'

    if mapl[ey][ex] == 'lu' :     #Turrnrrnrrnrnrnring wire
        left1('deepskyblue')
        up1('deepskyblue')
        if direction == 'r' :
            ey-=1
            direction = 'u'
        elif direction == 'd' :
            ex-=1
            direction='l'
    if mapl[ey][ex] == 'ru' :
        right1('deepskyblue')
        up1('deepskyblue')
        if direction == 'l' :
            ey-=1
            direction = 'u'
        elif direction == 'd' :
            ex+=1
            direction='r'
    if mapl[ey][ex] == 'rd' :
        right1('deepskyblue')
        down1('deepskyblue')
        if direction == 'l' :
            ey+=1
            direction = 'd'
        elif direction == 'u' :
            ex+=1
            direction='r'
    if mapl[ey][ex] == 'ld' :
        left1('deepskyblue')
        down1('deepskyblue')
        if direction == 'r' :
            ey+=1
            direction = 'd'
        elif direction == 'u' :
            ex-=1
            direction='l'

def 저항을만났을때이동(저항값을담을리스트, 저항위치를담을리스트):
    global mapl, ex, ey, direction, resistorLocation
    if mapl[ey][ex][:3] == 'Rlr' :        # WHEN MEET RESISTORRRRRRR
        저항값을담을리스트.append(get_resistor_value(ex, ey))
        저항위치를담을리스트.append((ex, ey))
        if direction == 'l' :
            ex-=1
            direction == 'l'
        elif direction == 'r' :
            ex+=1
            direction='r'
    if mapl[ey][ex][:3] == 'Rud' :
        저항값을담을리스트.append(get_resistor_value(ex, ey))
        저항위치를담을리스트.append((ex, ey))
        if direction == 'u' :
            ey-=1
            direction == 'u'
        elif direction == 'd' :
            ey+=1
            direction='d'

def 삼발이를만났을때이동():
    global mapl, ex, ey, direction
    if mapl[ey][ex] == 'lur' :       # When Meet SAMBARI starting point
        left1('deepskyblue')
        up1('deepskyblue')
        right1('deepskyblue')
        if direction == 'r' :
            upArrow(ex, ey)
            rightArrow(ex, ey)
            sambari('u', 'r')
        elif direction == 'd' :
            leftArrow(ex, ey)
            rightArrow(ex, ey)
            sambari('l', 'r')
        elif direction == 'l' :
            leftArrow(ex, ey)
            upArrow(ex, ey)
            sambari('l', 'u')
    if mapl[ey][ex] == 'urd' :
        up1('deepskyblue')
        right1('deepskyblue')
        down1('deepskyblue')
        if direction == 'u' :
            upArrow(ex, ey)
            rightArrow(ex, ey)
            sambari('u', 'r')
        elif direction == 'd' :
            downArrow(ex, ey)
            rightArrow(ex, ey)
            sambari('d', 'r')
        elif direction == 'l' :
            upArrow(ex, ey)
            downArrow(ex, ey)
            sambari('u', 'd')
    if mapl[ey][ex] == 'ldr' :
        left1('deepskyblue')
        down1('deepskyblue')
        right1('deepskyblue')
        if direction == 'r' :
            downArrow(ex, ey)
            rightArrow(ex, ey)
            sambari('d', 'r')
        elif direction == 'u' :
            leftArrow(ex, ey)
            rightArrow(ex, ey)
            sambari('l', 'r')
        elif direction == 'l' :
            leftArrow(ex, ey)
            downArrow(ex, ey)
            sambari('l', 'd')
    if mapl[ey][ex] == 'uld' :
        up1('deepskyblue')
        left1('deepskyblue')
        down1('deepskyblue')
        if direction == 'u' :
            upArrow(ex, ey)
            leftArrow(ex, ey)
            sambari('u', 'l')
        elif direction == 'd' :
            downArrow(ex, ey)
            leftArrow(ex, ey)
            sambari('d', 'l')
        elif direction == 'r' :
            upArrow(ex, ey)
            downArrow(ex, ey)
            sambari('u', 'd')
# [만나는삼바리화살표]
# mannaneunsambarihwasalpyow


            
def sambari(dir1, dir2):
    global direction, sambariEnd, resistors, ex, ey
    assert len(mapl[ey][ex]) == 3
    
    print("삼발이실행", end='\t')
    printcurlocation()
    
    만나는삼발이를만난방향들 = []
    sambari_x, sambari_y = ex, ey

    print(f"삼발이에서 <{dir1}> 방향으로 이동", end='\t')
    printcurlocation()
    만나는삼발이를만날때까지전선타고이동(dir1, 만나는삼발이를만난방향들)

    print(f"삼발이에서 다시 <{dir2}> 방향으로 이동", end='\t')
    printcurlocation()
    ex, ey = sambari_x, sambari_y
    만나는삼발이를만날때까지전선타고이동(dir2, 만나는삼발이를만난방향들)

    print("삼발이 이동종료")


    def 만나는삼발이화살표():
        match direction:
            case 'u':
                upArrow(ex, ey)
            case 'd':
                downArrow(ex, ey)
            case 'r':
                rightArrow(ex, ey)
            case 'l':
                leftArrow(ex, ey)

    def 만나는삼발이색칠(삼발이도선방향):
        match 삼발이도선방향:
            case 'u':
                up1('deepskyblue')
            case 'd':
                down1('deepskyblue')
            case 'r':
                right1('deepskyblue')
            case 'l':
                left1('deepskyblue')

    만나는삼발이를만난방향들 = list(map(lambda x: {'d': 'u', 'u': 'd', 'r': 'l', 'l': 'r'}[x], 
                                만나는삼발이를만난방향들))
    만나는삼발이 = mapl[ey][ex]
    for 만나는삼발이가향하는방향 in 만나는삼발이[:3]:
        #print(만나는삼발이가향하는방향, 만나는삼발이, 만나는삼발이를만난방향들)
        만나는삼발이색칠(만나는삼발이가향하는방향)
        if 만나는삼발이가향하는방향 not in 만나는삼발이를만난방향들:
            #print(f"방향을 {direction}으로 결정")
            direction = 만나는삼발이가향하는방향
    만나는삼발이화살표()
    
    printcurlocation()
    if direction == 'u': ey -= 1
    elif direction == 'd': ey += 1
    elif direction == 'l': ex -= 1
    elif direction == 'r': ex += 1
    printcurlocation()


def 만나는삼발이를만날때까지전선타고이동(dir, 만나는삼발이를만난방향들):
    global direction, sambariEnd, resistors, ex, ey
    printcurlocation()
    print(f"만삼만전 실행")
    direction = dir
    if direction == 'u': ey -= 1
    elif direction == 'd': ey += 1
    elif direction == 'l': ex -= 1
    elif direction == 'r': ex += 1
    else: raise Exception("미친놈아!!")

    printcurlocation()
    tmp1, tmp2 = [], []
    while mapl[ey][ex][-1] != '.': #```만나는``` 삼발이를 ```만나는``` 상황까지반복
        전선을만났을때이동()
        저항을만났을때이동(tmp1, tmp2)
        #printcurlocation()

    print("만나는삼발이도달")
    만나는삼발이를만난방향들.append(direction)
    resistors.append(tmp1)
    resistorLocation.append(tmp2)
    #print(resistors, resistorLocation, 만나는삼발이를만난방향들)



def get_resistor_value(x, y):
    global resistors, mapl, Rvalues
    Rvalues = [R1spinbox.get(),
               R2spinbox.get(),
               R3spinbox.get(),
               R4spinbox.get(),
               R5spinbox.get(),
               R6spinbox.get()]
    Rvalues = list(map(int, Rvalues))

    print(f"Rvalues를 {Rvalues}로 초기화합니다")
    print(f"({x}, {y}) 위치의 {mapl[y][x]}에서 저항 값을 받아오기를 시도합니다")
    if (n := mapl[y][x][-1]) not in '123456':
        raise Exception(f"({x}, {y}) 위치의 {mapl[y][x]}에 저항 값이 설정되어 있지 않습니다람쥐...")
    print(f"({x}, {y}) 위치의 {mapl[y][x]}의 저항 값: {Rvalues[int(n)-1]}")
    return Rvalues[int(n)-1]

def resistorCalculation():
    global resistors, electricCurrent, totalResist
    totalResist=0
    tempTotalResist1=0
    tempTotalResist2=0
    doThis=True
    for i in range(len(resistors)) :
        if type(resistors[i]) == int and doThis==True:
            totalResist += resistors[i]
        elif type(resistors[i]) == list and doThis==True :
            for j in range(len(resistors[i])) :
                tempTotalResist1+=resistors[i][j]
            for k in range(len(resistors[i+1])) :
                tempTotalResist2+=resistors[i+1][k]
            doThis=False
            totalResist += (tempTotalResist1*tempTotalResist2) / (tempTotalResist2+tempTotalResist1)
            tempTotalResist1=0
            tempTotalResist2=0
        elif doThis==False:
            doThis=True
    electricCurrent = battery_value / totalResist   # I = V / R

def deep_len(arr: list[list[int] | int]):
    cnt = 0
    for i in arr:
        if type(i) == int:
            cnt += 1
        else:
            cnt += len(i)
            
    return cnt


def electricCurrentCalculation() -> list[list[int] | int]:
    global resistors, totalResist, electricCurrent, resistorLocation, finalResult
    finalResult=[[None for _ in range(20)] for _ in range(20)]   #[r, v, i, p] 20*20

    skipNext = False
    for k in range(len(resistors)):
        if skipNext:
            skipNext = False
            continue

        if type(resistors[k]) == int:
            skipNext = False
            x, y = resistorLocation[k]
            r = resistors[k]
            i = electricCurrent
            v = i * r
            p = v * i
            finalResult[y][x] = [r, v, i, p]
            
        elif type(resistors[k]) == list:
            skipNext = True

            wire1, wire2 = resistors[k], resistors[k+1]
            wire1R, wire2R = map(sum, (wire1, wire2))
            wire1I, wire2I = map(lambda x: electricCurrent * x / (wire1R + wire2R), (wire2R, wire1R))

            for j in range(len(wire1)):
                x, y = resistorLocation[k][j]
                r = resistors[k][j]
                i = wire1I
                v = i * r
                p = v * i
                finalResult[y][x] = [r, i, v, p]

            for j in range(len(wire2)):
                x, y = resistorLocation[k+1][j]   #genius
                r = resistors[k+1][j]
                i = wire2I
                v = i * r
                p = v * i
                finalResult[y][x] = [r, i, v, p]
            

    #print(f"final result generated: \n{finalResult}")
    

def setresistance(self):
    explanationresistance.config(text = '저항 값을 선택')
    if self == '':
        return True
    
    valid = False
    
    if self.isdigit():
        if (int(self) >= 0 and int(self) <= 100):
            valid = True
    return valid

def errorsetresistance(self):
        unknowntext = str(self) + ' is invalid value \n valid value: 0~100'  #  위쪽에 정의되지 않은 키 입력들을 unknowntext로 간주, <입력된 키값, 'is not a valid key'>로써 나타냄
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

def setbattery(self):
    explanationbattery.config(text = '|전지 값을 선택|& \n |입력 도움 박스|')
    if self == '':
        return True
    
    valid = False
    
    if self.isdigit():
        if (int(self) >= 0 and int(self) <= 100):
            valid = True
    return valid

def errorsetbattery(self):
        unknowntext = str(self) + ' is invalid value \n valid value: 0~100'  #  위쪽에 정의되지 않은 키 입력들을 unknowntext로 간주, <입력된 키값, 'is not a valid key'>로써 나타냄
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

Button(ui, text = "OPERATE[o]", command = OPERATE).place(x = 190, y= 350, width = 100, height = 40)

# Button(ui, text = "RUN[r]", command = amugeona).place(x = 190, y= 350, width = 100, height = 40)

Button(ui, text = "WIRE[w]", command = MAKE_WIRE_LR).place(x = 30, y= 400, width = 80, height = 40)

# >> [Noreok]

# Resistance = [r+1 for r in range(0)]

# R1 = ttk.Combobox(inputjeo1, width = 10, height = 10, values = Resistance)
# R1.pack(padx=4)
# R1.set("첫 번째 저항 값 설정") 대충 이거 쓰는 것 보다 훨씬 좋은거 찾았다는 내용~

# I will make a MenuBar and Menu fuction

# 저항값 설정
explanationresistance = Label(inputjeo1, text = "▼저항값을 선택▼", height = 3)
explanationresistance.pack(padx=4)
#어쩔얼른코딩하셈ㅅㄱ
validate_command = (inputjeo1.register(setresistance), '%P')
invalid_command = (inputjeo1.register(errorsetresistance), '%P')

# for m in range(0, 11):
#     globals()['spinbox'{}.format(m)] = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
    
    # m.pack(padx=4)

R1spinbox = Spinbox(inputjeo1, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R1spinbox.pack(padx=4) 
R2spinbox = Spinbox(inputjeo1, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R2spinbox.pack(padx=4) 
R3spinbox = Spinbox(inputjeo1, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R3spinbox.pack(padx=4) 
R4spinbox = Spinbox(inputjeo1, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R4spinbox.pack(padx=4) 
R5spinbox = Spinbox(inputjeo1, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R5spinbox.pack(padx=4) 
R6spinbox = Spinbox(inputjeo1, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
R6spinbox.pack(padx=4) 


Rvalues = [R1spinbox.get(),
           R2spinbox.get(),
           R3spinbox.get(),
           R4spinbox.get(),
           R5spinbox.get(),
           R6spinbox.get()]
finalResult = []

# R7spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
# R7spinbox.pack(padx=4)
# R8spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
# R8spinbox.pack(padx=4)
# R9spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
# R9spinbox.pack(padx=4)
# R10spinbox = Spinbox(inputjeo1, width=10, from_=0, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command)
# R10spinbox.pack(padx=4)
# 그 더 좋은 방법은 하드코딩을 말하는 것입니다!!  하하하하....

# 전지의 전압 설정
explanationbattery = Label(inputjeo2, text = "▼전지 값을 선택▼", height = 3)
explanationbattery.pack(padx=4)

validate_command = (inputjeo2.register(setbattery), '%P')
invalid_command = (inputjeo2.register(errorsetbattery), '%P')


resultDisplay = Label(inputjeo3, text="nice")
resultDisplay.pack(anchor='n')


# 안되면 말좀
def update_variable(*args):
    global battery_value
    battery_value = battery_spinbox_var.get()

battery_spinbox_var = IntVar()

batteryspinbox = Spinbox(inputjeo2, width=10, from_=1, to=100, validate = 'all', validatecommand=validate_command, invalidcommand=invalid_command, textvariable=battery_spinbox_var)
batteryspinbox.pack(padx=4) 

battery_spinbox_var.trace('w', update_variable)
battery_value = battery_spinbox_var.get()



def BATTERYVALUECHECK(self):
    explanationbattery.config(text='')
    if self == '':
        return True
    
    
    valid = False
    if self.isdigit():
        if (int(self) != 0):
            valid = True
    return valid

def BATTERTYVALUEERROR():
    explanationbattery.config(text="0 is not valid value")



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

menu2.add_radiobutton(label = "Undo", state = "disable") # 미안한데 작동 안돼
menu2.add_radiobutton(label = "Redo") # 미안한데 작동 안돼
menu2.add_radiobutton(label = "Cut") # 미안한데 작동 안돼
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

#     tk.after(1000, whiletrue)

# tk.after(1000, whiletrue)

tk.mainloop()    #i like thi