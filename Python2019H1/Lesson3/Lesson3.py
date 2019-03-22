import pygame
from pygame.sprite import Sprite, Group
import sys

WORLD_HEIGHT = 14*32  # Высота экрана - 14 кубиков
WORLD_WIDTH = 16*32  # Ширина экрана - 16 кубиков
SCENE_WIDTH = 212*32  # Ширина всего мира - 212 кубиков

window = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
pygame.display.set_caption("Mario")

screen = pygame.Surface((SCENE_WIDTH, WORLD_HEIGHT))  # Основной экран, на нем будут все объекты
screenbg = pygame.Surface((SCENE_WIDTH, WORLD_HEIGHT))  # Фон, на нем будет фон

animGroup = Group()  # Группа для анимированных объектов
objGroup = Group()  # Группа для всех объектов (анимированных и нет)

''' Константы для более понятного кода '''
DIRECTION_LEFT = 'L'  # Марио смотрит влево
DIRECTION_RIGHT = 'R'  # Марио смотрит вправо
# Типы объектов:
OBJECT_QUESTION = 'question'  # Кубик с вопросиком
OBJECT_BRICK = 'brick'  # Кирпич
# Типы кубиков с вопросиком:
QUESTION_COIN = 'coin'  # Монетка
QUESTION_MUSHROOM = 'mushroom'  # Гриб роста

''' Настройки игры '''
SPEED = 3  # Скорость Марио
OBJ_ANIM_SPEED = 10  # Скорость анимации объектов


''' Класс для отрисовки мира '''
class World:
    def __init__(self, screenbg):
        screenbg.fill((107, 140, 255))  # голубой фон
        # Массив со всеми фоновыми картинками и их местоположениями:
        bgdata = {
            'hill1': [(0, 400)],
            'grass1': [(368, 400)],
            'hill2': [(512, 400)],
            'grass2': [(752, 400)],
            'grass3': [(1326, 400)],
            'cloud1': [(624, 96), (1808, 148)],
            'cloud3': [(880, 128)],
            'cloud2': [(1168, 96)]
        }
        for bgo in bgdata:
            for c in bgdata[bgo]:
                x, y = c
                img = pygame.image.load('images\\bg\\' + bgo + '.png').convert_alpha()
                # Т.к. я замерял нижний левый угол картинок, а выводятся они по верхнему левому, то нужно отнять высоту:
                y = y - img.get_rect().height
                # Шаблон повторяется 5 раз через каждые 1536 точек, поэтому эту картинку рисуем 5 раз в разных местах:
                for i in range(5):
                    screenbg.blit(img, (x, y))
                    x += 1536

        # Массив с землей:
        # Шаблон: 69 кубиков + 2 пустых + 15 кубиков + 3 пустых + 64 кубика + 2 пустых + 57 кубиков = 212 кубика всего
        fdata = [1 for i in range(69)] \
              + [0 for i in range(2)] \
              + [1 for i in range(15)] \
              + [0 for i in range(3)] \
              + [1 for i in range(64)] \
              + [0 for i in range(2)] \
              + [1 for i in range(57)]
        for i in range(2):
            for j in range(len(fdata)):
                if fdata[j] == 1:
                    x = 32 * j
                    y = 432 + 32 * i
                    Ground(x, y)
        
        # Массив со всеми остальными объектами:
        # Объекты располагаются в квадратах, отсчет идет снизу (от земли) вверх
        objdata = {
            'brick': [
                (20, 3),
                (22, 3),
                (24, 3),
                (77, 3),
                (5, 1), (7, 3)
            ],
            'question': [
                (16, 3, QUESTION_COIN),
                (21, 3, QUESTION_MUSHROOM),
                (22, 7, QUESTION_COIN),
                (23, 3, QUESTION_COIN),
                (6, 2, ''), (8, 4, '')
            ],
        }
        for objt in objdata:
            for coord in objdata[objt]:
                x = coord[0] * 32
                y = 400 - coord[1] * 32
                if objt == 'brick':
                    Brick(x, y)
                elif objt == 'question':
                    t = coord[2]
                    Question(x, y, t)
        

