import sys, pygame, os

WIDTH = 900
HEIGHT = 450
DISPLAY = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(DISPLAY)

speed = [2, 2]
black = 0, 0, 0
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

timer = pygame.time.Clock()

pygame.mixer.init()
music = pygame.mixer.music.load('gun1.wav')


while 1:
    timer.tick(80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > WIDTH:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > HEIGHT:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()