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


userx = 0
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






class Point():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def isinarea(self, topleft: "Point", bottomright: "Point") -> bool: #inclusive
        xinrange = topleft.x <= self.x <= bottomright.x
        yinrange = topleft.y <= self.y <= bottomright.y

        return xinrange and yinrange
    
# 크아악 모르겠다 << ㅋㅋ허접

class ElectricityParts():
    def __init__(self, position: Point, directions: str) -> None: 
        assert all(map(lambda x: x in 'udlr', directions)),\
            "directions는 u, d, l, r만으로 이루어진 문자열이여야 합니다"
        assert len(set(directions)) == len(directions),\
            "directions에는 중복된 문자가 없어야 합니다"
        
        self.position = position
        self.directions = list(directions)

    def rotateCW(self) -> None:
        change = {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
        self.directions = list(map(lambda x: change[x], self.directions))

    def isdirected(self, directions: str) -> bool:
        return set(self.directions) == set(directions)
     
    def next_position(self, input_direction: str) -> list[Point]:
        output_directions = self.directions.copy()
        output_directions.remove(input_direction)

        output_positions = []
        for direction in output_directions:
            x, y = self.position.x, self.position.y
            match direction:
                case 'u': y -= 1
                case 'd': y += 1
                case 'l': x -= 1
                case 'r': x += 1
            output_positions.append(Point(x, y))
        
        return output_positions

'''testE = ElectricityParts(Point(1, 1), 'lr')
print(testE.directions)
testE.rotateCW()
print(testE.directions)
input()'''

class Wire(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)

    def draw(self, color: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        
        if 'l' in self.directions():
            display.create_line(x, y+15, x+15, y+15, fill=color)

        if 'r' in self.directions():
            display.create_line(x+30, y+15, x+15, y+15, fill=color)
        
        if 'u' in self.directions():
            display.create_line(x+15, y+15, x+15, y, fill=color)

        if 'd' in self.directions():
            display.create_line(x+15, y+15, x+15, y+30, fill=color)

class Resistor(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)

    def draw(self, linecolor: str='black', spikecolor: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        if self.isdirected('lr'):
            display.create_line(x, y+15, x+3, y+15, fill=linecolor)
            display.create_line(x+3, y+15, x+5, y+25, fill=spikecolor)
            display.create_line(x+5, y+25, x+9, y+5, fill=spikecolor)
            display.create_line(x+9, y+5, x+13, y+25, fill=spikecolor)
            display.create_line(x+13, y+25, x+17, y+5, fill=spikecolor)
            display.create_line(x+17, y+5, x+21, y+25, fill=spikecolor)
            display.create_line(x+21, y+25, x+25, y+5, fill=spikecolor)
            display.create_line(x+25, y+5, x+27, y+15, fill=spikecolor)
            display.create_line(x+27, y+15, x+30, y+15, fill=linecolor)

        elif self.isdirected('ud'):
            display.create_line(x+15, y, x+15, y+3, fill=linecolor)
            display.create_line(x+15, y+3, x+25, y+5, fill=spikecolor)
            display.create_line(x+25, y+5, x+5, y+9, fill=spikecolor)
            display.create_line(x+5, y+9, x+25, y+13, fill=spikecolor)
            display.create_line(x+25, y+13, x+5, y+17, fill=spikecolor)
            display.create_line(x+5, y+17, x+25, y+21, fill=spikecolor)
            display.create_line(x+25, y+21, x+5, y+25, fill=spikecolor)
            display.create_line(x+5, y+25, x+15, y+27, fill=spikecolor)
            display.create_line(x+15, y+27, x+15, y+30, fill=linecolor)
        
class Battery(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)

    def draw(self) -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        display.create_line(x, y+15, x+11, y+15)
        display.create_line(x+11, y+25, x+11, y+5)
        display.create_line(x+19, y+20, x+19, y+11, width=3)
        display.create_line(x+19, y+15, x+30, y+15)
        

class Diode(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)

    def isdirected(self, directions: str) -> bool:
        return self.directions == list(directions)

    def draw(self, color: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        
        if self.isdirected('lr'):
            display.create_line(x, y+15, x+30, y+15, fill=color)
            display.create_polygon(x+5, y+5, x+5, y+25, x+25, y+15)
            display.create_line(x+25, y+5, x+25, y+25, width=2)

        elif self.isdirected('ud'):
            display.create_line(x+15, y, x+15, y+30, fill=color)
            display.create_polygon(x+5, y+5, x+25, x+5, x+15, y+25)
            display.create_line(x+5, y+25, x+25, y+25, width=2)

        elif self.isdirected('rl'):
            display.create_line(x, y+15, x+30, y+15, fill=color)
            display.create_polygon(x+25, y+5, x+25, y+25, x+5, y+15)
            display.create_line(x+5, y+5, x+5, y+25, width=2)

        elif self.isdirected('du'):
            display.create_line(x+15, y, x+15, y+30, fill=color)
            display.create_polygon(x+5, y+25, x+25, y+25, x+15, y+5)
            display.create_line(x+5, y+5, x+25, y+5, width=2)


class Board():
    def __init__(self, xsize: int, ysize: int) -> None:
        self.xsize = xsize
        self.ysize = ysize
        self.__mapl = [[None]*xsize for _ in range(ysize)]
        
    def get_part(self, position: Point) -> ElectricityParts:
        obj = self.__mapl[position.x][position.y]
        assert obj != None, f"{position}에 객체가 존재하지 않습니다"
        assert isinstance(obj, ElectricityParts), "{position}에 존재하는 객체가 전기 부품이 아닙니다"

        return obj
    
    def put_part(self, obj: ElectricityParts, position: Point) -> None:
        self.__mapl[position.x][position.y] = obj

    def remove_part(self, position: Point) -> None:
        self.__mapl[position.x][position.y] = None


class Cursor():
    def __init__(self) -> None:
        self.position = Point(0, 0)


    def __make_rectangle(self, color: str='red') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        display.create_rectangle(x, y, x+30, y+30, outline=color)

    def highlight(self) -> None:
        self.__make_rectangle(color='red')

    def dehighlight(self) -> None:
        
    
        



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

def MAKE_VOID():
    global mapl, userx, usery
    mapl[usery][userx] = ''

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
        #amugeona()
        print("전지 도달")
        #print(f"저항 리스트: {resistors}")
        #print(batteryspinbox)
        afteroperate=True

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

display.bind_all('<KeyPress>', keypressed)

#-------------------------------------------------------------------------Menu-------------------------------------------------------------------------


    display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30,outline='gray', fill='whitesmoke')

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














Button(ui, text = "UP[↑]", command = GO_UP).place(x = 110, y = 50, width = 80, height = 80)  #make 이동 ui

Button(ui, text = "LEFT[←]", command = GO_LEFT).place(x = 30, y = 130, width = 80, height = 80)

Button(ui, text = "RIGHT[→]", command = GO_RIGHT).place(x = 190, y = 130, width = 80, height = 80)

Button(ui, text = "DOWN[↓]", command = GO_DOWN).place(x = 110, y = 210, width = 80, height = 80)

Button(ui, text = 'EXIT[Esc]', command = closewarn).place(x = 120 , y = 500, width = 60, height = 60)

Button(ui, text = "CLEAR[Enter]", command = tempwarn).place(x = 190, y= 400, width = 80, height = 40)

Button(ui, text = "OPERATE[o]", command = OPERATE).place(x = 190, y= 350, width = 100, height = 40)

# Button(ui, text = "RUN[r]", command = amugeona).place(x = 190, y= 350, width = 100, height = 40)

Button(ui, text = "WIRE[w]", command = MAKE_WIRE_LR).place(x = 30, y= 400, width = 80, height = 40)


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