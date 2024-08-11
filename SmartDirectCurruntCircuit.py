from tkinter import *          #i like tkinter module libarary
import tkinter.font
import tkinter.ttk
import time
tk = Tk()

tk.title('SmartDirectCurruntCircuit-Yes')           # 회로를 구현할 장(張) 만들기
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

class Point: #location = Point(0, 0)
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


class ElectricityParts:
    def __init__(self, position: Point, directions: str) -> None: 
        assert all(map(lambda x: x in 'udlr', directions)),\
            "directions는 u, d, l, r만으로 이루어진 문자열이여야 합니다"
        assert len(set(directions)) == len(directions),\
            "directions에는 중복된 문자가 없어야 합니다"
        
        self.position = position
        self.directions = list(directions)
        self.real_next_positions: None|list[Point] = None
        self.current = -1
        self.current_ratio = 1
        
        board.put_part(self, self.position)
        self._draw()

        add_log(f"generated {self}")


    def _draw(self) -> None:
        raise AttributeError("ElectricityParts의 draw메소드는 반드시 오버라이드되어야 합니다\n"
            "지금 카사네 테토의 오버라이드 들으러 가기 >>> https://www.youtube.com/watch?v=LLjfal8jCYI")

    def show_status(self) -> None:
        '''이곳에 기구의 현재 상태를 표시'''
        '''아래는 임시 코드'''
        try:
            if self.real_next_positions != None:
               add_log(self.real_next_positions)
        except:
            add_log("an error occurred")

    def rotate_CW(self) -> None:
        board.erase(self.position)

        change = {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
        self.directions = list(map(lambda x: change[x], self.directions))
        self._draw()

    def isdirected(self, directions: str) -> bool:
        return set(self.directions) == set(directions)
    
    def get_next_positions(self, input_direction: str='') -> list[tuple[Point, str]]:
        change = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r'}
        output_directions = self.directions.copy()
        output_directions.remove(change[input_direction])

        output_positions = []
        for direction in output_directions:
            x, y = self.position.x, self.position.y
            match direction:
                case 'u': y -= 1
                case 'd': y += 1
                case 'l': x -= 1
                case 'r': x += 1
            output_positions.append((Point(x, y), direction))
        
        return output_positions

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} on {self.position}'

    def __del__(self) -> None:
        add_log(f'deleted {self}')


class Wire(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)
        self.__issambari = len(directions) == 3
        self.__isdivider = False
        self.teleport_pos: Point|None = None

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

    def show_status(self) -> None:
        super().show_status()
        try:
            if self.issambari:
                add_result(f"isdivider: {self.isdivider}")
            add_log(f"ratio: {self.current_ratio:.3f}")
        except:
            pass

    @property
    def issambari(self):
        return self.__issambari

    @property
    def isdivider(self):
        return self.__isdivider

    @isdivider.setter
    def isdivider(self, isdivider):
        self.__isdivider = isdivider


class Resistor(ElectricityParts):
    def __init__(self, position: Point, directions: str, resistance: float=1) -> None:
        super().__init__(position, directions)
        self.__voltage: float = -1
        self.__resistance: float = resistance
        self.__power_consumption: float = -1


    def show_status(self) -> None:
        super().show_status()
        try:
            add_result(f"voltage: {self.voltage:.3f}")
            add_result(f"current: {self.current:.3f}")
            add_result(f"resistance: {self.resistance:.3f}")
            add_result(f"power_consumption: {self.power_consumption:.3f}")
            add_log(f"ratio: {self.current_ratio:.3f}")
        except:
            pass


    def _draw(self, linecolor: str='black', spikecolor: str='black') -> None:
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

        fontiana=tkinter.font.Font(family='맑은 고딕', size=10, slant='roman', weight='bold')
        display.create_text(x+30, y+30, text=resistance_value, font=fontiana, fill='red', anchor=SE)
        
    @property
    def voltage(self):
        return self.__voltage
    
    @voltage.setter
    def voltage(self, value: int):
        assert value > 0, "저항에 걸리는 전압 값은 양수여야 합니다."
        self.__voltage = value

    @property
    def power_consumption(self):
        return self.__power_consumption
    
    @power_consumption.setter
    def power_consumption(self, value: int):
        assert value > 0, "저항의 소비전력 값은 양수여야 합니다."
        self.__power_consumption = value
    
    @property
    def resistance(self):
        return self.__resistance


