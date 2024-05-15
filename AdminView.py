import pygame


class AdminView:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("관리자 홈")
        self.font = pygame.font.SysFont("d2coding", 32)
        self.text_color = pygame.Color('black')

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