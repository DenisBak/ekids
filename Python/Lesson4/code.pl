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