class Battery(ElectricityParts):
    def __init__(self, position: Point, directions: str, voltage: float=1) -> None:
        super().__init__(position, directions)
        self.__voltage = voltage
        self.plus_direction = directions[0]
        self.minus_direction = directions[1]
        self.real_next_position = self.get_next_position()
        battery_count = board.find_battery_count()
        if battery_count > 1:
            add_log('battery already exist!')
            board.remove_part(position)

    def show_status(self) -> None:
        super().show_status()
        add_result(f"battery voltage: {self.voltage:.3f}")

    def get_next_position(self) -> Point:
        x, y = self.position.x, self.position.y
        match self.plus_direction:
            case 'u': y -= 1
            case 'd': y += 1
            case 'l': x -= 1
            case 'r': x += 1
        
        return Point(x, y)

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
        
        fontiana=tkinter.font.Font(family='그래픽', size=10, slant='roman', weight='bold')
        display.create_text(x+30, y+30, text=battery_value, font=fontiana, fill='red', anchor=SE)

    @property
    def voltage(self):
        return self.__voltage

    @voltage.setter
    def voltage(self, value: float):
        assert value > 0, "전지의 전압 값은 양수여야 합니다."
        self.__voltage = value
    

class Diode(ElectricityParts):
    def __init__(self, position: Point, directions: str) -> None:
        super().__init__(position, directions)
        self.input_direction = self.directions[0]
        self.output_direction = self.directions[1]

    def isdirected(self, directions: str) -> bool:
        return self.directions == list(directions)

    def get_next_positions(self, input_direction: str) -> list[Point|None, str]:
        if input_direction != self.input_direction:
            return [None]
        x, y = self.position.x, self.position.y
        match self.output_direction:
            case 'u': y += 1
            case 'd': y -= 1
            case 'l': x += 1
            case 'r': x -= 1
        
        return [Point(x, y), self.output_direction]

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



class Board:
    def __init__(self, xsize: int, ysize: int) -> None:
        self.xsize = xsize
        self.ysize = ysize
        self.__mapl = [[None]*self.xsize for _ in range(self.ysize)]

    def find_battery_pos(self) -> Point|None:
        for x in range(self.xsize):
            for y in range(self.ysize):
                point = Point(x, y)
                if isinstance(self.try_get_part(point), Battery):
                    add_log(f"found battery in {point}")
                    return point
        add_log(f"no battery in the board")
        return None
    
    def find_battery_count(self) -> int:
        batteryCount=0
        for x in range(self.xsize):
            for y in range(self.ysize):
                point = Point(x, y)
                if isinstance(self.try_get_part(point), Battery):
                    batteryCount+=1
        return batteryCount

    def get_battery(self) -> Battery:
        batterypos = self.find_battery_pos()
        add_log(batterypos)
        return self.get_part(batterypos)
        
    def get_part(self, position: Point) -> ElectricityParts: # 값 없으면 오류발생
        obj = self.__mapl[position.x][position.y]
        if obj == None:
            raise AttributeError(f"{position}에 객체가 존재하지 않습니다")
        elif not isinstance(obj, ElectricityParts):
            raise TypeError(f"{position}에 존재하는 객체가 전기 부품이 아닙니다")
        
        return obj
    
    def try_get_part(self, position: Point) -> ElectricityParts|None: # 값 없으면 None 반환
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


class Cursor:
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

    def generate_wire_Tshape(self, dir: str='lur'):
        Wire(cursor.position, dir)

    def generate_diode(self, dir: str='lr'):
        Diode(cursor.position, dir)

    def generate_resistor(self, dir: str='lr'):
        Resistor(cursor.position, dir, resistance_value)

    def generate_battery(self, dir: str='lr'):
        Battery(cursor.position, dir, battery_value)

    def remove_part(self):
        board.remove_part(cursor.position)

    def rotate_part(self):
        board.rotate_part(cursor.position)


