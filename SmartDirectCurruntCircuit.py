from tkinter import *          #i like tkinter
import tkinter.font
import time
tk = Tk()

tk.title('DCCOMICStm')           # 회로를 구현할 장(張) 만들기
tk.geometry("1150x600+0+0")
tk.resizable(False,False)

inputjeo1=Frame(tk, relief = "solid", width = 150, height = 250)    #divide window
inputjeo1.place(x=0, y=0)
inputjeo2=Frame(tk, relief = "solid", width = 146, height = 250)
inputjeo2.place(x=150, y=0)
inputjeo3=Frame(tk, relief = "solid", width = 300, height = 350)
inputjeo3.place(x=0, y=250)

dp=Frame(tk, relief = "solid", bd = 2, width = 600, height = 600)
dp.place(x = 296, y = 0)
ui=Frame(tk, relief = "solid", width = 250, height = 600)
ui.place(x = 900, y = 0)


display = Canvas(dp, bd=0, bg='whitesmoke')             #make display(canvas) Disupulayee Saing Seong
display.place(x = 0, y = 0, width = 600, height = 600)
Yukari='red'


class Point(): #location = Point(0, 0)
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def isinarea(self, topleft: "Point", bottomright: "Point") -> bool: #range
        xinrange = topleft.x <= self.x < bottomright.x
        yinrange = topleft.y <= self.y < bottomright.y

        return xinrange and yinrange
    
    def isinboard(self) -> bool:
        return self.isinarea(Point(0, 0), Point(board.xsize, board.ysize))


class ElectricityParts():
    def __init__(self, position: Point, directions: str) -> None: 
        assert all(map(lambda x: x in 'udlr', directions)),\
            "directions는 u, d, l, r만으로 이루어진 문자열이여야 합니다"
        assert len(set(directions)) == len(directions),\
            "directions에는 중복된 문자가 없어야 합니다"
        
        self.position = position
        self.directions = list(directions)
        board.put_part(self, self.position)
        self._draw()

        add_log(f"generated {self}")


    def _draw(self) -> None:
        raise AttributeError("ElectricityParts의 draw메소드는 반드시 오버라이드되어야 합니다\n"
            "지금 카사네 테토의 오버라이드 들으러 가기 >>> https://www.youtube.com/watch?v=LLjfal8jCYI")

    def show_status(self) -> None:
        '''이곳에 기구의 현재 상태를 표시'''


    def rotate_CW(self) -> None:
        board.erase(self.position)

        change = {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
        self.directions = list(map(lambda x: change[x], self.directions))
        self._draw()

    def isdirected(self, directions: str) -> bool:
        return set(self.directions) == set(directions)
    
    def next_positions(self, input_direction: str) -> list[Point]:
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

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} on {self.position}'

    def __del__(self) -> None:
        add_log(f'deleted {self}')


