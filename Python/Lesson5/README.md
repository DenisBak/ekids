# Лопаем пузыри

Необходимо вычислить столкновение между кораблем и пузырями. Для этого необходимо вычислить расстояние между их центрами и сравнить его с их радиусами. Если радиус корабля + радиус пузыря будут больше расстояния между центрами фигур - значит произошло столкновение.

Для вычисления расстояния между двумя координатами будем использовать формулу: `sqrt((x2-x1)**2 + (y2-y1)**2)`. Здесь `sqrt` означает квадратный корень, а `**2` - возведение в степень 2, т.е. в квадрат. Функция `sqrt` находится в библиотеке `math`, подключим ее в самом верху программы:

```python
from math import sqrt
```

Создадим функцию `distance`, возвращающую расстояние между центрами объектов, поместим ее после `clean_up_bubs` перед бесконечным циклом:

```python
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((y2-y1)**2 + (x2-x1)**2)
```

Функция принимает на вход идентификаторы двух объектов, в один будем передавать очередной пузырек, во второй - окружность нашего корабля. Здесь мы используем ранее написанные функции `get_coords`, которые возвращают координаты центров объектов, и используем их в формуле.

Для проверки столкнулись ли объекты, напишем процедуру `collision`. Но перед этим необходимо знать радиус пузырька, чтобы использовать его в проверке. Можно его вычислить, а можно сохранить в массиве при создании, выберем второй вариант. Создадим массив `bub_r` после создания массива `bub_speed`:

```python
...
bub_speed = list()
bub_r = list() # создаем массив для радиусов пузырей
...
```

В процедуре создания пузырька добавим радиус в массив:

```python
def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(10, 30)
    a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(a)
    bub_speed.append(randint(1, 10))
    bub_r.append(r) # Добавляем радиус пузырька в массив
```

В процедуре удаления пузырька не забудем очистить массив:

```python
def del_bubble(i):
    c.delete(bub_id[i])
    del bub_id[i]
    del bub_speed[i]
    del bub_r[i] # Удаляем радиус пузырька из массива
```

Теперь можем писать процедуру вычисления столкновения:

```python
def collision():
    for i in range(len(bub_id)-1, -1, -1):
        if distance(ship2, bub_id[i]) < (SHIP_R + bub_r[i]):
            del_bubble(i)
```

Здесь мы бежим по всем пузырькам (в обратном порядке) и если расстояние между ними меньше суммы их радиусов, удалим пузырек.
Вызовем ее в основном цикле:

```python
while True:
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    collision() # Вызываем проверку столкновения
    window.update()
    sleep(0.01)
```

Теперь при столкновении - пузырек исчезнет. Добавим счетчик лопнувших пузырьков, а чтобы добавить игровой момент - за быстрые и мелкие пузырьки будем давать больше очков. Будем считать очки так - "Скорость пузырька - радиус пузырька + 40". Чем больше скорость и чем меньше радиус - тем больше очков получит игрок.

Сделаем из процедуры `collision` функцию, которая вернет количество очков:

```python
def collision():
    points = 0
    for i in range(len(bub_id)-1, -1, -1):
        if distance(ship2, bub_id[i]) < (SHIP_R + bub_r[i]):
            points += (40 - bub_r[i]) + bub_speed[i]
            del_bubble(i)
    return points
```

В основном цикле программы будем добавлять результат функции к основной переменной `score`:

```python
score = 0 # Счет
while True:
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision() # Вызываем проверку столкновения
	print(score) # Временно выводим очки в консоль
    window.update()
    sleep(0.01)
```

В консоли теперь видно количество набранных очков. Добавим таймер и сделаем вывод очков и времени прямо на экран, а не в консоль. Для создания текста на экране используем функции `create_text` холста. Нам понадобится четыре текстовых объекта. Два буду содержать надписи "Время" и "Счет", а два остальных - соответствующие числа.
Создадим объекты прямо перед основным циклом:

```python
c.create_text(50, 30, text='Time', fill='white')
c.create_text(150, 30, text='Score', fill='white')
time_text = c.create_text(50, 50, fill='white')
score_text = c.create_text(150, 50, fill='white')
```

Создадим две процедуры, которые будут выводить счет и время в созданные два объекта:

```python
def show_score(score):
    c.itemconfig(score_text, text=str(score))

def show_time(time):
    c.itemconfig(time_text, text=str(time))
```

Для того чтобы число перевести в текст мы используем функцию `str`.

Дадим игроку 30 секунд на раунд. Создадим переменную `TIME_LIMIT`:

```python
TIME_LIMIT = 30
```

Для того, чтобы отмерить 30 секунд, нам необходимо узнать текущее время в секундах и прибавить к нему 30 секунд, это будет переменная `end`. Игра закончится, когда текущее время будет больше или равно конечного времени.
И бесконечный цикл поменяем на конечный, теперь он будет выглядеть так:

```python
TIME_LIMIT = 30 # 30 секунд на раунд
score = 0 # Счет
end = time() + TIME_LIMIT # Время, когда игра остановится
while time() < end: # бежим пока не достигли time
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision() # Вызываем проверку столкновения
    show_score(score) # Выводим текущий счет на экран
    show_time(int(end - time())) # Выводим оставшееся до конца время
    window.update()
    sleep(0.01)
```

Мы используем функцию `int` для того, чтобы дробное число стало целым.

# Полученный код

```python
from tkinter import *
from random import randint
from time import sleep, time # грузим time
from math import sqrt

window = Tk()
window.title('Первое окошко')

WIDTH = 600
HEIGHT = 400
SHIP_R = 15 # Радиус нашего корабля

c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

ship = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship2 = c.create_oval(0, 0, SHIP_R*2, SHIP_R*2, outline='red') # Поменяли 30 на SHIP_R*2

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
		
c.bind_all('<Key>', move_ship)

bub_id = list()
bub_speed = list()
bub_r = list() # создаем массив для радиусов пузырей
GAP = 100
def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(10, 30)
    a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(a)
    bub_speed.append(randint(1, 10))
    bub_r.append(r) # Добавляем радиус пузырька в массив

def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y

def del_bubble(i):
    c.delete(bub_id[i])
    del bub_id[i]
    del bub_speed[i]
    del bub_r[i] # Удаляем радиус пузырька из массива

def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x,y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)
# Вычисляем расстояние между двумя объектами
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((y2-y1)**2 + (x2-x1)**2)
# Вычисляем столкнулись ли объекты
def collision():
    points = 0
    for i in range(len(bub_id)-1, -1, -1):
        if distance(ship2, bub_id[i]) < (SHIP_R + bub_r[i]):
            points += (40 - bub_r[i]) + bub_speed[i]
            del_bubble(i)
    return points

c.create_text(50, 30, text='Time', fill='white')
c.create_text(150, 30, text='Score', fill='white')
time_text = c.create_text(50, 50, fill='white')
score_text = c.create_text(150, 50, fill='white')

def show_score(score):
    c.itemconfig(score_text, text=str(score))

def show_time(time):
    c.itemconfig(time_text, text=str(time))

TIME_LIMIT = 30 # 30 секунд на раунд
score = 0 # Счет
end = time() + TIME_LIMIT # Время, когда игра остановится
while time() < end: # бежим пока не достигли time
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision() # Вызываем проверку столкновения
    show_score(score) # Выводим текущий счет на экран
    show_time(int(end - time())) # Выводим оставшееся до конца время
    window.update()
    sleep(0.01)
```