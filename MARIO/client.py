# Импортируем библиотеки

import  sys, os
import pygame
import hero
import blocks
import  time

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


def main():
    pygame.init() # инициация PyGame
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Mario Boy")
    BACKGROUND = pygame.image.load(os.path.join('fon','Afternoon.jpg')).convert()


    timer = pygame.time.Clock()

    level = [
       "----------------------------------",
       "-                                -",
       "-                       --       -",
       "-                                -",
       "-            --                  -",
       "-                                -",
       "--                               -",
       "-                                -",
       "-                   ----     --- -",
       "-                                -",
       "--                               -",
       "-                                -",
       "-                            --- -",
       "-                                -",
       "-                                -",
       "-      ---                       -",
       "-                                -",
       "-   -------         ----         -",
       "-                                -",
       "-                         -      -",
       "-                            --  -",
       "-                                -",
       "-                                -",
       "----------------------------------"]


    player =  hero.Hero(40, 50) # создаем персонажа по (x,y) координатам
    left = right = False    # по умолчанию — стоим
    up = False

    player2 = hero.Hero(70, 40)

    entities = pygame.sprite.Group() # все объекты
    platforms = [] # поверхности
    entities.add(player)
    entities.add(player2)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    x=y=0 # координаты
    for row in level: # вся строка
            for col in row: # каждый символ
                if col == "-":
                    pf = blocks.Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    #то же самое и с высотой
            x = 0

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    TimeFor = time.time()
    ff = True
    while 1: # основной цикл программы
        timer.tick(60)

        if time.time() - TimeFor > 4:
            if ff:
                BACKGROUND = pygame.image.load(os.path.join('fon','Morning.jpg')).convert()
                ff = False
            else:
                BACKGROUND = pygame.image.load(os.path.join('fon','Late Afternoon.jpg')).convert()
                ff = True
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

        screen.blit(BACKGROUND, (0,0))      # каждую итерацию необходимо всё перерисовывать


                        #на каждой новой строчке начинаем с нуля

        camera.update(player)
        player.update(left,right, up, platforms)

        mes = list(UDP.DOWN())
        if mes[0] == 0:
            SL = False
        else:
            SL= True

        if mes[0] == 0:
            SR = False
        else:
            SR = True

        if mes[0] == 0:
            SUp = False
        else:
            SUp = True


        player2.update(SL,SR, SUp, platforms)

        #player.draw(screen)
        #player.collide(screen)
        #entities.draw(screen)

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()     # обновление и вывод всех изменений на экран



if __name__ == "__main__":
    main()