class CurrentManager:
    def __assign_realnextways_to_each_parts(self) -> None:
        #각 Part에 real_next_positions 속성을, 각 삼발이에 isdivider 속성을 부여(가장 먼저 호출돼야 함)
        visited = [[False]*board.xsize for _ in range(board.ysize)]
        start = board.find_battery_pos()
        if start == None:
            add_log("no battery found")
            return

        def dfs(point: Point, direction: str) -> bool: #Battery까지 길이 존재하는 경우만 True를 리턴
            curpart = board.try_get_part(point)
            if not isinstance(curpart, ElectricityParts):
                return False
            if isinstance(curpart, Battery):
                return True
            #add_log(f"{curpart.position, direction, curpart.get_next_positions(direction)}")
            realnexts = []
            for nextpoint, inputdirection in curpart.get_next_positions(direction):
                if visited[nextpoint.y][nextpoint.x]: continue
                
                visited[nextpoint.y][nextpoint.x] = True
                if dfs(nextpoint, inputdirection):
                    realnexts.append(nextpoint)
                visited[nextpoint.y][nextpoint.x] = False

            if not curpart.real_next_positions:
                curpart.real_next_positions = realnexts
            #add_log(f"{curpart.position, curpart.real_next_positions}")
            if isinstance(curpart, Wire) and curpart.issambari:
                curpart.isdivider |= (len(realnexts) == 2)

            return bool(realnexts)
        
        battery = board.get_battery()
        dfs(battery.get_next_position(), battery.plus_direction)


    def __calculate_curline_resistance(self, startpos: Point) -> tuple[float, Point]: #籤
        #현재 도선의 전체저항과 도선의 끝 위치를 튜플 형태로 반환
        curline_resistance = 0
        curpos = startpos
        while True:
            curpart = board.try_get_part(curpos)
            next_positions = curpart.real_next_positions
            
            if isinstance(curpart, Battery):
                return curline_resistance, curpos
            if isinstance(curpart, Wire) and curpart.issambari and not curpart.isdivider:
                return curline_resistance, curpos

            if isinstance(curpart, Resistor):
                curline_resistance += curpart.resistance

            if len(next_positions) > 1: #도선이 갈라질 경우(병렬) - 재귀적으로 처리
                nextlines_conductances: list[int] = []
                for next_pos in next_positions:
                    nextline_resistance, nextline_endpos = self.__calculate_curline_resistance(next_pos)
                    nextlines_conductances.append(1 / nextline_resistance)
                
                conductance_sum = sum(nextlines_conductances)
                for i in range(len(next_positions)):
                    next_pos = next_positions[i]
                    current_ratio = nextlines_conductances[i] / conductance_sum
                    self.__assign_current_ratio_to_curline(next_pos, current_ratio)

                curline_resistance += 1 / conductance_sum
                curpos = curpart.teleport_pos = board.get_part(nextline_endpos).real_next_positions[0]
                
            else:
                curpos = next_positions[0]

    
    def __assign_current_ratio_to_curline(self, curpos: Point, ratio: int) -> None:
        while True:
            curpart = board.get_part(curpos)
            curpart.current_ratio = ratio

            if isinstance(curpart, Wire) and curpart.issambari and not curpart.isdivider:
                return
            
            if len(curpart.real_next_positions) == 1:
                curpos = curpart.real_next_positions[0]
            else:
                curpos = curpart.teleport_pos
        

    def __calculate_overall_resistance(self) -> float:
        start_pos = board.get_battery().get_next_position()
        overall_resistance, _ = self.__calculate_curline_resistance(start_pos)
        add_log(f"overall resistance: {overall_resistance:.3f}")
        return overall_resistance

    def __calculate_start_current(self) -> float:
        battery = board.get_battery()
        start_current = battery.voltage / self.__calculate_overall_resistance()
        add_log(f"start current: {start_current:.3f}")
        return start_current

    def __assign_properties_to_resistors(self, startpos: Point, current: int) -> None:
        #각 저항에 전압, 전력, 소비전력 속성값을 계산해 부여
        curpos = startpos
        curcurrent = current
        while True:
            curpart = board.get_part(curpos)

            if isinstance(curpart, Resistor):
                curpart.current = curcurrent
                curpart.voltage = curpart.current * curpart.resistance
                curpart.power_consumption = curpart.current * curpart.voltage

            if isinstance(curpart, Battery):
                return
            if isinstance(curpart, Wire) and curpart.issambari and not curpart.isdivider:
                return

            next_positions = curpart.real_next_positions
            if len(next_positions) > 1:  #도선이 갈라질 경우(병렬) - 재귀적으로 처리
                for next_pos in next_positions:
                    next_part = board.get_part(next_pos)
                    self.__assign_properties_to_resistors(next_pos, curcurrent * next_part.current_ratio)
                    
                curpos = curpart.teleport_pos
            else:
                curpos = next_positions[0]
                
    def __assign_properties_to_all_resistors(self) -> None:
        start_pos = board.get_battery().get_next_position()
        start_current = self.__calculate_start_current()
        self.__assign_properties_to_resistors(start_pos, start_current)


    def operate(self) -> None:
        add_log("operating...")
        operationButton.config()
        self.__assign_realnextways_to_each_parts()
        self.__assign_properties_to_all_resistors()
        add_log("operating ended")
        operationButton.config(cursor='gumby')



