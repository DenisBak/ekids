# Очищаем ненужное

Когда пузырек улетает за левую границу экрана - он продолжает свое путешествие. Программа также каждый раз сдвигает его влево. Массив пузырей постоянно пополняется новыми пузырями, объем памяти и ненужных действий растет.
Будем удалять пузырь с экрана, а также очищать все связанные с ним массивы после того, как пузырек улетел за пределы экрана.
Для этого нам необходимо:
* узнать координаты каждого пузыря
* проверить - улетел ли пузырь за границу экрана
* если улетел - удалить его, очистить массивы

Для определения координат воспользуемся функцией холста `c.coords`, которой передадим созданный ранее объект (который хранятся в массиве `bub_id`).
По пузырю функция возвращает 2 координаты - `x1`,`y1`,`x2`,`y2` (т.к. при создании мы также указывали 2 координаты). Напишем свою функцию так, чтобы она возвращала всего одну координату - центр пузыря. Для этого найдем среднее арифметическое координат `x` и `y`: `x = (x1+x2)/2`, `y = (y1+y2)/2`.

Создадим функцию `get_coords`, в которую передадим идентификатор созданного ранее пузыря:
```python
# ...
# Здесь предыдущий код до цикла while

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y
	
# Здесь предыдущий код начиная от цикла while
while True:
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
	...
```
Слово `return` указывает на то, что у нас функция, а не процедура. Что при вызове `get_coords` она вернет 2 числа, которые нужно будет поместить в переменные.

Также напишем функцию для удаления одного пузыря. Назовем ее `del_bubble`, но в параметрах передадим индекс массива, а не идентификатор пузыря, т.к. по индексу мы сможем узнать идентификатор, а сам индекс нам нужен для того, чтобы удалить эту запись из массива. Для удаления записи из массива существует конструкция `del bub_id[i]`, где `i` - индекс массива, который нужно удалить. После удаления все нижерасположенные элементы сдвигаются вверх.
Для удаления пузыря с холста, воспользуемся процедурой `c.delete(x)`, где `x` - идентификатор пузыря. Нам необходимо очистить два массива - массив идентификаторов и массив скоростей.
```python
# после функции get_coords:
	
def del_bubble(i):
    c.delete(bub_id[i])
    del bub_id[i]
    del bub_speed[i]
```

Теперь, если вызвать эту функцию с параметром 5, то она удалит шестой пузырь, а также очистит в двух массивах шестые элементы.

Для удаления всех пузырей, которые покинули экран, напишем процедуру `clean_up_bubs`. Она будет бежать по всем пузырям, проверять координату `x`, если она за пределами экрана, например уже меньше -100, то удалим. Пузыри у нас создаются в процедуре `create_bubble` справа за пределами экрана, там мы тоже используем число 100. Выделим для него отдельную переменную, назовем ее `GAP`, и присвоим ей значение 100. Вставим ее перед функцией `create_bubble`:

```python
# здесь предыдущий код, исправляем функцию create_bubble

GAP = 100
def create_bubble():
    x = WIDTH + GAP # вместо 100 подставили переменную GAP
    y = randint(0, HEIGHT)
    r = randint(10, 30)
    a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(a)
    bub_speed.append(randint(1, 10))

# здесь остальной код
```

Теперь создадим процедуру `clean_up_bubs`. В ней будет цикл по всем пузырям, если пузырь улетел - мы его удалим. Есть одна проблема - при удалении записи из массива - все остальные сдвигаются вверх. Допустим пузыри с индексом 3,4,6 улетели за экран. Если бежать обычным циклом, получим такую картину:
* i=1
* Надо удалять 1? - Нет
* i=2
* Надо удалять 2? - Нет
* i=3
* Надо удалять 3? - Да, удаляем запись с индексом 3, все остальные сдвигаются выше. Теперь старая запись 4,6 стали 3,5
* i=4 
* Надо удалять 4? - Нет, т.к. 4й сдвинулся выше, на его место пришел 5й. А его удалять не надо. В итоге 4й, который удалять надо - ушел выше и мы его пропустили.
Чтобы этого избежать, будем бежать не с 0 до N-1, а с N до 0, для этого воспользуемся дополнительными двумя параметрами `range`:
```python
# после функции del_bubble:

def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x,y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

```

Процедура бежит по массиву, начиная с конца до 0 (-1 не включительно), с шагом -1 (в обратном порядке). Получает координаты текущего пузыря, если он вылетел за предел - удалим его.

Осталось только вызвать процедуру в основном цикле:
```python
while True:
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs() # вызываем очистку
    window.update()
    sleep(0.01)
```

# Дополнительно

Есть еще одна проблема - когда мы управляем кораблем, мы можем загнать его за пределы экрана. Можно этого избежать, добавив условия:
Если нажали клавишу "вверх" - смотрим координату `y` корабля, если она больше 0 - то разрешаем движение корабля вверх. Для красоты можно сравнивать не с нулем, а с 20 - тогда корабль не будет наполовину залезать за экран:
```python
...
# исправляем move_ship
def move_ship(event):
    if event.keysym == 'Up':
        x,y = get_coords(ship2) # проверяем координату корабля
        if y > 20: # разрешаем движение вверх, только если у корабля есть место
            c.move(ship, 0, -SHIP_SPD)
            c.move(ship2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
...
```

Аналогично исправляем оставшиеся 3 направления:

```python
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
```

# Итоговый код

```python
from tkinter import *
from random import randint
from time import sleep

window = Tk()
window.title('Первое окошко')

WIDTH = 600
HEIGHT = 400

c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

ship = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship2 = c.create_oval(0, 0, 30, 30, outline='red')

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
GAP = 100
def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(10, 30)
    a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(a)
    bub_speed.append(randint(1, 10))

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

def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x,y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

while True:
    if randint(1,10) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    window.update()
    sleep(0.01)
```