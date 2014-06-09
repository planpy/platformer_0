import pygame
import  sys

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("UFO Fire")

pygame.mouse.set_visible(0)
timer = pygame.time.Clock()
timer.tick(60)

ship = pygame.image.load("UFO.png")
ship_top = screen.get_height() - ship.get_height()
ship_left = screen.get_width() / 2 - ship.get_width()/2

screen.blit(ship, (ship_left, ship_top) )

BFon = pygame.image.load('fon.png')
BFonRect = BFon.get_rect()

shot = pygame.image.load("shoot.png")
shoot_y = 0

pygame.mixer.init()
music = pygame.mixer.music.load('gun1.wav')

while True:
    timer.tick(80)

    screen.blit(BFon, BFonRect)

    x,y = pygame.mouse.get_pos()
    screen.blit(ship, (x-ship.get_width()/ 4, ship_top))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot_y = 350
            shoot_x = x
            pygame.mixer.music.play()

    if shoot_y > 0:
        screen.blit(shot, (shoot_x, shoot_y))
        shoot_y -= 21

    pygame.display.flip()
