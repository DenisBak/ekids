import pygame
from pygame.sprite import Group, Sprite

window = pygame.display.set_mode((600, 400))
screen = pygame.Surface((600, 400))

clock = pygame.time.Clock()
inGame = True

im = pygame.image.load('images\\brick.png')
im2 = pygame.image.load('images\\q1.png')

g = Group()

# Первый способ
s = Sprite()
s.image = im
s.rect = s.image.get_rect()
s.rect.topleft = 100, 150
s.add(g)

# Второй способ
class Obj(Sprite):
    def __init__(self, im, x, y):
        Sprite.__init__(self)
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.add(g)

class Im(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, im, x, y)


Im(200, 150)
a = Im(250, 150)

class QQ(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, im2, x, y)

QQ(200, 250)

beton_img = pygame.image.load('images//cinder.png')
class Beton(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, beton_img, x, y)
for i in range(3):
    for j in range(3):
        Beton(i*32, j*32)

x = 100
while (inGame):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            inGame = False

    screen.fill((0,0,0))

    a.rect.x = x
    x += 1

    g.draw(screen)

    window.blit(screen, (0, 0))

    pygame.display.flip()
    clock.tick(50)