class Mario(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.sprites = {}  # Массив для хранения картинок Марио из двух букв - STATE + DIRECTION
        self.jumping = False  # При создании Марио не находится в прыжке
        self.moving = False  # При создании Марио не двигается
        self.direction = DIRECTION_RIGHT  # ...и смотрит вправо
        self.f = 0  # Номер текущего кадра анимации (первый = 0)
        self.velocity = 0  # Вертикальное ускорение Марио (для прыжков и падений)
        # Загружаем картинки в массив:
        files = {
            'AR': ['images\\marioAR.png'],
            'AL': ['images\\marioAL.png'],
            'BR': ['images\\marioBR1.png', 'images\\marioBR2.png', 'images\\marioBR1.png', 'images\\marioBR3.png'],
            'BL': ['images\\marioBL1.png', 'images\\marioBL2.png', 'images\\marioBL1.png', 'images\\marioBL3.png'],
            'CL': ['images\\marioCL.png'],
            'CR': ['images\\marioCR.png'],
        }
        for t in files:
            self.sprites[t] = []
            for ar in files[t]:
                self.sprites[t].append(pygame.image.load(ar).convert_alpha())
        ''' Следующие две переменные нужны для функций pygame '''
        self.image = self.sprites['AR'][0]  # Текущая картинка
        self.rect = self.image.get_rect()
        self.rect.bottomleft = x, y
        # После столкновения могут измениться:
        self.new_rect = self.rect  # Местоположение Марио (при столкновениях)
        self.new_velocity = 0  # Вертикальное ускорение (если ударился или приземлился)

    ''' Получаем текущую картинку очень просто. Берем состояние марио (Стоит - A, Бежит - B, Прыгает - C), затем
    прибавляем к букве его направление (Влево - L, Вправо - R), получаем строку типа AL - и берем картинку с
    текущим кадром '''
    def draw(self):
        sprite = '';
        # Определяем состояние Марио:
        if self.jumping:
            sprite = 'C'
        elif self.moving:
            sprite = 'B'
        else:
            sprite = 'A'
        # Добавляем направление Марио:
        sprite += self.direction
        # Определяем кадр (текущий и следующий):
        f = (self.f // SPEED) % len(self.sprites[sprite])
        self.f += 1  # Следующий кадр, далее смотрим, вылезли ли за края массива:
        if self.f > len(self.sprites[sprite]) * SPEED:
            self.f = 0
        bl = self.rect.bottomleft  # Сохраним текущую позицию картинки 
        self.image = self.sprites[sprite][f]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bl  # Восстановим позицию картинки
        screen.blit(self.image, self.rect.topleft)

    # Двигаем Марио влево
    def move_left(self):
        self.rect.left -= SPEED * 2
        if self.rect.left < 0:
            self.rect.left = 0
        self.direction = DIRECTION_LEFT
        self.moving = True

    # Двигаем Марио вправо
    def move_right(self):
        self.rect.left += SPEED * 2
        if self.rect.right > SCENE_WIDTH:
            self.rect.right = SCENE_WIDTH
        self.direction = DIRECTION_RIGHT
        self.moving = True

    # Марио прыгает вверх
    def jump(self, vel):
        self.jumping = True
        self.velocity = vel

    # Обрабатываем прыжки и падения
    def process_jumping(self):
        ''' Прыжки '''
        if self.jumping:
            self.rect.top = self.rect.top + self.velocity
            self.velocity += 1

    def get_x(self):
        x = WORLD_WIDTH/2 - self.rect.centerx
        if x > 0:
            x = 0
        if x < WORLD_WIDTH - SCENE_WIDTH:
            x = WORLD_WIDTH - SCENE_WIDTH
        return x


''' Класс-шаблон для всех объектов '''
class Obj(Sprite):
    def __init__(self, imgs, x, y):
        Sprite.__init__(self)
        self.images = []
        self.f = 0
        for im in imgs:
            self.images.append(im)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        if len(self.images) > 1:
            self.add(animGroup)
        self.add(objGroup)
        self.rect.bottomleft = x, y

    def anim(self):
        self.image = self.images[self.f // OBJ_ANIM_SPEED]
        self.f += 1
        if self.f // OBJ_ANIM_SPEED >= len(self.images):
            self.f = 0


''' Класс для земли '''
ground_img = pygame.image.load('images\\ground.png').convert_alpha()
class Ground(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [ground_img], x, y)


''' Класс для кирпичей '''
brick_img = pygame.image.load('images\\obj\\brick.png').convert_alpha()
class Brick(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [brick_img], x, y)


''' Класс для кубиков с вопросиками '''
question_imgs = [pygame.image.load('images\\obj\\q' + str(i+1) + '.png').convert_alpha() for i in range(3)]
class Question(Obj):
    def __init__(self, x, y, t):
        Obj.__init__(self, question_imgs, x, y)
        self.question_type = t
        

''' ИГРА '''

World(screenbg)  # Загружаем фон

mario = Mario(200*32, 360)  # Загружаем Марио

pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock()

inGame = True
while inGame:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            inGame = False
            pygame.quit()
            sys.exit()

    ''' Обрабатываем нажатия клавиш '''
    keys = pygame.key.get_pressed()  # Получаем массив всех нажатых клавиш
    if keys[pygame.K_LEFT]:  # Если нажата клавиша "Влево"
        mario.move_left()
    if keys[pygame.K_RIGHT]:  # Если нажата клавиша "Вправо"
        mario.move_right()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:  # Если нажата клавиша "Вверх" или "Пробел"
        mario.jump(-10)

    ''' Обрабатываем прыжки '''
    mario.process_jumping()

    ''' Рисуем фон '''
    screen.blit(screenbg, (0, 0))

    ''' Вызываем анимацию анимированных объектов '''
    for a in animGroup:
        a.anim()

    ''' Рисуем все остальные объекты '''
    objGroup.draw(screen)

    ''' Рисуем марио '''
    mario.draw()
    
    window.blit(screen, (mario.get_x(), 0))

    pygame.display.flip()

    clock.tick(50)
