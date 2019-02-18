import pygame
from pygame.sprite import Sprite, Group
import sys

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Mario")

screen = pygame.Surface((640, 480))

SPEED = 3
D_RIGHT = 1
D_LEFT = 0
D_DOWN = 1
D_UP = 0

groundGroup = Group()


class Ground(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load('images\\ground.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.add(groundGroup);

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
        self.velocity = 0
        self.big = False

    def jump(self, vel):
        if self.jumping:
            return
        self.jumping = True
        self.jf = 0
        self.velocity = vel

    def draw(self):
        sprite = '';
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
            self.jump(0) # падение                
            
        ''' Прыжки '''
        if self.jumping:
            self.jf += 1
            self.rect.top = self.rect.top + self.velocity

            blocks = pygame.sprite.spritecollide(mario, groundGroup, False)
            if len(blocks) > 0:
                if self.velocity >= 0:
                    print(self.velocity, self.rect.bottom)
                    for block in blocks:
                        print(block.rect.top)
                        if self.rect.bottom > block.rect.top and self.rect.bottom - block.rect.top <= self.velocity:
                            self.rect.bottom = block.rect.top + 1
                            self.jumping = False
                            print(False)
            
            self.velocity += 1

        l,b = self.rect.bottomleft
        self.image = self.sprites[sprite][f]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = l,b
        screen.blit(self.image, self.rect.topleft)



for i in range(20):
    Ground(i*32, 480-32-16)
    Ground(i*32, 480-16)


mario = Mario(10, 200, {'AR': ['images\\marioAR.png'],
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

pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock()

status = pygame.Surface((20,20))

inGame = True
while inGame:
    mario.moving = False
    for e in pygame.event.get([pygame.QUIT]):
        if e.type == pygame.QUIT:
            inGame = False
            sys.exit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mario.rect.left -= SPEED * 2
        mario.direction = D_LEFT
        mario.moving = True
    if keys[pygame.K_RIGHT]:
        mario.rect.left += SPEED * 2
        mario.direction = D_RIGHT
        mario.moving = True
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        mario.jump(-10)
    if keys[pygame.K_0]:
        mario.big = True

    screen.fill((100, 100, 255))

    mario.draw()
    groundGroup.draw(screen)

    window.blit(screen, (0,0))
    window.blit(status, (10,10))

    pygame.display.flip()

    clock.tick(30)

