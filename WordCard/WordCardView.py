import os

import pygame

from Api.Input import Input  # Assuming Input class is in the same directory


class WordCardView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("D2Coding", 48)
        self.font_small = pygame.font.SysFont("D2Coding", 28)
        self.font_tiny = pygame.font.SysFont("D2Coding", 18)

        # 이미지 로드
        current_dir = os.path.dirname(os.path.abspath(__file__))
        left_arrow_path = os.path.join(current_dir, "../Images/left_arrow.png")
        right_arrow_path = os.path.join(current_dir, "../Images/right_arrow.png")
        sound_path = os.path.join(current_dir, "../Images/sound.png")
        star_black_path = os.path.join(current_dir, "../Images/black_star.png")
        star_path = os.path.join(current_dir, "../Images/star.png")
        home_path = os.path.join(current_dir, "../Images/home.png")
        checkbox_checked_path = os.path.join(current_dir, "../Images/checkbox_unchecked.png")
        checkbox_unchecked_path = os.path.join(current_dir, "../Images/checkbox_checked.png")

        self.left_arrow = pygame.image.load(left_arrow_path).convert_alpha()
        self.left_arrow = pygame.transform.scale(self.left_arrow, (50, 50))
        self.right_arrow = pygame.image.load(right_arrow_path).convert_alpha()
        self.right_arrow = pygame.transform.scale(self.right_arrow, (50, 50))
        self.sound_icon = pygame.image.load(sound_path).convert_alpha()
        self.sound_icon = pygame.transform.scale(self.sound_icon, (50, 50))
        self.star_black = pygame.image.load(star_black_path).convert_alpha()
        self.star_black = pygame.transform.scale(self.star_black, (50, 50))
        self.star = pygame.image.load(star_path).convert_alpha()
        self.star = pygame.transform.scale(self.star, (50, 50))
        self.home_icon = pygame.image.load(home_path).convert_alpha()
        self.home_icon = pygame.transform.scale(self.home_icon, (50, 50))
        self.checkbox_checked = pygame.image.load(checkbox_checked_path).convert_alpha()
        self.checkbox_checked = pygame.transform.scale(self.checkbox_checked, (30, 30))
        self.checkbox_unchecked = pygame.image.load(checkbox_unchecked_path).convert_alpha()
        self.checkbox_unchecked = pygame.transform.scale(self.checkbox_unchecked, (30, 30))

        self.filter_labels = {
            'favorites': '즐겨찾기',
            '1': '초급',
            '2': '중급',
            '3': '고급',
            'wrong': '틀린단어'
        }
        self.filter_buttons = {
            'favorites': pygame.Rect(150, 50, 30, 30),
            '1': pygame.Rect(300, 50, 30, 30),
            '2': pygame.Rect(420, 50, 30, 30),
            '3': pygame.Rect(560, 50, 30, 30),
            'wrong': pygame.Rect(750, 50, 30, 30)
        }
        self.selected_levels = []
        self.show_favorites_only = False
        self.show_wrong_only = False

        self.current_image = self.star_black
        self.showing_meaning = False

        # Search input and button
        self.search_box = Input("", self, pygame.Rect(50, 600, 200, 32))
        self.search_button = pygame.Rect(260, 600, 80, 32)

    def draw_text_centered(self, surface, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

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

    def display_word(self, word, current_index, total_cards, is_favorite):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (240, 248, 255), (100, 100, 600, 400))
        word_surface = self.font.render(word, True, (0, 0, 0))
        self.screen.blit(word_surface, (400 - word_surface.get_width() // 2, 260 - word_surface.get_height() // 2))
        if not self.show_favorites_only and not self.show_wrong_only:
            self.toggle_image(is_favorite)
        self.draw_buttons()
        self.display_page_number(current_index, total_cards)
        self.draw_search()
        pygame.display.flip()

    def draw_search(self):
        # Draw search box and button
        self.search_box.draw(self.screen)
        pygame.draw.rect(self.screen, pygame.Color('lightskyblue3'), self.search_button)
        self.draw_text_centered(self.screen, "검색", self.font_small, (0, 0, 0), self.search_button)

    def display_meaning(self, word, meaning, current_index, total_cards, is_favorite):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (240, 248, 255), (100, 100, 600, 400))
        word_surface = self.font.render(word, True, (0, 0, 0))
        meaning_surface = self.font_small.render(meaning, True, (0, 0, 0))
        self.screen.blit(word_surface, (400 - word_surface.get_width() // 2, 260 - word_surface.get_height() // 2))
        self.screen.blit(meaning_surface,
                         (400 - meaning_surface.get_width() // 2, 360 - meaning_surface.get_height() // 2))
        if not self.show_favorites_only and not self.show_wrong_only:
            self.toggle_image(is_favorite)
        self.draw_buttons()
        self.display_page_number(current_index, total_cards)
        self.draw_search()
        pygame.display.flip()

    def display_no_wordcards(self):
        self.screen.fill((255, 255, 255))
        no_wordcards_surface = self.font_small.render("No wordcards found", True, (0, 0, 0))
        self.screen.blit(no_wordcards_surface,
                         (400 - no_wordcards_surface.get_width() // 2, 260 - no_wordcards_surface.get_height() // 2))
        self.draw_buttons()
        self.draw_search()
        pygame.display.flip()

    def draw_buttons(self):
        self.screen.blit(self.left_arrow, (520, 520))
        self.screen.blit(self.right_arrow, (620, 520))

        star_rect = None  # 초기화
        if not self.show_favorites_only and not self.show_wrong_only:
            star_rect = self.current_image.get_rect(topleft=(620, 130))
            self.screen.blit(self.current_image, star_rect.topleft)

        sound_rect = self.sound_icon.get_rect(topleft=(730, 130))  # 소리 아이콘 위치 조정
        self.screen.blit(self.sound_icon, sound_rect.topleft)
        self.screen.blit(self.home_icon, (680, 580))

        for level, rect in self.filter_buttons.items():
            label_surface = self.font_small.render(self.filter_labels[level], True, (0, 0, 0))
            self.screen.blit(label_surface, (rect.x - label_surface.get_width() - 10, rect.y))
            checkbox_image = self.checkbox_checked if level in self.selected_levels or (
                        level == 'favorites' and self.show_favorites_only) or (
                                                                  level == 'wrong' and self.show_wrong_only) else self.checkbox_unchecked
            self.screen.blit(checkbox_image, (rect.x, rect.y))

        pygame.display.flip()
        return star_rect, sound_rect  # 반환하여 컨트롤러에서 클릭을 감지할 수 있게 함

    def toggle_image(self, is_favorite):
        self.current_image = self.star if is_favorite else self.star_black

    def display_page_number(self, current_index, total_cards):
        page_number_surface = self.font_tiny.render(f"{current_index + 1} / {total_cards}", True, (0, 0, 0))
        self.screen.blit(page_number_surface, (400 - page_number_surface.get_width() // 2, 500))