board = Board(20, 20)
cursor = Cursor()
cursor_action = CursorAction()
current_manager = CurrentManager()

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
        cursor_action.generate_wire_Tshape(dir='lrd')

    elif event.keysym == 'h' : # 갈라지는 삼발이:"ㅡ"계열. 'ㅗ'자
        cursor_action.generate_wire_Tshape(dir='lru')

    elif event.keysym == 'j': # 만나는 삼발이: "ㅣ"계열. 'ㅓ'자
        cursor_action.generate_wire_Tshape(dir='udl')

    elif event.keysym == 'k': # 만나는 삼발이: "ㅣ"계열. 'ㅏ'자
        cursor_action.generate_wire_Tshape(dir='udr')

    elif event.keysym == 'b' : # 밧데리
        cursor_action.generate_battery(dir='lr')

    elif event.keysym == 'r' : # 저항
        cursor_action.generate_resistor(dir='lr')

    elif event.keysym == 'e' : # erase
        cursor_action.remove_part() # 클래스 내부에서 사용: self.position | 클래스 외부에서 사용: cursor.position

    elif event.keysym == 'd' : # diode
        cursor_action.generate_diode(dir='lr')

    elif event.keysym == 'o' :
        current_manager.operate()

    # elif event.keysym == 'g':
    #     print(battery_value)

    # elif event.keysym == 'r' : # start(run) module
    #     amugeona()

    elif event.keysym == 'minus' :
        add_log(resistance_value)

    elif event.keysym == 'plus' :
        add_log(battery_value)

    else:                     #Lee Sang Han Button Press >>> 비정의 커맨드 경고 창
        unknowntext = event.keysym,'is not a valid key'  #  위쪽에 정의되지 않은 키 입력들을 unknowntext로 간주, <입력된 키값, 'is not a valid key'>로써 나타냄
        toplevel = Toplevel(tk)
        toplevel.geometry("250x125+450+200")
        toplevel.resizable(False, False)
        toplevel.title("ERROR!")  # 창 이름
        Label(toplevel, text = unknowntext, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "error", compound = "top").place(x=20, y=20, width=210, height=50)  #  unknowntext출력, i마크 표시(붉은색) 할 창 생성
        Button(toplevel, width = 10, text = "okay", overrelief = "solid", command = toplevel.destroy).place(x=90, y=80, width=70)  #  ok버튼 누르면 경고 창 삭제


def setbattery(self):
    explanationbattery.config(text = '▼전지 값을 선택▼')
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
        toplevel.geometry("320x200+450+200")
        toplevel.resizable(False, False)
        toplevel.title("ERROR: not a valid key")  # 창 이름
        Label(toplevel, text = unknowntext, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "error", compound = "top").place(x=20, y=20, width=210, height=50)  #  unknowntext출력, i마크 표시(붉은색) 할 창 생성

        Button(toplevel, width = 10, text = "ok", overrelief = "solid", command = toplevel.destroy).place(x=20, y=80, width=70)  #  ok버튼 누르면 경고 창 삭제
    # explanationresistance.config(text = str(self) + "is invalid value \nvalid value: 0~100")
        cursor_action.remove_part() # 구 코드의 산물이라 작동 안됨 그런데 이거 없앨려면 스핀박스 안에 할당되어있는걸 없애줘야됨

display.bind_all('<KeyPress>', keypressed)
# display의 반댓말은 play ㅋㅋ

def temp():            # 00   clear()와 경고 창 삭제를 동시에
    global areyouokaytoclear
    board.clear()
    # deselectall()
    areyouokaytoclear.destroy()

