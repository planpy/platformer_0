# Импортируем библиотеки

import  sys, os
import pygame
import hero
import blocks
import  time
import  monsters
#Объявляем переменные
WIN_WIDTH = 900 #ширина создаваемого окна
WIN_HEIGHT = 500 # высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # группируем ширину и высоту в переменную

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)



def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)

def RFon(Nfon):
    if Nfon == 0:
        return pygame.image.load(os.path.join('fon','0.jpg')).convert()
    elif Nfon == 1:
        return pygame.image.load(os.path.join('fon','1.jpg')).convert()
    elif Nfon == 2:
        return pygame.image.load(os.path.join('fon','2.jpg')).convert()
    elif Nfon == 3:
        return pygame.image.load(os.path.join('fon','3.jpg')).convert()
    elif Nfon == 4:
        return pygame.image.load(os.path.join('fon','4.jpg')).convert()
    elif Nfon == 5:
        return pygame.image.load(os.path.join('fon','5.jpg')).convert()
    elif Nfon == 6:
        return pygame.image.load(os.path.join('fon','6.jpg')).convert()
    elif Nfon == 7:
        return pygame.image.load(os.path.join('fon','7.jpg')).convert()

def main():
    pygame.init() # инициация PyGame
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Mario Boy")
    BACKGROUND = pygame.image.load(os.path.join('fon','0.jpg')).convert()


    timer = pygame.time.Clock()

    level = [
       "--------------------------------------",
       "-                                    -",
       "-      --               -            -",
       "-                                    -",
       "-            --                      -",
       "-                      -             -",
       "--                          ------   -",
       "-                             Z      -",
       "-   -               ----     ---     -",
       "-                                    -",
       "--       --                     --   -",
       "-                 --                 -",
       "-                            ---     -",
       "- --          --                     -",
       "-                           --     ---",
       "-      ---              *            -",
       "-                             *      -",
       "-   -------         ----             -",
       "-                                    -",
       "-                         -          -",
       "--                          --      -",
       "----       *                         -",
       "-                                    -",
       "--------------------------------------"]


    player =  hero.Hero(40, 50) # создаем персонажа по (x,y) координатам
    left = right = False    # по умолчанию — стоим
    up = False

    player2 = hero.Hero(70, 40)

    entities = pygame.sprite.Group() # все объекты
    platforms = [] # проверка на поверхность
    entities.add(player)

    entities.add(player2)

    animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя

    tp = blocks.BlockTeleport(128,512,800,64)
    entities.add(tp)
    platforms.append(tp)
    animatedEntities.add(tp)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    x=y=0 # координаты
    for row in level: # вся строка
            for col in row: # каждый символ
                if col == "-":
                    pf = blocks.Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)
                if col == "*":
                    bd = blocks.BlockDie(x,y)
                    entities.add(bd)
                    platforms.append(bd)
                if col == "Z":
                    pr = blocks.Emblem(x,y)
                    entities.add(pr)
                    platforms.append(pr)
                    animatedEntities.add(pr)

                x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    #то же самое и с высотой
            x = 0

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    TimeFor = time.time()
    ff = True

    running = False
    NFOn = 1

    Nmonsters = pygame.sprite.Group() # Все передвигающиеся объекты
    mn1 = monsters.Monster(190,200,2,3,150,15)

    mn2 = monsters.Monster(344,511,0,1,0,150)

    entities.add(mn1)
    platforms.append(mn1)
    Nmonsters.add(mn1)

    entities.add(mn2)
    platforms.append(mn2)
    Nmonsters.add(mn2)

    while not player.winner: # основной цикл программы
        timer.tick(60)

        if time.time() - TimeFor > 5:
            if NFOn <8:
                BACKGROUND = RFon(NFOn)
                TimeFor = time.time()
                NFOn += 1
            else:
                NFOn = 0
                BACKGROUND = RFon(NFOn)
                TimeFor = time.time()

        for e in pygame.event.get(): # обрабатываем события
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type ==  pygame.KEYDOWN and e.key ==   pygame.K_LEFT:
               left = True
            if e.type ==   pygame.KEYDOWN and e.key ==   pygame.K_RIGHT:
               right = True
            if e.type ==   pygame.KEYUP and e.key ==   pygame.K_RIGHT:
               right = False
            if e.type ==   pygame.KEYUP and e.key ==  pygame.K_LEFT:
                left = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up = True
            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LSHIFT:
                running = True
            if e.type == pygame.KEYUP and e.key == pygame.K_LSHIFT:
                running = False

        screen.blit(BACKGROUND, (0,0))      # каждую итерацию необходимо всё перерисовывать


                        #на каждой новой строчке начинаем с нуля

        camera.update(player)
        player.update(left,right, up, running,platforms)

       # player2.update(left,right, up, platforms)

        #player.draw(screen)
        #player.collide(screen)
        #entities.draw(screen)

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        animatedEntities.update() # показываем анимацию
        Nmonsters.update(platforms) # передвигаем всех монстров


        pygame.display.update()     # обновление и вывод всех изменений на экран



if __name__ == "__main__":
    main()
