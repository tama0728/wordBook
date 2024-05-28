import pygame
from Game.Acid_Rain.GameController import GameController

def acid_rain_main(user_id):
    pygame.init()
    screen_width = 800
    screen_height = 600
    controller = GameController(screen_width, screen_height)
    controller.run(user_id)

if __name__ == "__main__":
    acid_rain_main("146") #jun의 id