def tempwarn():        # 00   clear, clear경고 창. 비정의 커맨드 경고 창 코드 참고.
    global areyouokaytoclear
    AYOC = "Are You Okay To Clear This Work?"
    areyouokaytoclear = Toplevel(tk)
    areyouokaytoclear.geometry("250x125+450+200")
    areyouokaytoclear.resizable(False, False)
    areyouokaytoclear.title("Warning!")
    Label(areyouokaytoclear, text = AYOC, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "info", compound = "top").place(x=20, y=20, width=210, height=50)
    Button(areyouokaytoclear, width = 10, text = "yes", overrelief = "solid", command = temp, bg='firebrick', fg='white').place(x=20, y=80, width=70)  #  yes 누르면 경고 창 삭제, clear실행
    Button(areyouokaytoclear, width = 10, text = "no", overrelief = "solid", command = areyouokaytoclear.destroy).place(x=160, y=80, width=70)  #  no 누르면 경고 창만 삭제


def close():           # 18   close the window
    tk.quit()
    tk.destroy()

def closewarn():       # 00   close the window with warnning window \ tempwarn 참고
    AYOE = "Are You Okay To Exit This Program?"
    areyouokaytoexit = Toplevel(tk)
    areyouokaytoexit.geometry("250x125+450+200")
    areyouokaytoexit.resizable(False, False)
    areyouokaytoexit.title("Warning!")
    Label(areyouokaytoexit, text = AYOE, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "info", compound = "top").place(x=20, y=20, width=210, height=50)
    Button(areyouokaytoexit, width = 10, text = "yes", overrelief = "solid", command = close, bg='firebrick', fg='white').place(x=20, y=80, width=70)
    Button(areyouokaytoexit, width = 10, text = "no", overrelief = "solid", command = areyouokaytoexit.destroy).place(x=160, y=80, width=70)
    
# def redo():
# def undo(): 응~ 어차피 지우기 기능 있으니 안 할꺼야~ areyouokaytoclearLOG

def logclearwarn():        # 00   clear, clear경고 창. 비정의 커맨드 경고 창 코드 참고.
    global areyouokaytoclearLOG
    AYOC = "Are You Okay To Clear This Log?"
    areyouokaytoclearLOG = Toplevel(tk)
    areyouokaytoclearLOG.geometry("250x125+450+200")
    areyouokaytoclearLOG.resizable(False, False)
    areyouokaytoclearLOG.title("Warning!")
    Label(areyouokaytoclearLOG, text = AYOC, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "info", compound = "top").place(x=20, y=20, width=210, height=50)
    Button(areyouokaytoclearLOG, width = 10, text = "yes", overrelief = "solid", command = real_clear_log, bg='firebrick', fg='white').place(x=20, y=80, width=70)  #  yes 누르면 경고 창 삭제, clear실행
    Button(areyouokaytoclearLOG, width = 10, text = "no", overrelief = "solid", command = areyouokaytoclearLOG.destroy).place(x=160, y=80, width=70)  #  no 누르면 경고 창만 삭제


def resultclearwarn():        # 00   clear, clear경고 창. 비정의 커맨드 경고 창 코드 참고.
    global areyouokaytoclearRESULT
    AYOC = "Are You Okay To Clear This Result?"
    areyouokaytoclearRESULT = Toplevel(tk)
    areyouokaytoclearRESULT.geometry("250x125+450+200")
    areyouokaytoclearRESULT.resizable(False, False)
    areyouokaytoclearRESULT.title("Warning!")
    Label(areyouokaytoclearRESULT, text = AYOC, width = 200, height = 50, fg = "red", relief = "solid", bitmap = "info", compound = "top").place(x=20, y=20, width=210, height=50)
    Button(areyouokaytoclearRESULT, width = 10, text = "yes", overrelief = "solid", command = real_clear_result, bg='firebrick', fg='white').place(x=20, y=80, width=70)  #  yes 누르면 경고 창 삭제, clear실행
    Button(areyouokaytoclearRESULT, width = 10, text = "no", overrelief = "solid", command = areyouokaytoclearRESULT.destroy).place(x=160, y=80, width=70)  #  no 누르면 경고 창만 삭제


