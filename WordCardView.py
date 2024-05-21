import pygame

class WordCardView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Malgun Gothic", 48)
        self.font_small = pygame.font.SysFont("Malgun Gothic", 28)

        # 이미지 로드
        self.left_arrow = pygame.image.load("left_arrow.png").convert_alpha()
        self.left_arrow = pygame.transform.scale(self.left_arrow, (50, 50))
        self.right_arrow = pygame.image.load("right_arrow.png").convert_alpha()
        self.right_arrow = pygame.transform.scale(self.right_arrow, (50, 50))
        self.sound_icon = pygame.image.load("sound.png").convert_alpha()
        self.sound_icon = pygame.transform.scale(self.sound_icon, (50, 50))
        self.star_black = pygame.image.load("black_star.png").convert_alpha()
        self.star_black = pygame.transform.scale(self.star_black, (50, 50))
        self.star = pygame.image.load("star.png").convert_alpha()
        self.star = pygame.transform.scale(self.star, (50, 50))
        self.home_icon = pygame.image.load("home.png").convert_alpha()
        self.home_icon = pygame.transform.scale(self.home_icon, (50, 50))

        self.current_image = self.star_black
        self.showing_meaning = False

    def display_word(self, word):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (240, 248, 255), (100, 100, 600, 400))
        word_surface = self.font.render(word, True, (0, 0, 0))
        self.screen.blit(word_surface, (400 - word_surface.get_width() // 2, 260 - word_surface.get_height() // 2))
        self.draw_buttons()
        pygame.display.flip()

    def display_meaning(self, meaning):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (240, 248, 255), (100, 100, 600, 400))
        meaning_surface = self.font_small.render(meaning, True, (0, 0, 0))
        self.screen.blit(meaning_surface, (400 - meaning_surface.get_width() // 2, 360 - meaning_surface.get_height() // 2))
        self.draw_buttons()
        pygame.display.flip()

    def display_no_wordcards(self):
        self.screen.fill((255, 255, 255))
        no_wordcards_surface = self.font_small.render("No wordcards found", True, (0, 0, 0))
        self.screen.blit(no_wordcards_surface, (400 - no_wordcards_surface.get_width() // 2, 260 - no_wordcards_surface.get_height() // 2))
        self.draw_buttons()
        pygame.display.flip()

    def draw_buttons(self):
        self.screen.blit(self.left_arrow, (520, 520))
        self.screen.blit(self.right_arrow, (620, 520))
        self.screen.blit(self.sound_icon, (700, 100))
        self.screen.blit(self.current_image, (600, 100))
        self.screen.blit(self.home_icon, (50, 50))
        pygame.display.flip()

    def toggle_image(self):
        if self.current_image == self.star_black:
            self.current_image = self.star
        else:
            self.current_image = self.star_black

    def display_word_and_meaning(self, word, meaning):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (240, 248, 255), (100, 100, 600, 400))

        # 단어와 뜻을 화면에 표시
        word_surface = self.font.render(word, True, (0, 0, 0))
        meaning_surface = self.font_small.render(meaning, True, (0, 0, 0))

        # 단어는 항상 같은 위치에 표시
        word_x = 400 - word_surface.get_width() // 2
        word_y = 260 - word_surface.get_height() // 2
        self.screen.blit(word_surface, (word_x, word_y))

        # 뜻은 단어 아래에 표시
        meaning_x = 400 - meaning_surface.get_width() // 2
        meaning_y = word_y + word_surface.get_height() + 20  # 단어 아래 20px
        self.screen.blit(meaning_surface, (meaning_x, meaning_y))

        self.draw_buttons()
        pygame.display.flip()