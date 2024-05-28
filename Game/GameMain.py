import pygame
import os
import sys
from Game.GameRectangle import Rectangle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game', 'Acid_Rain')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Game', 'Card_Flip')))
from Game.Card_Flip import Card_Flip_main
from Game.Acid_Rain import Acid_Rain_main

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# 메인 루프
def game_main(user_id):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption('Game Select')
    card_flip_start = Card_Flip_main
    acid_rain_start = Acid_Rain_main
    gameContinue = True

    card_width = 250
    card_height = 150

    center_x = screen_width // 2
    center_y = screen_height // 2
    margin = 30

    acid_rain_rect = Rectangle(center_x - card_width - margin, center_y - card_height // 2, card_width, card_height, GRAY,10)
    acid_rain_rect.set_text("산성비", BLACK, 30)

    card_flip_rect = Rectangle(center_x + margin, center_y - card_height // 2, card_width, card_height, GRAY, 10)
    card_flip_rect.set_text("카드 뒤집기", BLACK, 30)

    homeButton = Rectangle(screen_width - 70, screen_height - 70, 50, 50, GRAY)
    current_dir = os.path.dirname(__file__)
    homeButton.set_image(os.path.join(current_dir, 'Card_Flip','assets', 'home.png'))


    while gameContinue :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameContinue = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if homeButton.is_collide(event.pos):
                    gameContinue = False
                if acid_rain_rect.is_collide(event.pos):
                    acid_rain_start.acid_rain_main(user_id)
                if card_flip_rect.is_collide(event.pos):
                    card_flip_start.card_flip_main(user_id)

        # 화면을 하얀색으로 채우기
        screen.fill(WHITE)

        # 버튼을 그리기
        mouse_pos = pygame.mouse.get_pos()
        acid_rain_rect.is_hover(mouse_pos)
        card_flip_rect.is_hover(mouse_pos)
        homeButton.is_hover(mouse_pos)

        acid_rain_rect.draw(screen)
        card_flip_rect.draw(screen)
        homeButton.draw(screen)

        # 화면 업데이트
        pygame.display.flip()


if __name__ == '__main__':
    game_main("146") #jun의 id