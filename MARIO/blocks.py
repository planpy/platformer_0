import os
import pygame
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
#BLOCKS = pygame.image.load(os.path.join('blocks','platform.png')).convert()

ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами


ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % ICON_DIR),
            ('%s/blocks/portal1.png' % ICON_DIR)]


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))

        #elf.image.blit(BLOCKS)
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.image = pygame.image.load("%s/blocks/platform.png" % ICON_DIR)


        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load("%s/blocks/dieBlock.png" % ICON_DIR)

class BlockTeleport(Platform):
    def __init__(self, x, y, goX,goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class Emblem(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x,y)
        self.image = pygame.image.load("%s/blocks/emblem.png" % ICON_DIR)

