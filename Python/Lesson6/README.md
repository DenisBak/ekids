# Добавляем таймер обратного отсчета

Добавим две переменные, одна будет считать количество бонусных раундов, вторая определит, сколько очков нужно набрать для очередного раунда:

```python
...
BONUS_SCORE = 1000 # очки для следующего раунда
bonus = 0 # Бонусный раунд
# Далее идет основной цикл
# ОСНОВНОЙ ЦИКЛ
while time() < end: # бежим пока не достигли time
...
```
В основном цикле программы осталось написать условие добавления бонусного времени:

```python
	# После
	score += collision() # Вызываем проверку столкновения
	# Добавляем:
    if (int(score / BONUS_SCORE) > bonus):
        bonus += 1
        end += TIME_LIMIT
```

# Добавим бонусных пузырьков

Добавим бонусный пузырек, при столкновении с которым скорость движения всех остальных замедлится на несколько секунд.
Будем использовать ту же процедуру создания пузырьков `create_bubble`. Чтобы понять какой пузырек создается - обычный или бонусный, будем передавать в нее параметр `t`. Также доавим новый массив, в котором будут содержаться типы пузырьков (0 - обычный, 1 - бонусный). Если пузырек бонусный - он будет желтого цвета:
```python
bub_type = list() # тип пузыря
def create_bubble(t):
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(10, 30)
    clr = 'white' # по-умолчанию цвет белый
    if t == 1: # если создаем бонусный пузырек
        clr = 'yellow' # то цвет желтый
    a = c.create_oval(x-r, y-r, x+r, y+r, outline=clr) # меняем цвет на clr
    bub_id.append(a)
    bub_speed.append(randint(1, 10))
    bub_r.append(r) 
    bub_type.append(t) # Добавляем тип пузыря в массив
```

Мы добавили новый массив, не забудем удалить из него строки при удалении пузырьков, исправим `del_bubble`:

```pyton
def del_bubble(i):
    c.delete(bub_id[i])
    del bub_id[i]
    del bub_speed[i]
    del bub_r[i]
    del bub_type[i] # Удаляем запись из массива типов пузырей
```

Добавим переменную `bonus1_end`, в которой будет время окончания бонусного замедления, и исправим процедуру движения пузырьков `move_bubbles`, если сейчас действует бонусное время замедления - скорость всех пузырьков уменьшим. Но она может стать равной нулю и пузырьки остановятся - учтем это:
```python
bonus1_end = 0 # время, когда закончится действие бонуса с типом 1

def move_bubbles():
    for i in range(len(bub_id)):
        s = bub_speed[i] # скорость по умолчанию
        if (time() < bonus1_end): # бонус замедляет пузырьки
            s = int(s / 5); # в пять раз
            if (s == 0): # если скорость равна 0 (пузырьки стоят)
                s = 1 # пусть двигаются с минимальной скоростью
        c.move(bub_id[i], -s, 0)
```

Обработаем столкновение с бонусным пузырьком в функции `collision`, если столкнулись - поставим бонусное время замедления равным текущее + пара секунд. Вспомним, что тип пузырька (бонусный он или нет) хранится в массиве `bub_type`:

```python
BONUS1_TIME = 3 # время действия бонуса с типом 1

def collision():
    global bonus1_end # чтобы можно было изменить переменную 
    points = 0
    for i in range(len(bub_id)-1, -1, -1):
        if distance(ship2, bub_id[i]) < (SHIP_R + bub_r[i]):
            if (bub_type[i] == 1): # если пузырек бонусный
                bonus1_end = time() + BONUS1_TIME # бонус закончится через 3 сек
            points += (40 - bub_r[i]) + bub_speed[i]
            del_bubble(i)
    return points
```

Обращаем внимание на `global bonus1_end`, строка нужна для того, чтобы можно было поменять значение переменной, объявленной вне функции. Иначе ее значение после завершения функции останется старым.

Осталось только создавать бонусные пузырьки в основном цикле программы:

```python
...
# ОСНОВНОЙ ЦИКЛ
while time() < end: # бежим пока не достигли time
    if randint(1,10) == 1:
        create_bubble(0) # ставим здесь 0 - создаются обычные пузырьки
    if randint(1,200) == 1:
        create_bubble(1) # ставим здесь 1 - создаются бонусные пузырьки
	...
```

