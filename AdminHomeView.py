import pygame


class AdminHomeView:
    def __init__(self):
        add_button = pygame.Rect(100, 100, 100, 50)
        del_button = pygame.Rect(100, 200, 100, 50)
        edit_button = pygame.Rect(100, 300, 100, 50)

    # def run(self):
    #     done = False
    #     while not done:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 done = True
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 if add_button.collidepoint(event.pos):
    #                     print("추가 버튼 클릭")
    #                 elif del_button.collidepoint(event.pos):
    #                     print("삭제 버튼 클릭")
    #                 elif edit_button.collidepoint(event.pos):
    #                     print("수정 버튼 클릭")
    #         pygame.display.flip()
    #