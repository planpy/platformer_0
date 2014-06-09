# Импортируем библиотеки
import  sys, os
import pygame


#Объявляем переменные
WIN_WIDTH = 900 #ширина создаваемого окна
WIN_HEIGHT = 500 # высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # группируем ширину и высоту в переменную

def main():
    pygame.init() # инициация PyGame
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Mario Boy")
    BACKGROUND = pygame.image.load(os.path.join('fon','Afternoon.jpg')).convert()


    while 1: # основной цикл программы
        for e in pygame.event.get(): # обрабатываем события
            if e.type == pygame.QUIT:
                sys.exit()
        screen.blit(BACKGROUND, (0,0))      # каждую итерацию необходимо всё перерисовывать
        pygame.display.update()     # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
