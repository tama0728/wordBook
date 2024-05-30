import pygame

from Api.Button import Button

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Rectangle(Button):  # Rectangle 클래스가 Button 클래스를 상속받음
    def __init__(self, x, y, width, height, color=BLACK, border_radius=0):
        # Button 클래스의 생성자를 호출하여 초기화
        super().__init__(pygame.Rect(x, y, width, height), '', color)
        self.border_radius = border_radius
        self.text_color = BLACK
        self.font_size = 30
        self.image = None
        self.width = width
        self.height = height
        self.text_lines = []

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            if self.border_radius > 0:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
            else:
                pygame.draw.rect(screen, self.color, self.rect)

        total_text_height = len(self.text_lines) * self.font_size
        start_y = self.rect.centery - total_text_height // 2

        for i, line in enumerate(self.text_lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(
                center=(self.rect.centerx, start_y + self.font_size * i + self.font_size // 2))
            screen.blit(text_surface, text_rect)

    def set_text(self, text, text_color=BLACK, font_size=30):
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.SysFont("d2coding", self.font_size)
        self.text_lines = self.wrap_text(text)

    def wrap_text(self, text):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width, _ = self.font.size(word + ' ')
            if current_width + word_width <= self.rect.width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
