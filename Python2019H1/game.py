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
D_DOWN = 1
D_UP = 0
T_COIN = 1
OBJ_ANIM_SPEED = 10

groundGroup = Group()
animGroup = Group()
actionGroup = Group()

gndtpl = [1 for i in range(69)] + [0 for i in range(2)] + [1 for i in range(15)] + [0 for i in range(3)] \
         + [1 for i in range(64)] + [0 for i in range(2)] + [1 for i in range(57)]
worldData = {
    'bg': {
        'hill1': [(i * 768*2, 400) for i in range(5)],
        'grass1': [(368 + i * 768*2, 400) for i in range(5)],
        'hill2': [(512 + i * 768*2, 400) for i in range(5)],
        'grass2': [(752 + i * 768*2, 400) for i in range(5)],
        'grass3': [(1326 + i * 768*2, 400) for i in range(5)],
    },
    'gnd': {
        'gnd': [(j*16*2, 400 + i * 16*2) if gndtpl[j] == 1 else (-1, -1) for i in range(2) for j in range(212)]
    },
    'obj': {
        'q': [(16, 3, T_COIN)]
    }
}


class World:
    def __init__(self):
        pass

    def init(self):
        screenbg.fill((107, 140, 255))
        for t in worldData:
            for w in worldData[t]:
                for c in worldData[t][w]:
                    if t == 'bg':
                        x, y = c
                        img = pygame.image.load('images\\bg\\' + w + '.png').convert_alpha()
                        y = y - img.get_rect().height
                        screenbg.blit(img, (x, y))
                    elif t == 'gnd':
                        x, y = c
                        if x >= 0 and y >= 0:
                            Ground(x, y)
                    elif t == 'obj':
                        x, y, t = c
                        if x >= 0 and y >= 0:
                            if t == T_COIN:
                                Question(x * 16 * 2, 400 - y * 16 * 2)


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
        self.add(groundGroup)
        self.add(actionGroup)
        self.rect.bottomleft = x, y
        self.disabled = False

    def collide_bottom(self):
        pass

    ''' Вызывается, когда Марио столкнулся с объектом '''
    def collide(self):
        # Марио двигается вверх

        if (self.rect.bottom > mario.rect.top) and (mario.velocity < 0) and (self.rect.bottom <= mario.rect.top - mario.velocity):
            self.collide_bottom()
            mario.velocity = 0
            mario.rect.top = self.rect.bottom
        # Марио двигается вправо и врезается в объект
        elif (self.rect.left < mario.rect.right) and (self.rect.left >= mario.prev_rect.right):
            mario.rect.right = self.rect.left
        # Марио двигается влево и врезается в объект
        elif (self.rect.right > mario.rect.left) and (self.rect.right <= mario.prev_rect.left):
            mario.rect.left = self.rect.right

    def anim(self):
        self.image = self.images[self.f // OBJ_ANIM_SPEED]
        self.f += 1
        if self.f // OBJ_ANIM_SPEED >= len(self.images):
            self.f = 0


question_imgs = [pygame.image.load('images\\obj\\q' + str(i+1) + '.png').convert_alpha() for i in range(3)]
question_dis_img = pygame.image.load('images\\obj\\q0.png').convert_alpha()
ground_img = pygame.image.load('images\\ground.png').convert_alpha()


class Question(Obj):
    def __init__(self, x, y):
        Obj.__init__(self, question_imgs, x, y)

    def collide_bottom(self):
        if not self.disabled:
            animGroup.remove(self)
            self.image = question_dis_img
            self.disabled = True


class Ground(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.add(groundGroup)


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
        self.jf = 0

        self.image = self.sprites['AR'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.moving = False
        self.jumping = False
        self.direction = D_RIGHT
        self.velocity = 0.0
        self.big = False
        self.dead = False
        self.prev_rect = self.rect

    def die(self):
        self.dead = True

    def jump(self, vel):
        if self.jumping:  # усиленный прыжок, если долго держать кнопку
            if self.velocity < 0 and vel == -10:
                self.velocity -= 0.7
        else:
            self.jumping = True
            self.jf = 0
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

    def draw(self):
        sprite = ''
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

        blocks = pygame.sprite.spritecollide(mario, groundGroup, False)
        if len(blocks) == 0:
            self.jump(0)  # падение
            
        ''' Прыжки '''
        if self.jumping:
            self.jf += 1
            self.rect.top = self.rect.top + self.velocity

            blocks = pygame.sprite.spritecollide(mario, groundGroup, False)
            if len(blocks) > 0:
                if self.velocity >= 0:
                    for block in blocks:
                        if self.rect.bottom > block.rect.top and self.rect.bottom - block.rect.top <= self.velocity:
                            self.rect.bottom = block.rect.top + 1
                            self.jumping = False

            self.velocity += 1

        ''' Марио упал вниз '''
        if self.rect.top > WORLD_HEIGHT:
            mario.die()

        l, b = self.rect.bottomleft
        self.image = self.sprites[sprite][f]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = l, b
        screen.blit(self.image, self.rect.topleft)


mario = Mario(300, 360, {'AR': ['images\\marioAR.png'],
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

world = World()
world.init()

pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock()

status = pygame.Surface((20, 20))

inGame = True
while inGame:
    mario.moving = False
    mario.prev_rect = pygame.Rect(mario.rect)
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

    screen.blit(screenbg, (0, 0))

    groundGroup.draw(screen)

    blocks = pygame.sprite.spritecollide(mario, actionGroup, False)
    for b in blocks:
        b.collide()

    ''' Вызываем анимацию анимированных объектов '''
    for a in animGroup:
        a.anim()
    animGroup.draw(screen)

    mario.draw()

    window.blit(screen, (mario.get_x(), 0))

    # window.blit(status, (10, 10))

    pygame.display.flip()

    clock.tick(50)

