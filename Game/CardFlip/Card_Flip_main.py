import pygame
from Game.StartScreen import StartScreen
from Game.ShowResult import ShowResult
from Game.CardFlip.CardFlipModel import CardFlipModel
from Game.CardFlip.CardFlipView import CardFlipView
from Game.CardFlip.CardFlipController import CardFlipController


# 메인 루프
def card_flip_main(user_id, username):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('카드 뒤집기 게임')
    model = CardFlipModel()
    view = CardFlipView(screen, model)
    controller = CardFlipController(model, view)
    start_screen = StartScreen(screen, user_id, username)
    gameContinue = start_screen.card_start()

    # 게임 시작 시간 기록
    model.start_timer()

    while gameContinue:
        for event in pygame.event.get():
            gameContinue = controller.handle_event(event)
            if(not gameContinue):
                break
        view.draw()
        pygame.time.Clock().tick(30)

        # 게임이 종료되면 루프를 벗어남
        if model.is_won():
            elapsed_time = model.get_elapsed_time()
            result_viewer = ShowResult(screen, 800, 600)
            TF = result_viewer.show_time_result(elapsed_time, user_id, username)
            if TF:
                card_flip_main(user_id, username)
            break

    # 게임 종료 시간 기록


if __name__ == '__main__':
    card_flip_main(146, "Jun") #jun의 id