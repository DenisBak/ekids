import pygame
from pygame.sprite import Sprite, Group
import sys

WORLD_HEIGHT = 14*16*2
WORLD_WIDTH = 16*16*2
SCENE_WIDTH = 212*16*2

window = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
pygame.display.set_caption("Mario")

screen = pygame.Surface((SCENE_WIDTH, WORLD_HEIGHT))
screenbg = pygame.Surface((SCENE_WIDTH, WORLD_HEIGHT))

SPEED = 3
D_RIGHT = 1
D_LEFT = 0
# Типы объектов:
T_QUESTION = 'q'
T_BRICK = 'brick'
T_GROUND = 'ground'
T_ACTION_BRICK = 'coinbrick'
T_PIPE = 'pipe'
T_CINDER = 'cinder'
T_FLAGSTICK = 'flagstick'
T_FLAG = 'flag'
T_FLAGSTICKBALL = 'flagstickball'
T_CASTLE = 'castle'
# Подтипы объекта T_QUESTION
T_COIN = 1
T_MUSHROOM = 2
T_STAR = 3
# Скорость анимации объектов
OBJ_ANIM_SPEED = 10

animGroup = Group()  # Группа для анимированных объектов
actionGroup = Group()  # Группа для объектов с которыми можно взаимодействовать
objGroup = Group()  # Группа для всех объектов (анимированных и нет)

gndtpl = [1 for i in range(69)] + [0 for i in range(2)] + [1 for i in range(15)] + [0 for i in range(3)] \
         + [1 for i in range(64)] + [0 for i in range(2)] + [1 for i in range(57)]

world_data = {
    'bg': {
        'hill1': [(0, 400)],
        'grass1': [(368, 400)],
        'hill2': [(512, 400)],
        'grass2': [(752, 400)],
        'grass3': [(1326, 400)],
        'cloud1': [(624, 96), (1808, 148)],
        'cloud3': [(880, 128)],
        'cloud2': [(1168, 96)]
    },
    'obj': {
        T_QUESTION: [
            (16, 3, T_COIN),
            (21, 3, T_MUSHROOM),
            (22, 7, T_COIN),
            (23, 3, T_COIN),
            (78, 3, T_MUSHROOM),
            (94, 7, T_COIN),
            (106, 3, T_COIN),
            (109, 3, T_COIN),
            (112, 3, T_COIN),
            (109, 7, T_MUSHROOM),
            (129, 7, T_COIN),
            (130, 7, T_COIN),
            (170, 3, T_COIN)
        ],
        T_BRICK: [(20, 3), (22, 3), (24, 3), (77, 3), (79, 3)]
                 + [(80 + i, 7) for i in range(8)]  # 80 - 87
                 + [(91 + i, 7) for i in range(3)]  # 91 - 93
                 + [(100, 3), (118, 3), (121, 7), (122, 7), (123, 7), (128, 7), (129, 3), (130, 3), (131, 7),
                    (168, 3), (169, 3), (171, 3)]
        ,
        T_GROUND: [(j*16*2, 400 + i * 16*2) if gndtpl[j] == 1 else (-1, -1) for i in range(2) for j in range(212)],
        T_ACTION_BRICK: [(94, 3, T_COIN), (101, 3, T_STAR)],
        T_PIPE: [(28, 0, 0, ''), (38, 0, 1, ''), (38, 1, 0, ''), (46, 2, 0, ''), (46, 1, 1, ''), (46, 0, 1, '')
                 , (57, 2, 0, 'UNDER1'), (57, 1, 1, ''), (57, 0, 1, ''), (163, 0, 0, 'UNDER1_OUT'), (179, 0, 0, '')],
        T_CINDER: [(134, 0)] + [(135, i) for i in range(2)] + [(136, i) for i in range(3)] + [(137, i) for i in range(4)] +
            [(143, 0)] + [(142, i) for i in range(2)] + [(141, i) for i in range(3)] + [(140, i) for i in range(4)] +
            [(148, 0)] + [(149, i) for i in range(2)] + [(150, i) for i in range(3)] + [(151, i) for i in range(4)] + [(152, i) for i in range(4)] +
            [(158, 0)] + [(157, i) for i in range(2)] + [(156, i) for i in range(3)] + [(155, i) for i in range(4)] +
            [(181 + i, j) for i in range(8) for j in range(i+1)] + [(189, j) for j in range(8)] + [(198, 0)],
        T_FLAGSTICK: [(198, 1+i) for i in range(9)],
        T_FLAG: [(197.5, 9)],
        T_FLAGSTICKBALL: [(198, 10)],
        T_CASTLE: [(202, 0, 1)],
    }
}


