# Создаем шарики

## Циклы и массивы

Создавать пузырьки мы уже умеем. Для того, чтобы создать пузырек в любом месте экрана, можно поступить следующим образом: определяем координату центра окружности, например (500, 300). Далее отнимаем от чисел радиус окружности (например 10) и получаем координату верхнего левого угла квадрата (490, 290), в котором будет рисоваться круг. Затем к координатам добавляем радиус и получаем нижний правый угол квадрата (510, 310).
Таким образом, чтобы нарисовать окружность с радиусом 10 в точке (500, 300), нужно выполнить:
```python
a = c.create_oval(500-10, 300-10, 500+10, 300+10, outline='white')
```

Конечно же, проще это сделать с помощью переменных:
```python
x = 500
y = 300
r = 10
a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
```

Для того, чтобы создать пузырек в случайном месте, необходимо указать случайные координаты. Для того, чтобы получить случайное число, необходимо использовать функцию `randint` из модуля `random`. В самом верху нашей программы подключим этот модуль и загрузим эту функцию:
```python
from random import randint
```

Например, чтобы получить случайно число в диапазоне от 1 до 10, нужно вызвать `randint(1, 10)`. И теперь вместо чисел 500 и 300 указываем генерацию случайных. Переменная `x` у нас может быть в диапазоне от 0 до ширины нашего экрана. Ширина у нас `WIDTH` (которая равна 600), т.е. у нас получится `x = randint(0, WIDTH)`. Переменная `y` может быть в диапазоне от 0 до высоты экрана. Высота у нас `HEIGHT` (которая равна 400). Получим `y = randint(0, HEIGHT)`. Радиус пусть тоже будет случайным от 10 до 30.
У нас (с учетом предыдущего кода из прошлых уроков будет так):
```python
from tkinter import *
from random import randint
 
window = Tk()
... (здесь весь остальной текст) ...
c.bind_all('<Key>', move_ship)

x = randint(0, WIDTH)
y = randint(0, HEIGHT)
r = randint(10,30)
a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
```

Каждый раз как мы будем запускать программу - пузырек будет появляться в случайном месте.
Давайте создадим функцию, которая будет создавать пузырек. Добавим `def` и имя функции перед четырьмя строками, а перед ними добавим отступы:
```python
def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
```

Теперь каждый раз, как будем вызывать функцию - пузырек будет создаваться в случайном месте. Вызовем функцию 4 раза:
```python
def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')

create_bubble()
create_bubble()
create_bubble()
create_bubble()
```

Получим 4 пузырька в случайных местах случайного размера. 
Для того, чтобы вызвать функцию `create_bubble` 10 раз, можно использовать цикл. Заменим код:
```python
def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')

for i in range(10):
	create_bubble()
```

Конструкция `range(10)` формирует 10 чисел от 0 до 9 и помещает их каждый раз в переменную i, а затем выполняет то, что в этом цикле (смотрим по отступам). Значение переменной i нам пока не нужно. Нам нужно просто 10 раз выполнить процедуру.

Что делать, если нам необходимо третий пузырек подвинуть? Сейчас мы его подвинуть никак не можем, потому что у нас нет переменной, в которой он лежит. Переменная a во-первых перезатерлась 4м пузырьком, а во-вторых находится внутри функции и ее использовать мы не можем. Мы можем для каждого пузырька создавать новые переменные a1, a2, a3 и a4, но если пузырьков будет много, это будет неудобно. Поэтому будем использовать массивы.
Массивы - это такие структуры, которые позволяют хранить несколько значений под одним именем, доступ к ним осуществляется по индексу. В этом случае будем использовать `a[0]`, `a[1]`, `a[2]` и `a[3]`. Индексы начинаются с нуля и указываются в скобках `[]`. На первый взгляд мы только усложнили, но сейчас познакомимся с циклами и поймем в чем удобство.
Объявим массив с именем `bub_id`, а созданный пузырек (который временно в переменной `a`) добавим в наш массив с помощью команды `.append`:

```python
bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)

for i in range(10):
	create_bubble()
```

После вызова `bub_id.append(a)` в конец массива добавляется `a` (новосозданный пузырек).
Теперь у нас в массиве `bub_id` содержится 10 пузырьков. `bub_id[0]` ссылается на первый, `bub_id[1]` на второй, ..., `bub_id[9]` на десятый.

Следущим шагом давайте сдвинем все созданные пузырьки влево на 10 точек. Если бы у нас на каждый пузырек была отдельная переменная (или если бы мы не знали про циклы), то мы бы делали так:
```python
c.move(bub_id[0], -10, 0)
c.move(bub_id[1], -10, 0)
c.move(bub_id[2], -10, 0)
... (тут еще 6) ...
c.move(bub_id[9], -10, 0)
```

Здесь мы меням координату `x` на 10 влево, координату `y` не меняем (0) у каждого из десяти пузырьков.
Но теперь используем циклы и переменную i. Переменную будем использовать вместо чисел: `c.move(bub_id[i], -10, 0)`. И получим следующий код:

```python
bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)

for i in range(10):
	create_bubble()
	
for i in range(10):
	c.move(bub_id[i], -10, 0)
```
Давайте для удобства перемещение пузырьков вынесем в отдельную процедуру, назовем ее `move_bubbles`:

```python
bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)
	
def move_bubbles():
	for i in range(10):
		c.move(bub_id[i], -10, 0)

for i in range(10):
	create_bubble()

```