def aboutlc():
    AYOE = "About DirectCurrent Circuit \n Visualizing DirectCurrent Circuit And Experience It \n \n \n Editors: MinSu.L JunSeok.S HyunJune.J \n email: rkddkdus05@gmail.com"
    aboutLC = Toplevel(tk)
    aboutLC.geometry("320x200+450+200")
    aboutLC.resizable(False, False)
    aboutLC.title("About DirectCurrent Circuit")
    lclabel = Label(aboutLC, text = AYOE, width = 300, height = 150, fg = "medium purple", relief = "solid", bitmap = "info", compound = "top")
    lclabel.pack()
    lcbutton = Button(aboutLC, width = 10, text = "close", overrelief = "solid", command = aboutLC.destroy)
    lcbutton.pack()

def lchelp():
    AYOE = "DirectCurrent Circuit Help \n Commands \n \n \n [m(ㅡ)] > [fill 'ㅡ'wire] \n [l(ㅣ)] > [fill 'ㅣ'wire] \n \n derived from 'ㅡ' is fill Current Distribution wire \n [n(ㅜ)] > [fill 'ㅜ'wire] \n [h(ㅗ)] > [fill 'ㅗ'wire] \n \n derived from 'ㅣ' is fill Current Collecting wire \n [j(ㅓ)] > [fill 'ㅓ'wire] \n [k(ㅏ)] > [fill 'ㅏ'wire] \n \n [s(ㄴ)] > [fill 'ㄴ'wire] \n [b] > [set battery]  \n [r] > [set resistance]  \n [space] > [rotate wire] \n [Esc] > [Exit] \n [Enter] > [Clear] \n [e] > [Erase] \n [o] > [Operate] "
    LCHelp = Toplevel(tk)
    LCHelp.geometry("320x520+450+70")
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
    Nihahaha.geometry("400x400+400+100")
    Nihahaha.resizable(False, False)
    Nihahaha.title("NiHaHaHa!")
    imagenihaha = PhotoImage(file = "nihahaha.PNG")
    Label.image = imagenihaha #  because of Python gabagecollector works reference counting, so i have to 수동으로 참고 횟수 늘려주기.
    nilabel = Label(Nihahaha, image = imagenihaha, compound = "top")
    nilabel.pack(expand = 1, anchor = CENTER)
    add_log("Nihahaha!")

# --------------------------------------------------------User Interface(left)---------------------------------------------------------------

explanationbattery = Label(inputjeo2, text = "▼전지 값을 선택▼", height = 3)

validate_command = (inputjeo2.register(setbattery), '%P')
invalid_command = (inputjeo2.register(errorsetbattery), '%P')

def update_variable(*args):
    global battery_value
    battery_value = battery_spinbox_var.get()

battery_spinbox_var = DoubleVar()

batteryspinbox = Spinbox(inputjeo2, width=10, from_=1, to=100, increment=0.1, validate = 'all', bd=3, validatecommand=validate_command, invalidcommand=invalid_command, textvariable=battery_spinbox_var, state='readonly')


battery_spinbox_var.trace('w', update_variable)
battery_value = battery_spinbox_var.get()


# re


explanationresistance = Label(inputjeo2, text = "▼저항 값을 선택▼", height = 3)


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
#$$
def setresistance(self):
    explanationresistance.config(text = '▼저항 값을 선택▼')
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
    cursor_action.remove_part()


validate_command = (inputjeo2.register(setresistance), '%P')
invalid_command = (inputjeo2.register(errorsetresistance), '%P')

def 헬보이2골든아미VALUECHECK(self):
    explanationresistance.config(text='')
    if self == '':
        return True
    
    
    valid = False
    if self.isdigit():
        if (int(self) != 0):
            valid = True
    return valid

def 헬보이2골든아미VALUEERROR():
    explanationresistance.config(text="0 이면 전선 불타다")

def MicoMicoNyanNyanJoItsukaraSokoniYasureteImasuru(self):
    explanationresistance.config(text = '|저항 값을 선택|')
    if self == '':
        return True
    
    valid = False
    
    if self.isdigit():
        if (int(self) >= 0 and int(self) <= 100):
            valid = True
    return valid



def update_variable(*args):
    global resistance_value
    resistance_value = resistance_spinbox_var.get()

resistance_spinbox_var = DoubleVar()

resistancespinbox = Spinbox(inputjeo2, width=10, from_=1, to=100, increment=0.1, validate = 'all', bd=3, validatecommand=validate_command, invalidcommand=invalid_command, textvariable=resistance_spinbox_var, state='readonly')

