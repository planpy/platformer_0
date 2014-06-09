# Импортируем библиотеки

import  sys, os
import pygame
import hero
import blocks
import  time
import  monsters

pygame.init()
#Объявляем переменные
WIN_WIDTH = 950 #ширина создаваемого окна
WIN_HEIGHT = 500 # высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # группируем ширину и высоту в переменную

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

FILE_DIR = os.path.dirname(__file__)

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


def loadLevel():
    global playerX, playerY # объявляем глобальные переменные, это координаты героя

    levelFile = open('%s/levels/1.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/": # пока не нашли символ завершения файла
        line = levelFile.readline() #считываем построчно
        if line[0] == "[": # если нашли символ начала уровня
            while line[0] != "]": # то, пока не нашли символ конца уровня
                line = levelFile.readline() # считываем построчно уровень
                if line[0] != "]": # и если нет символа конца уровня
                    endLine = line.find("|") # то ищем символ конца строки
                    level.append(line[0: endLine]) # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "": # если строка не пустая
         commands = line.split() # разбиваем ее на отдельные команды
         if len(commands) > 1: # если количество команд > 1, то ищем эти команды
            if commands[0] == "player": # если первая команда - player
                playerX= int(commands[1]) # то записываем координаты героя
                playerY = int(commands[2])
            if commands[0] == "portal": # если первая команда portal, то создаем портал
                tp = blocks.BlockTeleport(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]))
                entities.add(tp)
                platforms.append(tp)
                animatedEntities.add(tp)
            if commands[0] == "monster": # если первая команда monster, то создаем монстра
                mn = monsters.Monster(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]),int(commands[5]),int(commands[6]))
                entities.add(mn)
                platforms.append(mn)
                MasMons.add(mn)



def main():
    loadLevel()
    pygame.init() # инициация PyGame
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Mario Boy")
    BACKGROUND = pygame.image.load(os.path.join('fon','0.jpg')).convert()


    timer = pygame.time.Clock()

    #level = []


    player =  hero.Hero(playerX, playerX) # создаем персонажа по (x,y) координатам
    left = right = False    # по умолчанию — стоим
    up = False

    player2 = hero.Hero(playerX, playerX)

    entities = pygame.sprite.Group() # все объекты
    platforms = [] # проверка на поверхность
    entities.add(player)

    entities.add(player2)

    animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
    """
    tp = blocks.BlockTeleport(128,512,800,64)
    entities.add(tp)
    platforms.append(tp)
    animatedEntities.add(tp)
    """

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
                if col == "Z": #блок проверки
                    pr = blocks.Emblem(x,y)
                    entities.add(pr)
                    platforms.append(pr)
                    animatedEntities.add(pr)

                x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    #то же самое и с высотой
            x = 0

    total_level_width  = len(level[0])* PLATFORM_WIDTH# Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    TimeFor = time.time()
    ff = True

    running = False
    NFOn = 1
    """
    Nmonsters = pygame.sprite.Group() # Все передвигающиеся объекты
    mn = monsters.Monster(190,200,2,3,150,15)
    entities.add(mn)
    platforms.append(mn)
    Nmonsters.add(mn)
    """

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

        animatedEntities.update() # показываем анимацию
                        #на каждой новой строчке начинаем с нуля

        MasMons.update(platforms) # передвигаем всех монстров

        camera.update(player)

        player.update(left,right, up, running,platforms)

       # player2.update(left,right, up, platforms)

        #player.draw(screen)
        #player.collide(screen)
        #entities.draw(screen)

        for e in entities:
            screen.blit(e.image, camera.apply(e))



        pygame.display.update()     # обновление и вывод всех изменений на экран



level = []
entities = pygame.sprite.Group() # все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
MasMons = pygame.sprite.Group()
platforms = []


class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font=None, font_size=30,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            # Redraw the background
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()


if __name__ == "__main__":
    #main()
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Start', 'Quit')

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()
