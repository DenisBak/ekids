from tkinter import *
from random import randint
from time import sleep, time 
from math import sqrt

window = Tk()
window.title('Первое окошко')

WIDTH = 600
HEIGHT = 400
SHIP_R = 15 

c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

ship = c.create_polygon(5, 5, 5, 25, 30, 15, fill='lime')
ship2 = c.create_oval(0, 0, SHIP_R*2, SHIP_R*2, outline='lime')

MID_X = WIDTH / 2
MID_Y = HEIGHT / 2

c.move(ship, MID_X, MID_Y)
c.move(ship2, MID_X, MID_Y)

SHIP_SPD = 10
def move_ship(event):
    if event.keysym == 'Up':
        x,y = get_coords(ship2)
        if y > 20:
            c.move(ship, 0, -SHIP_SPD)
            c.move(ship2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
        x,y = get_coords(ship2)
        if y < HEIGHT-20:
            c.move(ship, 0, SHIP_SPD)
            c.move(ship2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        x,y = get_coords(ship2)
        if x > 20:
            c.move(ship, -SHIP_SPD, 0)
            c.move(ship2, -SHIP_SPD, 0)
    elif event.keysym == 'Right':
        x,y = get_coords(ship2)
        if x < WIDTH-20:
            c.move(ship, SHIP_SPD, 0)
            c.move(ship2, SHIP_SPD, 0)
		
#c.bind_all('<Key>', move_ship)

IS_UP = False
IS_DOWN = False
IS_LEFT = False
IS_RIGHT = False
def keypressed(event):
    global IS_UP
    global IS_DOWN
    global IS_LEFT
    global IS_RIGHT
    if event.keysym == 'Up':
        IS_UP = True
    if event.keysym == 'Down':
        IS_DOWN = True
    if event.keysym == 'Left':
        IS_LEFT = True
    if event.keysym == 'Right':
        IS_RIGHT = True
    if event.keysym == 'r':
        reset()

def keyreleased(event):
    global IS_UP
    global IS_DOWN
    global IS_LEFT
    global IS_RIGHT
    if event.keysym == 'Up':
        IS_UP = False
    if event.keysym == 'Down':
        IS_DOWN = False
    if event.keysym == 'Left':
        IS_LEFT = False
    if event.keysym == 'Right':
        IS_RIGHT = False

def move():
    if IS_UP:
        x,y = get_coords(ship2)
        if y > 20:
            c.move(ship, 0, -SHIP_SPD)
            c.move(ship2, 0, -SHIP_SPD)
    if IS_DOWN:
        x,y = get_coords(ship2)
        if y < HEIGHT-20:
            c.move(ship, 0, SHIP_SPD)
            c.move(ship2, 0, SHIP_SPD)
    if IS_LEFT:
        x,y = get_coords(ship2)
        if x > 20:
            c.move(ship, -SHIP_SPD, 0)
            c.move(ship2, -SHIP_SPD, 0)
    if IS_RIGHT:
        x,y = get_coords(ship2)
        if x < WIDTH-20:
            c.move(ship, SHIP_SPD, 0)
            c.move(ship2, SHIP_SPD, 0)

c.bind_all('<KeyPress>', keypressed)
c.bind_all('<KeyRelease>', keyreleased)

bub_id = list()
bub_speed = list()
bub_r = list() 
bub_type = list() # тип пузыря
GAP = 100
def create_bubble(t):
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(10, 30)
    s = randint(1, 10) 
    clr = 'white' # по-умолчанию цвет белый
    if t == 1: # если создаем бонусный пузырек
        clr = 'yellow'# то цвет желтый
        r = randint(10,15)
        s = randint(7,10)
    if t == 2:
        clr = 'black'
        r = randint(10,20)
        s = randint(1,5)
    if t == 3:
        clr = 'pink'
        r = 15
        s = randint(7,10)
    a = c.create_oval(x-r, y-r, x+r, y+r, outline=clr) # меняем цвет на clr
    bub_id.append(a)
    bub_speed.append(s)
    bub_r.append(r) 
    bub_type.append(t) # Добавляем тип пузыря в массив

bonus1_end = 0 # время, когда закончится действие бонуса с типом 1

def move_bubbles():
    for i in range(len(bub_id)):
        s = bub_speed[i] # скорость по умолчанию
        if bub_type[i]==0:
            if (time() < bonus1_end): # бонус замедляет пузырьки
                s = int(s / 5);
                if (s == 0):
                    s = 1
        c.move(bub_id[i], -s, 0)

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y

def del_bubble(i):
    c.delete(bub_id[i])
    del bub_id[i]
    del bub_speed[i]
    del bub_r[i]
    del bub_type[i] # Удаляем запись из массива типов пузырей

def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x,y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((y2-y1)**2 + (x2-x1)**2)

BONUS1_TIME = 3 # время действия бонуса с типом 1
life_count = 3

def collision():
    global bonus1_end # чтобы можно было изменить переменную 
    points = 0
    global life_count
    global end
    for i in range(len(bub_id)-1, -1, -1):
        if distance(ship2, bub_id[i]) < (SHIP_R + bub_r[i]):
            if (bub_type[i] == 1): # если пузырек бонусный
                bonus1_end = time() + BONUS1_TIME # бонус закончится через 5 сек
            if (bub_type[i] == 2):
                life_count-=1
            if (bub_type[i] == 3):
                life_count+=1
            if (bub_type[i] == 2 or bub_type[i]== 3):
                show_hp(life_count)
                if life_count == 3:
                    c.itemconfig(ship2, outline = 'lime')
                elif life_count == 2:
                    c.itemconfig(ship2, outline = 'orange')
                elif life_count == 1:
                    c.itemconfig(ship2, outline = 'red')
                elif life_count == 0:
                    c.itemconfig(ship2, outline = 'darkblue')
                elif life_count == -1:
                    end = time()-1
            
            points += (40 - bub_r[i]) + bub_speed[i]
            del_bubble(i)
    return points

c.create_text(50, 30, text='Time', fill='white')
c.create_text(150, 30, text='Score', fill='white')
c.create_text(250, 30, text='hp', fill='white')
time_text = c.create_text(50, 50, text='1111', fill='white')
score_text = c.create_text(150, 50, fill='white')
hp_text = c.create_text(250, 50, fill='white')

def show_hp(life_count):
    c.itemconfig(hp_text, text=str(life_count))
    
def show_score(score):
    c.itemconfig(score_text, text=str(score))

def show_time(time):
    c.itemconfig(time_text, text=str(time))

TIME_LIMIT = 30 # 30 секунд на раунд
BONUS_SCORE = 1000 # очки для следующего раунда
score = 0 # Счет
bonus = 0 # Бонусный раунд
end = time() + TIME_LIMIT

def reset():
    global score
    global bonus
    global end
    global life_count
    for i in range(len(bub_id)-1, -1, -1):
        del_bubble(i)
    score = 0
    bonus = 0
    end = time() + TIME_LIMIT
    life_count = 3
    show_hp(life_count)

# ОСНОВНОЙ ЦИКЛ
while True:
    while time() < end: # бежим пока не достигли time
        if randint(1,10) == 1:
            create_bubble(0)
        if randint(1,150) == 1:
            create_bubble(1)
        if randint(1,150) == 1:
            create_bubble(2)
        if randint(1,450) == 1:
            create_bubble(3)    
        move() # двигаем корабль
        move_bubbles()
        clean_up_bubs()
        score += collision() # Вызываем проверку столкновения
        if (int(score / BONUS_SCORE) > bonus):
            bonus += 1
            end += TIME_LIMIT
        
        show_score(score)
        show_time(int(end - time()))
        window.update()
        sleep(0.01)
    window.update()
    sleep(0.01)
