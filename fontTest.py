import sys

import pygame
from pygame.locals import QUIT

pygame.init()
SCREEN = pygame.display.set_mode((3024, 1964))
pygame.display.set_caption('한글폰트 확인')

sysFont = pygame.font.SysFont(None, 24)
txt = '한글'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for i, name in enumerate(pygame.font.get_fonts()):
        try:
            font = pygame.font.SysFont(name, 24)
        except:
            continue
        ln = len(name) * 12

        imgName = sysFont.render('%s:' % name, True, (255, 255, 255))
        try:
            imgTxt = font.render(txt, True, (255, 255, 255))
        except:
            continue
        x = i % 2 * 300
        y = i // 2 * 25

        SCREEN.blit(imgName, (x, y))
        SCREEN.blit(imgTxt, (x + ln, y))

    pygame.display.update()