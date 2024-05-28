import os
import pygame
from Button import Button
from Input import Input  # 검색 입력 필드를 위해 Input 클래스를 가져옵니다.

class BasicWordbookView:
    def __init__(self):
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("영어 단어장")

        self.font_large = pygame.font.SysFont("D2Coding", 20)
        self.font_small = pygame.font.SysFont("D2Coding", 15)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        star_filled_image_path = os.path.join(current_dir, "star_filled.png")
        star_empty_image_path = os.path.join(current_dir, "star_empty.png")
        home_image_path = os.path.join(current_dir, "home.png")

        self.star_filled_image = pygame.image.load(star_filled_image_path)
        self.star_filled_image = pygame.transform.scale(self.star_filled_image, (20, 20))

        self.star_empty_image = pygame.image.load(star_empty_image_path)
        self.star_empty_image = pygame.transform.scale(self.star_empty_image, (20, 20))

        self.home_image = pygame.image.load(home_image_path)
        self.home_image = pygame.transform.scale(self.home_image, (40, 40))

        # 홈 버튼 설정
        self.home_button_rect = pygame.Rect(self.SCREEN_WIDTH - 50, 10, 40, 40)

        # 새로운 버튼들을 생성하고 리스트에 저장
        self.prev_button = Button(pygame.Rect(20, self.SCREEN_HEIGHT - 50, 80, 40), "이전")
        self.next_button = Button(pygame.Rect(600, self.SCREEN_HEIGHT - 50, 80, 40), "다음")

        # 검색 입력 필드 및 버튼 추가
        self.search_box = Input("", self, pygame.Rect(250, 100, 200, 32))
        self.search_button = Button(pygame.Rect(470, 100, 80, 32), "검색")
        self.search_result = []

    def draw_text_centered(self, surface, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def display_page(self, page, word_data, total_pages, favorite_status, checkboxes):
        self.screen.fill((255, 255, 255))

        headers = ["No.", "단어", "뜻", "Lv."]
        header_positions = [(120, 180), (240, 180), (430, 180), (560, 180)]
        for header, pos in zip(headers, header_positions):
            header_text = self.font_large.render(header, True, pygame.Color('black'))
            header_rect = header_text.get_rect(center=pos)
            self.screen.blit(header_text, header_rect)

        for i, word in enumerate(word_data):
            text_y = 200 + i * 60
            star_image = self.star_filled_image if word['favorite'] else self.star_empty_image
            star_rect = pygame.Rect(60, text_y, 20, 20)
            self.screen.blit(star_image, star_rect)
            
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(100, text_y, 40, 30))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(150, text_y, 180, 30))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(340, text_y, 180, 30))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(530, text_y, 60, 30))

            index_text = self.font_large.render(str((page - 1) * 10 + i + 1), True, pygame.Color('black'))
            word_text = self.font_large.render(word['word'], True, pygame.Color('black'))
            meaning_text = self.font_small.render(word['mean'], True, pygame.Color('black')) if len(word['mean']) > 5 else self.font_large.render(word['mean'], True, pygame.Color('black'))
            
            level_text_str = ""
            if word['lv'] == 1:
                level_text_str = "초급"
            elif word['lv'] == 2:
                level_text_str = "중급"
            elif word['lv'] == 3:
                level_text_str = "고급"
            level_text = self.font_large.render(level_text_str, True, pygame.Color('black'))

            index_text_rect = index_text.get_rect(center=(120, text_y + 15))
            word_text_rect = word_text.get_rect(center=(240, text_y + 15))
            meaning_text_rect = meaning_text.get_rect(center=(430, text_y + 15))
            level_text_rect = level_text.get_rect(center=(560, text_y + 15))

            self.screen.blit(index_text, index_text_rect)
            self.screen.blit(word_text, word_text_rect)
            self.screen.blit(meaning_text, meaning_text_rect)
            self.screen.blit(level_text, level_text_rect)
        
        # 홈 버튼을 화면에 그림
        self.screen.blit(self.home_image, self.home_button_rect)
        
        # 새로운 버튼들을 화면에 그림
        self.prev_button.draw(self.screen)
        self.next_button.draw(self.screen)

        # 검색 입력 필드 및 버튼 그리기
        self.search_box.draw(self.screen)
        self.search_button.draw(self.screen)

        # 현재 페이지와 전체 페이지 표시
        page_info_text = f"{page} / {total_pages}"
        page_info_surface = self.font_large.render(page_info_text, True, pygame.Color('black'))
        page_info_rect = page_info_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
        self.screen.blit(page_info_surface, page_info_rect)

        for checkbox in checkboxes:
            checkbox.draw()
        
        pygame.display.flip()

    def draw_text(self, text, rect, align, font_size=20):
        font = pygame.font.SysFont("d2coding", font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        if align == 'left_out':
            text_rect = text_surface.get_rect(midleft=rect.midright)
        elif align == 'left_in':
            text_rect = text_surface.get_rect(midleft=rect.midleft)
        elif align == 'center':
            text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