resistance_spinbox_var.trace('w', update_variable)
resistance_value = battery_spinbox_var.get()

resultLock=IntVar()
logLock=IntVar()

explanationbattery.place(x=25, y=20, width=100, height=30)

batteryspinbox.place(x=30, y=50, width=90, height=25)

explanationresistance.place(x=25, y=90, width=100, height=30) 

resistancespinbox.place(x=30, y=120, width=90, height=25)

tkinter.ttk.Separator(inputjeo2, orient=HORIZONTAL).place(x=25, y=168, width=100)

Checkbutton(inputjeo2, text='Result Lock', justify=LEFT, variable=resultLock).place(x=25, y=185, width=100, height=25)

Checkbutton(inputjeo2, text='Log Lock   ', justify=LEFT, variable=logLock).place(x=25, y=215, width=100, height=25)

# --------------------------------------------------------Log & Result---------------------------------------------------------------

def clear_result():
    resultDisplay.config(state=NORMAL)
    resultDisplay.delete(1.0, END)
    resultDisplay.insert(END, 'result successfully erased'+'\n')
    resultDisplay.config(state=DISABLED)

def clear_log():
    logDisplay.config(state=NORMAL)
    logDisplay.delete(1.0, END)
    logDisplay.insert(END, 'log successfully erased'+'\n')
    logDisplay.config(state=DISABLED)

def real_clear_result(): # 확인창 만들기 위해 사용d
    global areyouokaytoclearRESULT
    clear_result()
    areyouokaytoclearRESULT.destroy()

def real_clear_log():
    global areyouokaytoclearLOG
    clear_log()
    areyouokaytoclearLOG.destroy()

fontia=tkinter.font.Font(family='그래픽', size=10, slant='roman')
resultAlimi = Message(inputjeo3, text='Result', width=121, justify='left', bg='black', fg='white', font=fontia)
resultDisplay = Text(inputjeo3, bg='white', width=130, padx=5)
logAlimi = Message(inputjeo3, text='Log', width=121, bg='black', fg='white', font=fontia)
logDisplay = Text(inputjeo3, bg='white', width=140, padx=5)
logDisplay.insert('current', "user log here\n")
resultDisplay.insert('current', "result here\n")
scrollia=Scrollbar(inputjeo3, width=5, command=logDisplay.yview)
scrolliana=Scrollbar(inputjeo3, width=5, command=resultDisplay.yview)
resultDisplay.config(yscrollcommand=scrolliana.set, state=DISABLED)
logDisplay.config(yscrollcommand=scrollia.set, state=DISABLED)
resultClearButton=Button(inputjeo3, text='result clear', command=resultclearwarn)
logClearButton=Button(inputjeo3, text='log clear', command=logclearwarn)

resultAlimi.place(x=10, y=10, width=130, height=20)
resultDisplay.place(x=10, y=40, width=130, height=250)
logAlimi.place(x=150, y=10, width=140, height=20)
logDisplay.place(x=150, y=40, width=140, height=250)
scrolliana.place(x=135, y=40, width=5, height=250)
scrollia.place(x=285, y=40, width=5, height=250)
resultClearButton.place(x=10, y=295)
logClearButton.place(x=150, y=295)

def add_result(newresult):
    printResult=resultLock.get()
    if printResult == 0:
        resultDisplay.config(state=NORMAL)
        resultDisplay.insert(END, str(newresult)+'\n')
        resultDisplay.see(END)
        resultDisplay.config(state=DISABLED)

def add_log(newlog):
    printLog=logLock.get()
    if printLog == 0:
        logDisplay.config(state=NORMAL)
        logDisplay.insert(END, str(newlog)+'\n')
        logDisplay.see(END)
        logDisplay.config(state=DISABLED)


#-------------------------------------------------------------------------User Interface(right)-------------------------------------------------------------------------

Button(ui, text = "UP[↑]", command = cursor.go_up, bg='gainsboro', repeatdelay=200, repeatinterval=40, cursor='top_side').place(x = 90, y = 30, width = 70, height = 70)  #make 이동 ui

Button(ui, text = "LEFT[←]", command = cursor.go_left, bg='gainsboro', repeatdelay=200, repeatinterval=40, cursor='left_side').place(x = 20, y = 100, width = 70, height = 70)