class Wire(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)

    def _draw(self, color: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        
        if 'l' in self.directions:
            display.create_line(x, y+15, x+16, y+15, fill=color)

        if 'r' in self.directions:
            display.create_line(x+30, y+15, x+15, y+15, fill=color)
        
        if 'u' in self.directions:
            display.create_line(x+15, y+15, x+15, y, fill=color)

        if 'd' in self.directions:
            display.create_line(x+15, y+15, x+15, y+30, fill=color)


class Resistor(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)
        self.__voltage = -1
        self.__current = -1
        self.__resistance = -1 # 레지스탕스 히다리 에이 미기 비

# name > 접근 제어자: Public, 모든 외부 접근 허용
# _name > 접근 제어자: Protected, 자기 클래스, 자식 클래스 접근 허용
# __name > 접근 제어자: Private, 자기 클래스 접근 허용


    def _draw(self, linecolor: str='black', spikecolor: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        font=tkinter.font.Font(family='그래픽', size=10, slant='roman', weight='bold')
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
            # display.create_text(x+23, y+23, text="83", font=font, fill='red')

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
            # display.create_text(x+23, y+23, text="83", font=font, fill='red')
        

class Battery(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)
        self.plus_direction = directions[0]
        self.minus_direction = directions[1]

    def next_positions(self) -> list[Point]:
        x, y = self.position.x, self.position.y
        match self.plus_direction:
            case 'u': y -= 1
            case 'd': y += 1
            case 'l': x -= 1
            case 'r': x += 1
        
        return [Point(x, y)]

    def isdirected(self, directions: str) -> bool:
        return self.directions == list(directions)

    def _draw(self, plus: str='black', minus: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP

        if self.isdirected('lr'):
            display.create_line(x, y+15, x+11, y+15, fill=plus)
            display.create_line(x+11, y+25, x+11, y+5)
            display.create_line(x+19, y+20, x+19, y+11, width=3)
            display.create_line(x+19, y+15, x+30, y+15, fill=minus)
        
        elif self.isdirected('ud'):
            display.create_line(x+15, y, x+15, y+11, fill=plus)
            display.create_line(x+5, y+11, x+25, y+11)
            display.create_line(x+10, y+19, x+19, y+19, width=3)
            display.create_line(x+15, y+19, x+15, y+30, fill=minus) 

        elif self.isdirected('rl'):
            display.create_line(x+30, y+15, x+19, y+15, fill=plus)
            display.create_line(x+19, y+5, x+19, y+25)
            display.create_line(x+11, y+10, x+11, y+19, width=3)
            display.create_line(x+11, y+15, x, y+15, fill=minus)

        elif self.isdirected('du'):
            display.create_line(x+15, y+30, x+15, y+19, fill=plus)
            display.create_line(x+25, y+19, x+5, y+19)
            display.create_line(x+20, y+11, x+11, y+11, width=3)
            display.create_line(x+15, y+11, x+15, y, fill=minus)
        

class Diode(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)
        self.input_direction = self.directions[0]
        self.output_direction = self.directions[1]

    def isdirected(self, directions: str) -> bool:
        return self.directions == list(directions)

    def next_positions(self, input_direction: str) -> list[Point|None]:
        if input_direction != self.input_direction:
            return [None]
        x, y = self.position.x, self.position.y
        match self.output_direction:
            case 'u': y += 1
            case 'd': y -= 1
            case 'l': x += 1
            case 'r': x -= 1
        
        return [Point(x, y)]

    def _draw(self, inputcolor: str='black', outputcolor: str='black') -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        
        if self.isdirected('lr'):
            display.create_line(x, y+15, x+5, y+15, fill=inputcolor)
            display.create_line(x+25, y+15, x+30, y+15, fill=outputcolor)
            display.create_polygon(x+5, y+5, x+5, y+25, x+25, y+15)
            display.create_line(x+25, y+5, x+25, y+25, width=2)

        elif self.isdirected('ud'):
            display.create_line(x+15, y, x+15, y+5, fill=inputcolor)
            display.create_line(x+15, y+25, x+15, y+30, fill=outputcolor)
            display.create_polygon(x+5, y+5, x+25, y+5, x+15, y+25)
            display.create_line(x+5, y+25, x+25, y+25, width=2)

        elif self.isdirected('rl'):
            display.create_line(x+25, y+15, x+30, y+15, fill=inputcolor)
            display.create_line(x, y+15, x+5, y+15, fill=outputcolor)
            display.create_polygon(x+25, y+5, x+25, y+25, x+5, y+15)
            display.create_line(x+5, y+5, x+5, y+25, width=2)


        elif self.isdirected('du'):
            display.create_line(x+15, y+25, x+15, y+30, fill=inputcolor)
            display.create_line(x+15, y, x+15, y+5, fill=outputcolor)
            display.create_polygon(x+5, y+25, x+25, y+25, x+15, y+5)
            display.create_line(x+5, y+5, x+25, y+5, width=2)



class Board():
    def __init__(self, xsize: int, ysize: int) -> None:
        self.xsize = xsize
        self.ysize = ysize
        self.__mapl = [[None]*self.xsize for _ in range(self.ysize)]
        
    def get_part(self, position: Point) -> ElectricityParts: # 값 없으면 오류발생
        obj = self.__mapl[position.x][position.y]
        if obj == None:
            raise AttributeError(f"{position}에 객체가 존재하지 않습니다")
        elif not isinstance(obj, ElectricityParts):
            raise TypeError(f"{position}에 존재하는 객체가 전기 부품이 아닙니다")
        
        return obj
    
    def try_get_part(self, position: Point) -> ElectricityParts: # 값 없으면 None 반환
        return self.__mapl[position.x][position.y]
    
    def put_part(self, obj: ElectricityParts, position: Point) -> None:
        self.remove_part(position)
        self.__mapl[position.x][position.y] = obj

    def remove_part(self, position: Point) -> None:
        try:
            part = self.try_get_part(position)
            del part
            self.__mapl[position.x][position.y] = None
            self.erase(position)
        except:
            add_log(f'no ElectricityPart on {position}')

    def rotate_part(self, position: Point) -> None:
        try:
            part = self.get_part(position)
            part.rotate_CW()
            add_log(f'rotated {part}')
        except:
            add_log(f'no ElectircityPart on {position}')
        
    def clear(self) -> None:
        for x in range(self.xsize):
            for y in range(self.ysize):
                self.remove_part(Point(x, y))

    def erase(self, position: Point) -> None:
        PROP = 30
        x = position.x*PROP
        y = position.y*PROP
        display.create_rectangle(x, y, x+30, y+30,outline='gray', fill='whitesmoke')
        cursor.highlight()

    def isblank(self, position: Point) -> bool:
        return self.try_get_part(position) == None


class Cursor():
    def __init__(self) -> None:
        self.position = Point(0, 0)
        self.Yukari = 'red'
        self.highlight()

    def go_left(self) -> None:
        self.__move_cursor(-1, 0)

    def go_right(self) -> None:
        self.__move_cursor(1, 0)

    def go_up(self) -> None:
        self.__move_cursor(0, -1)

    def go_down(self) -> None:
        self.__move_cursor(0, 1)

    def go_upleft(self) -> None:
        self.__move_cursor(-1, -1)

    def go_upright(self) -> None:
        self.__move_cursor(1, -1)

    def go_downleft(self) -> None:
        self.__move_cursor(-1, 1)

    def go_downright(self) -> None:
        self.__move_cursor(1, 1)

    def toggle(self) -> None:
        if self.highlighted:
            self.dehighlight()
        else:
            self.highlight()

    def KadenokoujiYukari(self):
        if self.Yukari == 'red':
            self.Yukari='blue'
        elif self.Yukari == 'blue':
            self.Yukari='green'
        elif self.Yukari == 'green':
            self.Yukari='gray'
        elif self.Yukari == 'gray':
            self.Yukari='red'
        self.__draw_rectangle(color=self.Yukari)

    def highlight(self) -> None: 
        self.highlighted = True
        self.__draw_rectangle(color=self.Yukari)
        part = board.try_get_part(self.position)
        if isinstance(part, ElectricityParts):
            part.show_status()

    def dehighlight(self) -> None:
        self.highlighted = False
        self.__draw_rectangle(color='grey')
        
    def __draw_rectangle(self, color:str) -> None:
        PROP = 30
        x = self.position.x*PROP
        y = self.position.y*PROP
        display.create_rectangle(x, y, x+30, y+30, outline=color)


    def __move_cursor(self, dx: int, dy: int) -> None:
        new_pos = Point(self.position.x+dx, self.position.y+dy)
        if not new_pos.isinboard():
            new_pos = Point((new_pos.x+board.xsize)%board.xsize,
                            (new_pos.y+board.ysize)%board.ysize)
        self.dehighlight()
        self.position = new_pos
        self.highlight()



class CursorAction:
    def generate_wire_line(self, dir: str='lr'):
        Wire(cursor.position, dir)

    def generate_wire_curved(self, dir: str='ru'):
        Wire(cursor.position, dir)

    def generage_wire_Tshape(self, dir: str='lur'):
        Wire(cursor.position, dir)

    def generate_diode(self, dir: str='lr'):
        Diode(cursor.position, dir)

    def generate_resistor(self, dir: str='lr'):
        Resistor(cursor.position, dir)

    def generate_battery(self, dir: str='lr'):
        Battery(cursor.position, dir)

    def remove_part(self):
        board.remove_part(cursor.position)

    def rotate_part(self):
        board.rotate_part(cursor.position)


class CurrentManager:
    ...


board = Board(20, 20) # ↘일과 열의 관계 左下向
cursor = Cursor()
cursor_action = CursorAction()

def draw_window():
    display.delete('all')
    for i in range(20):                                          #draw display
        display.create_line(30*i, 0, 30*i, 600, fill = "gray")
    for i in range(20):
        display.create_line(0, 30*i, 600, 30*i, fill = "gray")
    # for i in range(4):
    #     display.create_line(0, 150*i, 600, 150*i, fill = "black")
    # for i in range(4):
    #     display.create_line(150*i, 0, 150*i, 600, fill = "black")            asdfasdfasdfasdfasdfasfd

draw_window()



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


def get_resistor_value(x, y):
    global resistors, mapl, Rvalues
    Rvalues = [# R1spinbox.get(),
               # R2spinbox.get(),
               # R3spinbox.get(),
               # R4spinbox.get(),
               # R5spinbox.get(),
               # R6spinbox.get()
               ]
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

def keypressed(event):        #when keypressed ~~

    if event.keysym == 'a' :
        add_log('a')

    elif event.keysym == 'Up' :
        cursor.go_up()

    elif event.keysym == 'Left' :
        cursor.go_left()

    elif event.keysym == 'Down' :
        cursor.go_down()

    elif event.keysym == 'Right' :
        cursor.go_right()

    elif event.keysym == 'Return' :
        tempwarn()

    elif event.keysym == 'Escape' :
        closewarn()

    elif event.keysym == 'space' : # 회전
        cursor_action.rotate_part()

    elif event.keysym == 'm' : # 'ㅡ'or'ㅣ'자
        cursor_action.generate_wire_line(dir='lr')

    elif event.keysym == 'l' :
        cursor_action.generate_wire_line(dir='ud')

    elif event.keysym == 's' : # 'ㄴ'자
        cursor_action.generate_wire_curved(dir='ru')

    elif event.keysym == 'n' : # 갈라지는 삼발이:"ㅡ"계열. 'ㅜ'자
        cursor_action.generage_wire_Tshape(dir='lrd')

    elif event.keysym == 'h' : # 갈라지는 삼발이:"ㅡ"계열. 'ㅗ'자
        cursor_action.generage_wire_Tshape(dir='lru')

    elif event.keysym == 'j': # 만나는 삼발이: "ㅣ"계열. 'ㅓ'자
        cursor_action.generage_wire_Tshape(dir='udl')

    elif event.keysym == 'k': # 만나는 삼발이: "ㅣ"계열. 'ㅏ'자
        cursor_action.generage_wire_Tshape(dir='udr')

    # elif event.keysym == 'equal' : # '+'자 lrud
    #     MAKE_WIRE_LRUD()

    elif event.keysym == 'b' : # 밧데리
        cursor_action.generate_battery(dir='lr')

    elif event.keysym == 'r' : # 저항
        cursor_action.generate_resistor(dir='lr')

    elif event.keysym == 'e' : # erase
        cursor_action.remove_part() # 클래스 내부에서 사용: self.position | 클래스 외부에서 사용: cursor.position

    elif event.keysym == 'd' : # diode
        cursor_action.generate_diode(dir='lr')

    # elif event.keysym == '1' :
    #     SELECT_RESISTANCE1()

    # elif event.keysym == '2' :
    #     SELECT_RESISTANCE2()

    # elif event.keysym == '3' :
    #     SELECT_RESISTANCE3()

    # elif event.keysym == '4' :
    #     SELECT_RESISTANCE4()

    # elif event.keysym == '5' :
    #     SELECT_RESISTANCE5()

    # elif event.keysym == '6' :
    #     SELECT_RESISTANCE6()

    elif event.keysym == 'o' :
        OPERATE()

    # elif event.keysym == 'g':
    #     print(battery_value)

    # 당신의 아무거나. 스타트로 대체되다. 불만 있습니까? Korean Heroes? !!!!!!!

    # elif event.keysym == 'r' : # start(run) module
    #     amugeona()

    else:                     #Lee Sang Han Button Press >>> 비정의 커맨드 경고 창
        unknowntext = event.keysym,'is not a valid key'  #  위쪽에 정의되지 않은 키 입력들을 unknowntext로 간주, <입력된 키값, 'is not a valid key'>로써 나타냄
        toplevel = Toplevel(tk)
        toplevel.geometry("320x200+820+100")
        toplevel.resizable(False, False)
        toplevel.title("ERROR: not a valid key")  # 창 이름
        label = Label(toplevel, text = unknowntext, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "error", compound = "top")  #  unknowntext출력, i마크 표시(붉은색) 할 창 생성
        label.pack()

        button = Button(toplevel, width = 10, text = "ok", overrelief = "solid", command = toplevel.destroy)  #  ok버튼 누르면 경고 창 삭제
        button.pack()


def clear():           # 19   clear the window
    global userx, usery, mapl

    cursor.dehighlight()
    userx = 0
    usery = 0
    cursor.highlight()
# 딸피코드 ok
    board.clear()
    # for musaku in range(1, 20):
    #     for misaku in range(20):
    #         mapl[misaku][musaku] = ''

    draw_window()


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
        display.create_rectangle(userx*30, usery*30, userx*30+30, usery*30+30,outline='gray', fill='whitesmoke')

display.bind_all('<KeyPress>', keypressed)

def temp():            # 00   clear()와 경고 창 삭제를 동시에
    global areyouokaytoclear
    board.clear()
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
    AYOE = "DirectCurrent Circuit Help \n Commands \n \n \n [m(ㅡ)] > [fill 'ㅡ'wire] \n [l(ㅣ)] > [fill 'ㅣ'wire] \n \n derived from 'ㅡ' is fill Current Distribution wire \n [n(ㅜ)] > [fill 'ㅜ'wire] \n [h(ㅗ)] > [fill 'ㅗ'wire] \n \n derived from 'ㅣ' is fill Current Collecting wire \n [j(ㅓ)] > [fill 'ㅓ'wire] \n [k(ㅏ)] > [fill 'ㅏ'wire] \n \n [s(ㄴ)] > [fill 'ㄴ'wire] \n [b] > [set battery]  \n [r] > [set resistance]  \n [space] > [rotate wire] \n [Esc] > [Exit] \n [Enter] > [Clear] \n [e] > [Erase] \n [o] > [Operate] "
    LCHelp = Toplevel(tk)
    LCHelp.geometry("320x520+820+100")
    LCHelp.resizable(False, False)
    LCHelp.title("DirectCurrent Circuit Help")
    lclabel = Label(LCHelp, text = AYOE, width = 300, height = 470, fg = "gold4", relief = "solid", bitmap = "info", compound = "top")
    lclabel.pack()
    lcbutton = Button(LCHelp, width = 10, text = "close", overrelief = "solid", command = LCHelp.destroy)
    lcbutton.pack()

# def showlist():
#     global mapl
#     Showlist = Toplevel(tk)
#     Showlist.geometry("8000x400")
#     Showlist.resizable(False, False)
#     Showlist.title("Let's check about it")
#     Showlabel = Label(Showlist, text = mapl)
#     Showlabel.pack()
#     print("Show my walkie talkie man")


def nihahaha():  #  NiHaHaHa!!!!
    Nihahaha = Toplevel(tk)
    Nihahaha.geometry("400x400")
    Nihahaha.resizable(False, False)
    Nihahaha.title("NiHaHaHa!")
    imagenihaha = PhotoImage(file = "nihahaha.PNG")
    Label.image = imagenihaha #  because of Python gabagecollector works reference counting, so i have to 수동으로 참고 횟수 늘려주기.
    nilabel = Label(Nihahaha, image = imagenihaha, compound = "top")
    nilabel.pack(expand = 1, anchor = CENTER)
    add_log("Nihahaha!")


explanationbattery = Label(inputjeo2, text = "▼전지 값을 선택▼", height = 3)
explanationbattery.pack(padx=4)

validate_command = (inputjeo2.register(setbattery), '%P')
invalid_command = (inputjeo2.register(errorsetbattery), '%P')

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

def setbattery(self):
    explanationbattery.config(text = '|전지 값을 선택|& \n |입력 도움 박스|')
    if self == '':
        return True
    
    valid = False
    
    if self.isdigit():
        if (int(self) >= 0 and int(self) <= 100):
            valid = True
    return valid


# 이거 작동 안함 ㅋㅋ
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


def BATTERTYVALUEERROR():
    explanationbattery.config(text="0 is not valid value")

texts = Text(inputjeo2, width=15, height=2)
texts.insert(INSERT, "")
texts.pack(padx=4)


fontia=tkinter.font.Font(family='그래픽', size=10, slant='roman', weight='bold')
resultAlimi = Message(inputjeo3, text='Result', width=121, justify='left', bg='black', fg='white', font=fontia)
resultDisplay = Message(inputjeo3, text="result is not calculated yet", justify='left', bg='white', width=130, padx=5)
logAlimi = Message(inputjeo3, text='Log', width=121, bg='black', fg='white', font=fontia)
logDisplay = Text(inputjeo3, bg='white', width=130, padx=5)
logDisplay.insert('current', "user log here\n")
scrollia=Scrollbar(inputjeo3, width=5, command=logDisplay.yview)
logDisplay.config(yscrollcommand=scrollia.set, state=DISABLED)

resultAlimi.place(x=10, y=10, width=130, height=20)
resultDisplay.place(x=10, y=40, width=130, height=250)
logAlimi.place(x=150, y=10, width=140, height=20)
logDisplay.place(x=150, y=40, width=140, height=250)
scrollia.place(x=285, y=40, width=5, height=250)

def add_log(newlog):
    logDisplay.config(state=NORMAL)
    logDisplay.insert(END, str(newlog)+'\n')
    logDisplay.see(END)
    logDisplay.config(state=DISABLED)

# add_log('i like it')


# class ShirokoJumpscare(ElectricityParts):
#     def __init__(self, position: Point, directions: str) -> None:
#         super().__init__(position, directions)

#     def isdirected(self, directions: str) -> bool:
#     return self.directions == list(directions)


def ShirokoJumpscare():
    add_log(resistors) # 'ElectricityParts' has no attribute 'output_positions'<<뭔개소리야있잖아;;진짜맞짱마렵네;;; 응아님

# def AtsuiAtsukuteHikrabisoUgoiteNaiNoniAtsuiYo():
#     wire = Wire(cursor.position, 'lr')

def DomoSenseiDomoMichiruDesu():
    ElectricityParts.show_status()
# def matsuii():
# def Uwah囧():
#     resistor = Resistor(cursor.position, 'lr')
# # 무녀무녀냥냥
# def MicoMicoNyanNyanJoItsukaraSokoniYasureteImasuru():
#     # add_log("Serika")
#     diode = Diode(cursor.position, 'lr')

# def NyanIchiNiSan():
#     wire = Wire(cursor.position, 'ru')

# def KadenokoujiYukari():
#     if not board.isblank(cursor.position):
#         part = board.get_part(cursor.position)
#         part.rotate_CW()

# def Torya():
#     battery = Battery(cursor.position, 'lr')

# def shubababa():
#     wire = Wire(cursor.position, 'rud')

# def kuyashii():
#     board.remove_part(cursor.position)

# def KeisanToriKanpeki():

# Kiryu Kikyou



# def SunaookamiShiroko():

# def KuromiSerika():


#-------------------------------------------------------------------------Menu-------------------------------------------------------------------------


Button(ui, text = "UP[↑]", command = cursor.go_up).place(x = 90, y = 30, width = 70, height = 70)  #make 이동 ui

Button(ui, text = "LEFT[←]", command = cursor.go_left).place(x = 20, y = 100, width = 70, height = 70)

Button(ui, text = "RIGHT[→]", command = cursor.go_right).place(x = 160, y = 100, width = 70, height = 70)

Button(ui, text = "DOWN[↓]", command = cursor.go_down).place(x = 90, y = 170, width = 70, height = 70)

Button(ui, text = "[↖]", command = cursor.go_upleft).place(x = 20, y = 30, width = 70, height = 70)  #make 이동 ui

Button(ui, text = "[↗]", command = cursor.go_upright).place(x = 160, y = 30, width = 70, height = 70)

Button(ui, text = "[↙]", command = cursor.go_downleft).place(x = 20, y = 170, width = 70, height = 70)

Button(ui, text = "[↘]", command = cursor.go_downright).place(x = 160, y = 170, width = 70, height = 70)

Button(ui, text = "highlight", command = cursor.KadenokoujiYukari).place(x = 90, y = 100, width = 70, height = 70)


Button(ui, text = "Wire[m]", command = cursor_action.generate_wire_line).place(x=20, y=280, width=70, height=70) # wire lr

Button(ui, text = "Resistor[r]", command = cursor_action.generate_resistor).place(x=90, y=280, width=70, height=70) # resistor lr

Button(ui, text = "Diode[d]", command = cursor_action.generate_diode).place(x=160, y=280, width=70, height=70) # diode lr

Button(ui, text = "ㄴ wire[s]", command = cursor_action.generate_wire_curved).place(x=20, y=350, width=70, height=70) # wire ㄴ

Button(ui, text = "Rotate\n[space]", command = cursor_action.rotate_part).place(x=90, y=350, width=70, height=70) # rotate

Button(ui, text = "Battey[b]", command = cursor_action.generate_battery).place(x=160, y=350, width=70, height=70) # battery lr

Button(ui, text = "Sambari[s]", command = cursor_action.generage_wire_Tshape).place(x=20, y=420, width=70, height=70) # wire rud

Button(ui, text = "Operate[o]", command = OPERATE).place(x = 160, y= 420, width = 70, height = 70) # gogogogogoogogogogogo!!!!!!

Button(ui, text = "Erase[e]", command = cursor_action.remove_part).place(x=90, y=420, width=70, height=70) # erase   esraswefd

# Button(ui, text = "RUN[r]", command = amugeona).place(x = 190, y= 350, width = 100, height = 40)


Button(ui, text = "CLEAR\n[Enter]", command = tempwarn).place(x = 20 , y = 520, width = 70, height = 50)

Button(ui, text = 'EXIT[Esc]', command = closewarn).place(x = 160, y= 520, width = 70, height = 50)


menubar = Menu(tk) # menubar is Menu

menu1 = Menu(menubar, tearoff = 0) # menu1은 첫 번째 Menu, tearoff = 0: 하위 메뉴 분리 기능 사용 유무 판단

menu1.add_command(label = "Clear", command = tempwarn)
menu1.add_separator()
menu1.add_command(label = "Exit", command = closewarn)
menubar.add_cascade(label = "File", menu = menu1)

menu2 = Menu(menubar, tearoff = 0, selectcolor = "green")

menu2.add_radiobutton(label = "Undo", state = "disable") # 미안한데 작동 안돼 ㅇㅇㄴㅇ
menu2.add_radiobutton(label = "Redo") # 미안한데 작동 안돼
menu2.add_radiobutton(label = "Cut") # 미안한데 작동 안돼
menubar.add_cascade(label = "Edit", menu = menu2)

menu3 = Menu(menubar, tearoff = 0)

menu3.add_checkbutton(label = "R.S.", command = DomoSenseiDomoMichiruDesu) # Real Status
menu3.add_checkbutton(label = "status", command = ShirokoJumpscare)
menu3.add_checkbutton(label = "nihahaha", command = nihahaha)
menubar.add_cascade(label = "Run", menu = menu3)

menu4 = Menu(menubar, tearoff = 0)

menu4.add_command(label = "About DirectCurrentCircuit", command = aboutlc)
menu4.add_separator()
menu4.add_command(label = "D.C. Help", command = lchelp)
menubar.add_cascade(label = "Help", menu = menu4)

tk.config(menu = menubar)

tk.mainloop()