class World:
    def __init__(self):
        pass

    def init(self):
        screenbg.fill((107, 140, 255))
        for wdt in world_data:
            if wdt == 'bg':
                for bgo in world_data[wdt]:
                    for c in world_data[wdt][bgo]:
                        x, y = c
                        img = pygame.image.load('images\\bg\\' + bgo + '.png').convert_alpha()
                        y = y - img.get_rect().height
                        # Шаблон повторяется 5 раз
                        for i in range(5):
                            screenbg.blit(img, (x, y))
                            x += 768*2
            elif wdt == 'obj':
                for objt in world_data[wdt]:
                    for coord in world_data[wdt][objt]:
                        if objt == T_QUESTION:
                            x, y, t = coord
                            Question(x * 16 * 2, 400 - y * 16 * 2, t)
                        elif objt == T_BRICK:
                            x, y = coord
                            Brick(x * 16 * 2, 400 - y * 16 * 2)
                        elif objt == T_GROUND:
                            x, y = coord
                            if x >= 0 and y >= 0:
                                Ground(x, y)
                        elif objt == T_ACTION_BRICK:
                            # Пока будет обычный
                            x, y, t = coord
                            Brick(x * 16 * 2, 400 - y * 16 * 2)
                        elif objt == T_PIPE:
                            x, y, a, t = coord
                            Pipe(x * 16 * 2, 400 - y * 16 * 2, a, t)
                        elif objt == T_CINDER:
                            x, y = coord
                            Cinder(x * 16 * 2, 400 - y * 16 * 2)
                        elif objt == T_FLAGSTICK:
                            x, y = coord
                            Flagstick(x * 16 * 2, 400 - y * 16 * 2)
                        elif objt == T_FLAG:
                            x, y = coord
                            Flag(x * 16 * 2, 400 - y * 16 * 2)
                        elif objt == T_CASTLE:
                            x, y, t = coord
                            Castle(x * 16 * 2, 400 - y * 16 * 2, t)
                        elif objt == T_FLAGSTICKBALL:
                            x, y = coord
                            Flagstickball(x * 16 * 2, 400 - y * 16 * 2)


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
        self.add(actionGroup)
        self.rect.bottomleft = x, y
        self.disabled = False
        self.transparent = False  # можно ли проходить сквозь объект

    def collide_bottom(self):
        pass

    def collide_right(self):
        pass

    def collide_left(self):
        pass

    ''' Вызывается, когда Марио столкнулся с объектом '''
    def collide(self):
        # Смотрим пересечение, чтобы отсечь незначительные касания
        r = self.rect.clip(mario.rect)
        # Марио двигается вверх
        if r.bottom == self.rect.bottom and r.width > r.height:
            if mario.velocity <= 0:
                self.collide_bottom()
                if not self.transparent:
                    mario.new_velocity = 0
            if not self.transparent:
                mario.new_rect.top = self.rect.bottom
            print("BOTTOM")
        elif r.left == self.rect.left and r.height > r.width:
            if mario.direction == D_RIGHT:
                self.collide_right()
            if not self.transparent:
                mario.new_rect.right = self.rect.left
            print("RIGHT")
        elif r.right == self.rect.right and r.height > r.width:
            if mario.direction == D_LEFT:
                self.collide_left()
            if not self.transparent:
                mario.new_rect.left = self.rect.right
            print("LEFT")
        elif r.top == self.rect.top and r.width > r.height:
            if not self.transparent:
                mario.new_rect.bottom = self.rect.top
            print("TOP")
        else:
            #print("SKIP:", self.rect, mario.rect, r)
            pass

    def anim(self):
        self.image = self.images[self.f // OBJ_ANIM_SPEED]
        self.f += 1
        if self.f // OBJ_ANIM_SPEED >= len(self.images):
            self.f = 0


question_imgs = [pygame.image.load('images\\obj\\q' + str(i+1) + '.png').convert_alpha() for i in range(3)]
brick_img = pygame.image.load('images\\obj\\brick.png').convert_alpha()
question_dis_img = pygame.image.load('images\\obj\\q0.png').convert_alpha()
ground_img = pygame.image.load('images\\ground.png').convert_alpha()
pipe_img = pygame.image.load('images\\obj\\pipe1.png').convert_alpha()
pipe2_img = pygame.image.load('images\\obj\\pipe2.png').convert_alpha()
cinder_img = pygame.image.load('images\\obj\\cinder.png').convert_alpha()
flagstick_img = pygame.image.load('images\\obj\\flagstick.png').convert_alpha()
castle1_img = pygame.image.load('images\\obj\\castle1.png').convert_alpha()
castle2_img = pygame.image.load('images\\obj\\castle2.png').convert_alpha()
flag_img = pygame.image.load('images\\obj\\flag.png').convert_alpha()
flagstickball_img = pygame.image.load('images\\obj\\flagstickball.png').convert_alpha()
coin_imgs = [pygame.image.load('images\\obj\\coin' + str(i+1) + '.png').convert_alpha() for i in range(4)]
goomba_imgs = [pygame.image.load('images\\obj\\goomba' + str(i+1) + '.png').convert_alpha() for i in range(2)]

class Question(Obj):
    def __init__(self, x, y, t):
        Obj.__init__(self, question_imgs, x, y)
        self.type = t

    def collide_bottom(self):
        if not self.disabled:
            animGroup.remove(self)
            self.image = question_dis_img
            self.disabled = True
            xc,yc = self.rect.midtop
            if self.type == T_COIN:
                Coin(xc-8, yc)


class Coin(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, coin_imgs, x, y)
        self.animf = 0

    def anim(self):
        Obj.anim(self)
        self.animf += 1
        if self.animf <= 25:
            self.rect = self.rect.move(0, -2)
        else:
            self.rect = self.rect.move(0, 2)
        if self.animf == 50:
            self.animf = 0
            self.kill()
        

class Brick(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [brick_img], x, y)

    def collide_bottom(self):
        if mario.big:
            self.kill()  # удаляем из всех групп


class Cinder(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [cinder_img], x, y)


class Flagstick(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [flagstick_img], x, y)
        self.transparent = True


class Flagstickball(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [flagstickball_img], x, y)
        self.transparent = True


class Flag(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [flag_img], x, y)
        self.transparent = True


class Castle(Obj):
    def __init__(self, x, y, t):
        if t == 1:
            castle = castle1_img
        else:
            castle = castle2_img
        Obj.__init__(self, [castle], x, y)
        self.transparent = True


class Pipe(Obj):
    def __init__(self, x, y, a, t):
        if a == 0:
            img = pipe_img
        elif a == 1:
            img = pipe2_img
        Obj.__init__(self, [img], x, y)


class Ground(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, [ground_img], x, y + 32)


class MarioRect(Sprite):
    # Нужен для проверки нахождения на поверхности
    def __init__(self):
        Sprite.__init__(self)
        self.rect = mario.rect


# TODO
class Goomba(Obj):
    def __init__(self, x, y, d):
        Obj.__init__(self, goomba_imgs, x, y)
        self.direction = d

    def anim(self):
        if self.direction == D_RIGHT:
            self.rect = self.rect.move(10, 0)
        else:
            self.rect = self.rect.move(-10, 0)


class Mario(Sprite):
    def __init__(self, x, y, files):
        Sprite.__init__(self)
        ''' Картинки: '''
        self.sprites = {}
        for t in files:
            self.sprites[t] = []
            for ar in files[t]:
                self.sprites[t].append(pygame.image.load(ar).convert_alpha())
        self.f = 0

        self.image = self.sprites['AR'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.moving = False
        self.jumping = False
        self.direction = D_RIGHT
        self.velocity = 0
        self.big = False
        self.dead = False

        # После столкновения могут измениться
        self.new_rect = self.rect
        self.new_velocity = 0

    def die(self):
        self.dead = True

    def jump(self, vel):
        if self.jumping:  # усиленный прыжок, если долго держать кнопку
            if self.velocity < 0 and vel == -10:
                self.velocity -= 0.7
        else:
            self.jumping = True
            self.velocity = vel

    def move_left(self):
        self.rect.left -= SPEED * 2
        if self.rect.left < 0:
            self.rect.left = 0
        self.direction = D_LEFT
        self.moving = True

    def move_right(self):
        self.rect.left += SPEED * 2
        if self.rect.right > SCENE_WIDTH:
            self.rect.right = SCENE_WIDTH
        self.direction = D_RIGHT
        self.moving = True

    def get_x(self):
        x = self.rect.left + self.rect.width / 2  # середина марио
        x = WORLD_WIDTH/2 - x  # начало сцены
        if x > 0:
            x = 0
        if x < WORLD_WIDTH - SCENE_WIDTH:
            x = WORLD_WIDTH - SCENE_WIDTH
        return x

    def process_jumping(self):
        ''' Прыжки '''
        if self.jumping:
            self.rect.top = self.rect.top + self.velocity
            self.velocity += 1

    def process_move(self):
        # Смотрим стоит ли Марио на земле (его копию переместим на пиксель вниз):
        mario_rect.rect = mario.rect.copy().move(0, 1)
        bl = pygame.sprite.spritecollide(mario_rect, objGroup, False)
        mario_stand = False
        for b in bl:
            if not b.transparent:
                r = mario_rect.rect.clip(b.rect)
                if r.width > 5:
                    mario_stand = True
                    if mario.velocity >= 0 and mario.jumping:
                        mario.jumping = False
        if not mario_stand:
            mario.jump(0)

        ''' Марио упал вниз '''
        if self.rect.top > WORLD_HEIGHT:
            self.die()

    def draw(self):
        if self.jumping:
            if self.direction == D_RIGHT:
                sprite = 'CR'
            else:
                sprite = 'CL'
        elif self.moving:
            if self.direction == D_RIGHT:
                sprite = 'BR'
            else:
                sprite = 'BL'
        else:
            if self.direction == D_RIGHT:
                sprite = 'AR'
            else:
                sprite = 'AL'
        if self.big:
            sprite = 'Big' + sprite

        f = (self.f // SPEED) % len(self.sprites[sprite])

        self.f += 1
        if self.f > len(self.sprites[sprite]) * SPEED:
            self.f = 0

        l, b = self.rect.bottomleft
        self.image = self.sprites[sprite][f]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = l, b
        screen.blit(self.image, self.rect.topleft)


mario = Mario(4000, 360, {
    'AR': ['images\\marioAR.png'],
    'AL': ['images\\marioAL.png'],
    'BR': ['images\\marioBR1.png', 'images\\marioBR2.png', 'images\\marioBR1.png', 'images\\marioBR3.png'],
    'BL': ['images\\marioBL1.png', 'images\\marioBL2.png', 'images\\marioBL1.png', 'images\\marioBL3.png'],
    'CL': ['images\\marioCL.png'],
    'CR': ['images\\marioCR.png'],
    'BigAR': ['images\\marioBigAR.png'],
    'BigAL': ['images\\marioBigAL.png'],
    'BigBR': ['images\\marioBigBR1.png', 'images\\marioBigBR2.png', 'images\\marioBigBR1.png', 'images\\marioBigBR3.png'],
    'BigBL': ['images\\marioBigBL1.png', 'images\\marioBigBL2.png', 'images\\marioBigBL1.png', 'images\\marioBigBL3.png'],
    'BigCL': ['images\\marioBigCL.png'],
    'BigCR': ['images\\marioBigCR.png'],
    })

mario_rect = MarioRect()

world = World()
world.init()

pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock()

status = pygame.Surface((20, 20))

inGame = True
while inGame:
    mario.moving = False
    if mario.dead:
        inGame = False
        pygame.quit()
        sys.exit()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            inGame = False
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mario.move_left()
    if keys[pygame.K_RIGHT]:
        mario.move_right()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        mario.jump(-10)
    if keys[pygame.K_0]:
        mario.big = True
    mario.process_jumping()

    # Рисуем фон
    screen.blit(screenbg, (0, 0))

    ''' Обрабатываем столкновения с другими объектами '''
    mario.new_rect = pygame.Rect(mario.rect)
    mario.new_velocity = mario.velocity
    blocks = pygame.sprite.spritecollide(mario, actionGroup, False)
    for block in blocks:
        block.collide()
    # После столкновения могут измениться координаты и ускорение
    if len(blocks) > 0:
        mario.rect = pygame.Rect(mario.new_rect)
        mario.velocity = mario.new_velocity

    # Смотрим падения, столкновения с землей
    mario.process_move()

    ''' Вызываем анимацию анимированных объектов '''
    for a in animGroup:
        a.anim()

    ''' Рисуем все остальные объекты '''
    objGroup.draw(screen)

    ''' Рисуем марио '''
    mario.draw()

    window.blit(screen, (mario.get_x(), 0))

    # window.blit(status, (10, 10))

    pygame.display.flip()

    clock.tick(50)