Button(ui, text = "RIGHT[→]", command = cursor.go_right, bg='gainsboro', repeatdelay=200, repeatinterval=40, cursor='right_side').place(x = 160, y = 100, width = 70, height = 70)

Button(ui, text = "DOWN[↓]", command = cursor.go_down, bg='gainsboro', repeatdelay=200, repeatinterval=40, cursor='bottom_side').place(x = 90, y = 170, width = 70, height = 70)

Button(ui, text = "[↖]", command = cursor.go_upleft, repeatdelay=200, repeatinterval=40, cursor='top_left_corner').place(x = 20, y = 30, width = 70, height = 70)  #make 이동 ui

Button(ui, text = "[↗]", command = cursor.go_upright, repeatdelay=200, repeatinterval=40, cursor='top_right_corner').place(x = 160, y = 30, width = 70, height = 70)

Button(ui, text = "[↙]", command = cursor.go_downleft, repeatdelay=200, repeatinterval=40, cursor='bottom_left_corner').place(x = 20, y = 170, width = 70, height = 70)

Button(ui, text = "[↘]", command = cursor.go_downright, repeatdelay=200, repeatinterval=40, cursor='bottom_right_corner').place(x = 160, y = 170, width = 70, height = 70)

Button(ui, text = "highlight", command = cursor.KadenokoujiYukari, repeatdelay=200, repeatinterval=40, cursor='man').place(x = 90, y = 100, width = 70, height = 70)

tkinter.ttk.Separator(ui, orient=HORIZONTAL).place(x=15, y=260, width=220)

Button(ui, text = "─ Wire[m]", command = cursor_action.generate_wire_line, bg='gainsboro').place(x=20, y=280, width=70, height=70) # wire lr

Button(ui, text = "Resistor[r]", command = cursor_action.generate_resistor, bg='gainsboro').place(x=90, y=280, width=70, height=70) # resistor lr

Button(ui, text = "Diode[d]", command = cursor_action.generate_diode, bg='gainsboro').place(x=160, y=280, width=70, height=70) # diode lr

Button(ui, text = "└ wire[s]", command = cursor_action.generate_wire_curved, bg='gainsboro').place(x=20, y=350, width=70, height=70) # wire ㄴ

Button(ui, text = "RotateCW\n[space]", command = cursor_action.rotate_part, bg='gainsboro').place(x=90, y=350, width=70, height=70) # rotate

Button(ui, text = "Battey[b]", command = cursor_action.generate_battery, bg='gainsboro').place(x=160, y=350, width=70, height=70) # battery lr

Button(ui, text = "┴ Sambari[h]", command = cursor_action.generate_wire_Tshape, bg='gainsboro').place(x=20, y=420, width=70, height=70) # wire rud

operationButton = Button(ui, text = "Operate[o]", command = current_manager.operate, bg='skyblue',  cursor='gumby') # gogogogogoogogogogogo!!!!!!
operationButton.place(x = 160, y= 420, width = 70, height = 70)

Button(ui, text = "Erase[e]", command = cursor_action.remove_part, bg='gainsboro').place(x=90, y=420, width=70, height=70) # erase   esraswefd

# Button(ui, text = "RUN[r]", command = amugeona).place(x = 190, y= 350, width = 100, height = 40)

tkinter.ttk.Separator(ui, orient=HORIZONTAL).place(x=15, y=510, width=220)

Button(ui, text = "CLEAR\n[Enter]", command = tempwarn, bg='ghostwhite', bd=3, relief=RIDGE, activebackground='ghostwhite').place(x = 20 , y = 530, width = 80, height = 50)

Button(ui, text = 'EXIT[Esc]', command = closewarn, bg='firebrick', fg='white', bd=3, activebackground='firebrick', activeforeground='white').place(x = 150, y= 530, width = 80, height = 50)

#-------------------------------------------------------------------------Menu-------------------------------------------------------------------------

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

menu3.add_checkbutton(label = "nihahaha", command = nihahaha)
menubar.add_cascade(label = "Run", menu = menu3)

menu4 = Menu(menubar, tearoff = 0)

menu4.add_command(label = "About DirectCurrentCircuit", command = aboutlc)
menu4.add_separator()
menu4.add_command(label = "D.C. Help", command = lchelp)
menubar.add_cascade(label = "Help", menu = menu4)

tk.config(menu = menubar)

tk.mainloop()