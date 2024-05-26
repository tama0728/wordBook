import pygame
from Game.Acid_Rain.GameController import GameController

def acid_rain_main(username):
    pygame.init()
    screen_width = 800
    screen_height = 600
    controller = GameController(screen_width, screen_height)
    controller.run(username)

if __name__ == "__main__":
    acid_rain_main("jun")