Мы исправили вызов `create_bubble` для основных пузырьков, т.к. теперь `create_bubble` ожидает на вход один параметр - число, которое поместится в переменную `t`.

# Убираем задержку при управлении с клавиатуры.
Корабль двигается тогда, когда нажимается клавиша, скорость нажатия клавиши зависит от клавиатуры и настроек, чтобы от этого не зависеть, исправим логику - движение корабля будем делать в основном цикле программы, а при нажатии и отпускании клавиш просто будем ставить "флаги".
Мы откажемся от процедуры `move_ship`, исправим ее следующим образом, перед ней создадим переменные-флаги для четырех сторон, удалим параметр `event` и условия движения корабля:

```python
IS_UP = False
IS_DOWN = False
IS_LEFT = False
IS_RIGHT = False
def move_ship(event):
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
```
Т.е. сейчас корабль будет двигаться в указанном направлении только если соответствующий флаг включен.

Устанавливать и убирать флаги будем при нажатии и отпускании клавиш, старое назначение удалим:
Найдем:
```python
c.bind_all('<Key>', move_ship)
```

И удалим (или закомментируем):
```python
#c.bind_all('<Key>', move_ship)
```

Вместо этого добавим две процедуры, которые будут вызываться при нажатии и отпускании клавиш:

```python
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

c.bind_all('<KeyPress>', keypressed)
c.bind_all('<KeyRelease>', keyreleased)
```

Осталось вызвать `move_ship` в основном цикле игры:
```python
# ОСНОВНОЙ ЦИКЛ
while time() < end: 
    if randint(1,10) == 1:
        create_bubble(0)
    if randint(1,200) == 1:
        create_bubble(1)
    move_ship() # двигаем корабль
	...
```

# Финальный код:
```python
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

ship = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship2 = c.create_oval(0, 0, SHIP_R*2, SHIP_R*2, outline='red')

MID_X = WIDTH / 2
MID_Y = HEIGHT / 2

c.move(ship, MID_X, MID_Y)
c.move(ship2, MID_X, MID_Y)

SHIP_SPD = 10

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

def move_ship():
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
    clr = 'white' # по-умолчанию цвет белый
    if t == 1: # если создаем бонусный пузырек
        clr = 'yellow' # то цвет желтый
    a = c.create_oval(x-r, y-r, x+r, y+r, outline=clr) # меняем цвет на clr
    bub_id.append(a)
    bub_speed.append(randint(1, 10))
    bub_r.append(r) 
    bub_type.append(t) # Добавляем тип пузыря в массив

bonus1_end = 0 # время, когда закончится действие бонуса с типом 1

def move_bubbles():
    for i in range(len(bub_id)):
        s = bub_speed[i] # скорость по умолчанию
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

def collision():
    global bonus1_end # чтобы можно было изменить переменную 
    points = 0
    for i in range(len(bub_id)-1, -1, -1):
        if distance(ship2, bub_id[i]) < (SHIP_R + bub_r[i]):
            if (bub_type[i] == 1): # если пузырек бонусный
                bonus1_end = time() + BONUS1_TIME # бонус закончится через 3 сек
            points += (40 - bub_r[i]) + bub_speed[i]
            del_bubble(i)
    return points

c.create_text(50, 30, text='Time', fill='white')
c.create_text(150, 30, text='Score', fill='white')
time_text = c.create_text(50, 50, text='1111', fill='white')
score_text = c.create_text(150, 50, fill='white')

def show_score(score):
    c.itemconfig(score_text, text=str(score))

def show_time(time):
    c.itemconfig(time_text, text=str(time))

TIME_LIMIT = 30 # 30 секунд на раунд
BONUS_SCORE = 1000 # очки для следующего раунда
score = 0 # Счет
bonus = 0 # Бонусный раунд
end = time() + TIME_LIMIT

# ОСНОВНОЙ ЦИКЛ
while time() < end: # бежим пока не достигли time
    if randint(1,10) == 1:
        create_bubble(0)
    if randint(1,200) == 1:
        create_bubble(1)
    move_ship() # двигаем корабль
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
```