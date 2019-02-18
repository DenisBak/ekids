import pygame

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mario")

screen = pygame.Surface((800, 600))

SPEED = 3
D_RIGHT = 1
D_LEFT = 0
D_DOWN = 1
D_UP = 0


class Mario:
    def __init__(self, x, y, files):
        self.x = x
        self.y = y
        ''' Картинки: '''
        self.ar = []
        self.al = []
        self.br = []
        self.bl = []
        for ar in files['AR']:
            self.ar.append(pygame.image.load(ar).convert_alpha())
        for al in files['AL']:
            self.al.append(pygame.image.load(al).convert_alpha())
        for br in files['BR']:
            self.br.append(pygame.image.load(br).convert_alpha())
        for bl in files['BL']:
            self.bl.append(pygame.image.load(bl).convert_alpha())
        self.f = 0
        self.jf = 0

        self.moving = False
        self.jumping = False
        self.direction = D_RIGHT
        self.vDirection = D_DOWN
        self.velocity = 0

    def jump(self):
        if self.jumping:
            return
        self.vDirection = D_UP
        self.jumping = True
        self.jf = 0
        self.velocity = -10

    def draw(self):
        if self.moving:
            if self.direction == D_RIGHT:
                f = (self.f // SPEED) % len(self.br)
                screen.blit(self.br[f], (self.x, self.y))
            else:
                f = (self.f // SPEED) % len(self.bl)
                screen.blit(self.bl[f], (self.x, self.y))
        else:
            if self.direction == D_RIGHT:
                f = (self.f // SPEED) % len(self.ar)
                screen.blit(self.ar[f], (self.x, self.y))
            else:
                f = (self.f // SPEED) % len(self.al)
                screen.blit(self.al[f], (self.x, self.y))
        self.f += 1
        if self.f > len(self.br) * SPEED:
            self.f = 0
        ''' Прыжки '''
        if self.jumping:
            self.jf += 1
            if self.vDirection == D_UP:
                self.y = self.y + self.velocity
            self.velocity += 1
            if self.jf == 21:
                self.jumping = False


mario = Mario(10, 200, {'AR': ['images\\marioAR.png'],
                        'AL': ['images\\marioAL.png'],
                        'BR': ['images\\marioBR1.png', 'images\\marioBR2.png', 'images\\marioBR3.png'],
                        'BL': ['images\\marioBL1.png', 'images\\marioBL2.png', 'images\\marioBL3.png']})

pygame.key.set_repeat(1, 1)
clock = pygame.time.Clock()

status = pygame.Surface((20,20))

inGame = True
while inGame:
    mario.moving = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            inGame = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                status.fill((255,0,0))
            elif e.key == pygame.K_RIGHT:
                status.fill((0,255,0))
            else:
                status.fill((0,0,255))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mario.x -= SPEED * 2
            mario.direction = D_LEFT
            mario.moving = True
        if keys[pygame.K_RIGHT]:
            mario.x += SPEED * 2
            mario.direction = D_RIGHT
            mario.moving = True
        if keys[pygame.K_SPACE]:
            mario.jump();

    screen.fill((100, 100, 255))

    mario.draw()

    window.blit(screen, (0,0))
    window.blit(status, (10,10))

    pygame.display.flip()

    clock.tick(30)