У данного кода есть одна проблема - если мы создадим 5 пузырьков, то процедура попытается переместить 10, на шестом пузырьке будет ошибка. Поэтому пусть процедура перемещает столько пузырьков, сколько в массиве. Узнать длину массива можно узнать с помощью функции `len(bub_id)`, используем ее вместо 10:
```python
def move_bubbles():
	for i in range(len(bub_id)):
		c.move(bub_id[i], -10, 0)
```

Если мы вызовем функцию перемещения и запустим программу, мы не увидим движения. Т.к. создадутся пузырьки и переместятся мгновенно. Давайте двигать пузырьки бесконечно влево. Создадим бесконечный цикл. Для этого будем использовать не `for`, а `while`:

```python
bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)

def move_bubbles():
	for i in range(len(bub_id)):
		c.move(bub_id[i], -10, 0)

for i in range(10):
	create_bubble()
	
while True:
	move_bubbles()
```

Если запустить программу - она зависнет, мы даже не увидим окошка, т.к. `while True` будет вызываться бесконечно, т.к. условие `True` у нас не меняется. (Кстати, чтобы прервать зависшую программу, надо нажать CTRL+C).
Для того, чтобы окно реагировало на изменения, добавим `window.update()`
```python
bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)

def move_bubbles():
	for i in range(len(bub_id)):
		c.move(bub_id[i], -10, 0)

for i in range(10):
	create_bubble()
	
while True:
	move_bubbles()
	window.update()
```

Если запустить программу - мы не увидим пузырьков, потому что они мгновенно улетят влево. Давайте добавим задержку. Это можно сделать с помощью процедуры `sleep` из модуля `time`. Импортируем его в самом верху программы, а в процедуру при вызове передадим 0.01 с.
```python
from tkinter import *
from random import randint
from time import sleep

window = Tk()
... остальной код здесь ...

bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)

def move_bubbles():
	for i in range(len(bub_id)):
		c.move(bub_id[i], -10, 0)

for i in range(10):
	create_bubble()
	
while True:
	move_bubbles()
	window.update()
	sleep(0.01)
```

Если запустить программу - мы увидим что пузырьки уплываю влево. Давайте создавать новые пузырьки в бесконечном цикле, у 10 ранее созданных удалим:
```python
bub_id = list()

def create_bubble():
	x = randint(0, WIDTH)
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)

def move_bubbles():
	for i in range(len(bub_id)):
		c.move(bub_id[i], -10, 0)
	
while True:
	create_bubble()
	move_bubbles()
	window.update()
	sleep(0.01)
```

Если запустить код, то мы увидим как появляются пузырьки и уплывают влево. На текущий момент у нас такие проблемы:
1. Пузырьки появлюятся в пустом месте
2. Пузырьков очень много, нужно раз в 10 меньше.
3. Все пузырьки плывут с одинаковой скоростью
4. Когда пузырек уплывает за пределы экрана - мы все равно его двигаем и создаем новые. В итоге массив постоянно растет и увеличивается, что в дальнейшем приведет к большому расходу памяти, ненужным действиям и тормозам.

Три проблемы мы решим на этом уроке.
Для начала будем создавать пузырьки за пределами экрана справа. Для этого координату x не будем формировать случайным образом, а пусть будет она равна ширине экрана (`WIDTH`) + 100.
Второе. У каждого пузырька должна быть своя скорость движения, а не 10, как у всех. Для хранения скоростей создадим еще один массив, назовем его `bub_speed`, который будем заполнять во время создания пузырька случайными числами от 1 до 10.
И последнее, в бесконечном цикле будем создавать пузырек не каждый раз, а каждый десятый раз. Вариантов реализации несколько, мы возьмем работу со случайными числами. Сформируем случайное число от 1 до 10. Если оно 1 - формируем пузырек, если нет - не формируем.
Исправленные моменты отмечены комментарием #.

```python
bub_id = list()
bub_speed = list() # Объявляем новый массив

def create_bubble():
	x = WIDTH + 100 # Координата x всегда справа за пределами экрана
	y = randint(0, HEIGHT)
	r = randint(10,30)
	a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
	bub_id.append(a)
	bub_speed.append(randint(1,10)) # Заполняем массив случайным числом от 1 до 10

def move_bubbles():
	for i in range(len(bub_id)):
		c.move(bub_id[i], -bub_speed[i], 0) # Вместо -10 будем использовать -bub_speed[i], в котором хранится скорость текущего пузырька.
	
while True:
	if (randint(1,10) == 1): # Формируем пузырек в среднем в одном из 10 случаев.
		create_bubble()
	move_bubbles()
	window.update()
	sleep(0.01)
```

# Итоговый код:

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
        c.move(ship, 0, -SHIP_SPD)
        c.move(ship2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
        c.move(ship, 0, SHIP_SPD)
        c.move(ship2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        c.move(ship, -SHIP_SPD, 0)
        c.move(ship2, -SHIP_SPD, 0)
    elif event.keysym == 'Right':
        c.move(ship, SHIP_SPD, 0)
        c.move(ship2, SHIP_SPD, 0)
		
c.bind_all('<Key>', move_ship)

bub_id = list()
bub_speed = list()

def create_bubble():
    x = WIDTH + 100
    y = randint(0, HEIGHT)
    r = randint(10,30)
    a = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(a)
    bub_speed.append(randint(1,10))

def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)
	
while True:
    if (randint(1,10) == 1): 
        create_bubble()
    move_bubbles()
    window.update()
    sleep(0.01)
```

![Окно](https://github.com/usbo/ekids/raw/master/Python/Lesson3/img/img1.gif)