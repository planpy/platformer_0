import pygame
import  os
import pyganim
import  blocks
import monsters

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR =255, 255, 128

MOVE_EXTRA_SPEED = 2.5 # Ускорение
JUMP_EXTRA_POWER = 1 # дополнительная сила прыжка
ANIMATION_SUPER_SPEED_DELAY = 0.05 # скорость смены кадров при ускорении

JUMP_POWER = 10
GRAVITY = 0.5 # Сила, которая будет тянуть нас вниз

ANIMATION_DELAY = 0.1 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
            ('%s/mario/r2.png' % ICON_DIR),
            ('%s/mario/r3.png' % ICON_DIR),
            ('%s/mario/r4.png' % ICON_DIR),
            ('%s/mario/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
            ('%s/mario/l2.png' % ICON_DIR),
            ('%s/mario/l3.png' % ICON_DIR),
            ('%s/mario/l4.png' % ICON_DIR),
            ('%s/mario/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, 0.1)]

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # начальная позиция Х
        self.startY = y
        self.image = pygame.Surface((WIDTH,HEIGHT))
        self.image.fill( COLOR)
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект

        self.yvel = 0
        self.onGround = False

        self.image.set_colorkey(COLOR) # делаем фон прозрачным
        # Анимация движения вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()

#        Анимация движения влево
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()


        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-умолчанию, стоим

        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

        self.winner = False


    def update(self,  left, right, up,  running, platforms):
        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if running and (left or right): # если есть ускорение и мы движемся
                    self.yvel -= JUMP_EXTRA_POWER # то прыгаем выше
                self.image.fill(COLOR)
                self.boltAnimJump.blit(self.image, (0, 0))



        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image.fill(COLOR)
            if running: # если усkорение
                self.xvel-=MOVE_EXTRA_SPEED # то передвигаемся быстрее
                if not up: # и если не прыгаем
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0)) # то отображаем быструю анимацию
            else: # если не бежим
                if not up: # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0)) # отображаем анимацию движения
            if up: # если же прыгаем
                    self.boltAnimJumpLeft.blit(self.image, (0, 0)) # отображаем анимацию прыжка

        if right:
            self.xvel = MOVE_SPEED # Право = x + n
            self.image.fill(COLOR)
            if running:
                self.xvel+=MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(COLOR)
                self.boltAnimStay.blit(self.image, (0, 0))


        if not self.onGround:
            self.yvel +=  GRAVITY

        self.onGround = False; # Мы не знаем, когда мы на земле((

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)
        #self.rect.y += self.yvel

        #self.rect.x += self.xvel # переносим свои положение на xvel

    #def draw(self, screen): # выводим себя на экран
       # screen.blit(self.image, (self.rect.x,self.rect.y))
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх
                    self.yvel = 0                 # и энергия прыжка пропадает

                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster): # если пересекаемый блок - blocks.BlockDie
                    self.die()# умираем
                elif isinstance(p, blocks.BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, blocks.Emblem): # если коснулись эмблемы
                    self.winner = True # победа!

    def die(self):
        pygame.time.wait(500)
        self.teleporting(self.startX, self.startY) # перемещаемся в начальные координаты
    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
